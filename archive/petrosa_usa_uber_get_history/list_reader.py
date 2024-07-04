import pymongo
import os
import requests
import concurrent.futures

def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client

def concat_everything(ticker):
    full_info = get_ticker_info(ticker)
    print(get_ticker_info(ticker))
    ticket_list_col.update_one({"Symbol": ticker}, {"$set": full_info})



def get_ticker_info(ticker):
    url = f"https://api.polygon.io/v3/reference/tickers?ticker={ticker}&active=true&apiKey=APIKEY"
    data = requests.get(url)
    
    ret_data = data.json()

    if ret_data["results"] != []:
        ret_data = ret_data["results"][0]
        ret_data["Symbol"] = ret_data["ticker"]
        return ret_data
    else:
        return {}

ticket_list_col = get_client()["petrosa_usa"]["ticket_list"]

ticket_list = ticket_list_col.find({"active": None})

ticket_list = list(ticket_list)

print(ticket_list)
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as e:
    for item in ticket_list:
        e.submit(concat_everything, item["Symbol"])
