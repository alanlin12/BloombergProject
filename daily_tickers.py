import requests
import json

URL_LINK = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"

params = {
    "count": 10,
    "scrIds": "most_actives",
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL_LINK, headers=headers, params=params)

try:
    data = response.json()
    for item in data["finance"]["result"][0]["quotes"]:
        symbol = item["symbol"]
        name = item.get("shortName", "N/A")
        price = item.get("regularMarketPrice", "N/A")
        print(f"{symbol:10} {name:40} {price}")
except json.JSONDecodeError:
    print("Could not parse JSON.")
