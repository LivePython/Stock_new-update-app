import requests
import datetime
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Getting the date
year = datetime.date.today().year
month = datetime.date.today().month
day_ago = datetime.date.today().day - 1
two_days_ago = datetime.date.today().day - 2


if day_ago < 10 or two_days_ago < 10:
    day_ago = f'0{day_ago}'
    two_days_ago = f'0{two_days_ago}'

day_ago_date = f'{year}-{month}-{day_ago}'
two_days_date = f'{year}-{month}-{two_days_ago}'

# Getting the stock news
api_key = '**********************'
news_endpoint = 'https://newsapi.org/v2/everything'
news_parameter = {
    'q': 'Tesla',
    'from': day_ago_date,
    'sortBy': 'popularity',
    'apiKey': api_key,
}
# Working with the twilio api
account_sid = '*********************************'
auth_token = '******************************'
twilio_number = '+16896002692'
client = Client(account_sid, auth_token)

# Working the API for stock data using the date above
STOCK_API_KEY = '**********************'
end_point = 'https://www.alphavantage.co/query'
parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'interval': '5min',
    'apikey': STOCK_API_KEY,
}

response = requests.get(url=end_point, params=parameters)
response.raise_for_status()
one_day_ago = float(response.json()['Time Series (Daily)'][day_ago_date]['4. close'])
two_day_ago = float(response.json()['Time Series (Daily)'][two_days_date]['4. close'])
difference = abs(one_day_ago - two_day_ago)
percentage_value = (difference / one_day_ago) * 100

if percentage_value > 1 and one_day_ago > two_day_ago:
    news_r = requests.get(url=news_endpoint, params=news_parameter)
    three_article = news_r.json()['articles'][:3]
    formatted_article = [f"{STOCK}🔺{percentage_value}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in
                         three_article]

    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_=twilio_number,
            to="+2349152608026"
        )
elif percentage_value > 1:
    news_r = requests.get(url=news_endpoint, params=news_parameter)
    three_article = news_r.json()['articles'][:3]
    formatted_article = [
        f"{STOCK}🔻{percentage_value}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in
        three_article]

    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_=twilio_number,
            to="+2349152608026"
        )


twilio_failsafe = 'k9woU9KreFA358LzDsbdg4EszLTjy69NUu0idvgT'

