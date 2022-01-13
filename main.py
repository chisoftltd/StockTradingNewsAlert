import json
import requests
import os
from datetime import date, timedelta



#   --------------------- CONSTANTS -----------------------
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
today = date.today()
print(today)
yesterday = today - timedelta(days=1)
print(yesterday)
daybe4 = today - timedelta(days=2)
print(daybe4)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ.get("STOCK_API_KEY"),
}

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "to": daybe4,
    "sort_by": 'relevancy',
    "apiKey": os.environ.get("NEWS_API_KEY")
}

stock_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
print(stock_data['Time Series (Daily)']['2022-01-11']['4. close'])
print(stock_data['Time Series (Daily)']['2022-01-10']['4. close'])
price_diff = float(stock_data['Time Series (Daily)']['2022-01-11']['4. close']) - float(
    stock_data['Time Series (Daily)']['2022-01-10']['4. close'])
print(price_diff)
print((price_diff/float(stock_data['Time Series (Daily)']['2022-01-10']['4. close'])*100))

# print(json.dumps(data, indent=4))


news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
# print(json.dumps(news_data, indent=4))