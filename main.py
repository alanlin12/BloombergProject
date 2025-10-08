from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf

app = FastAPI(
    title="Stock Info API",
    description="Gathers simple stock information"
)

class stock_ticker(BaseModel):
    ticker: str

@app.get("/")
async def root():
    return {"message": "Stock Information"}

@app.post("/stock/{stock_ticker}")
async def obtain_stock_data(request: stock_ticker):
    try:
        stock = yf.Ticker(request.ticker)
        info = stock.info
        
        return{
            "ticker": request.ticker.upper(),
            "name": info.get("longName"),
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "volume": info.get("volume")
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticker not found")
        
@app.post("/stock/{stock_ticker}/history")
async def get_stock_history(request: stock_ticker):
    try:
        stock = yf.Ticker(request.ticker)
        history = stock.history(period="6mo")
        
        price_data = [{
            "date": index.strftime("%Y-%m-%d"),
            "price": round(row["Close"], 2)
        } for index, row in history.iterrows()
        ]
        
        return{
            "history": price_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"ERROR: {str(e)}")