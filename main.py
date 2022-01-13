import json
import requests
import os
from datetime import date, timedelta
from twilio.rest import Client

#   --------------------- CONSTANTS -----------------------
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
today = date.today()
yesterday = today - timedelta(days=1)
daybe4 = today - timedelta(days=2)
STO_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
account_sid = os.environ.get("OWN_ACCOUNT_SID")
auth_token = os.environ.get("OWN_AUTH_TOKEN")

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STO_API_KEY,
}

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "to": daybe4,
    "sort_by": 'relevancy',
    "apiKey": NEWS_API_KEY,
}

stock_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_price = float(stock_data['Time Series (Daily)'][str(yesterday)]['4. close'])
daybe4_price = float(stock_data['Time Series (Daily)'][str(daybe4)]['4. close'])
price_diff = abs(yesterday_price - daybe4_price)
percentage_price_diff = ((price_diff / daybe4_price) * 100)
if percentage_price_diff > 2:
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_article = news_data["articles"][:3]

    news_articles = [[item['title'], item['description']] for item in news_article]
    message = ""
    for news in news_articles:
        message += '\n'.join(news)
        message += '\n\n'
    today = date.today()
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Stock news at {today.strftime('%d/%m/%Y %h:%m')} for {COMPANY_NAME} are: \n\n"
             f"{message}",
        from_='+19388000690',
        to='+447597044364'
    )

# print(json.dumps(data, indent=4))


# print(json.dumps(news_data, indent=4))
