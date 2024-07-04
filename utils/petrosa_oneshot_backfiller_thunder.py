import requests
import datetime

data = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")

decoded = data.json()

utm_list = []

for symbol in decoded["symbols"]:
    print(symbol['symbol'],datetime.datetime.fromtimestamp( symbol['onboardDate']/1000))

