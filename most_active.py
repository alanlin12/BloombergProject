import requests
import pandas as pd

url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
params = {"scrIds": "most_actives", "count": 5}
headers = {"User-Agent": "Mozilla/5.0"}

data = requests.get(url, params=params, headers=headers).json()
quotes = data["finance"]["result"][0]["quotes"]

df = pd.DataFrame(quotes)[["symbol", "shortName", "regularMarketPrice", "regularMarketChangePercent", "trailingPE"]]
print(df)

