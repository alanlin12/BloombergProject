from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
from stock_tracker import get_active_stocks, get_gaining_stocks

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
async def get_stock_history(request: stock_ticker, period: str = "1d"):
    allowed_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "max"]
    
    if period not in allowed_periods:
        raise HTTPException(status_code=400, detail="Period not valid.")
    
    try:
        stock = yf.Ticker(request.ticker)
        interval = "1d"
        
        match period:
            case "1d":
                interval = "5m" 
            
            case "5d":
                interval = "30m"
            
            case "1mo":
                interval = "90m"
            
            case "3mo":
                interval = "1d"
            
            case "6mo" | "1y":
                interval = "5d"
                
            case _:
                interval = "1mo"
                
                
        history = stock.history(period=period, interval=interval)

        
        price_data = [{
            "date": index.strftime("%Y-%m-%d"),
            "close": round(row["Close"], 2),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "volume": round(row["Volume"])
            
        } for index, row in history.iterrows()
        ]
        
        return{
            "history": price_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"ERROR: {str(e)}")