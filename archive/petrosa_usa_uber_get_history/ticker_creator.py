import pandas as pd
import os
import pymongo

stocks = pd.read_csv("petrosa_usa_uber_get_history/russel3k.csv").values

stock_list = []
for stock in stocks:
    item = {}
    item["Symbol"] = stock[0]
    stock_list.append(item)


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:9M1RSaFuut@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client


col = get_client().petrosa_usa["ticker_list"]
col.insert_many(
    stock_list, ordered=False)
