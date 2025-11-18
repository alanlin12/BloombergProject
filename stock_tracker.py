import requests
import pandas as pd

url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
headers = {"User-Agent": "Mozilla/5.0"}

def get_active_stocks():
    params = {"scrIds": "most_actives"}

    data = requests.get(url, params=params, headers=headers).json()
    quotes = data["finance"]["result"][0]["quotes"]

    df = pd.DataFrame(quotes)[["symbol", "shortName", "regularMarketPrice", "regularMarketChangePercent", "trailingPE"]]
    return df[:10]

def get_gaining_stocks():
    params = {"scrIds": "day_gainers"}
    
    data = requests.get(url, params=params, headers=headers).json()
    quotes = data["finance"]["result"][0]["quotes"]

    df = pd.DataFrame(quotes)[["symbol", "shortName", "regularMarketPrice", "regularMarketChangePercent", "trailingPE"]]
    return df[:10]



