import os
from datetime import date, timedelta

import pymongo
from dateutil.relativedelta import relativedelta


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:9M1RSaFuut@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client

col = get_client().petrosa_usa["ticker_list"]
ticker_list_ticker_list = list(col.distinct("Symbol"))


distinct_ticker_from = list(get_client().petrosa_usa["candles_d1"].distinct("ticker"))

temp3 = []
for element in ticker_list_ticker_list:
    if element not in distinct_ticker_from:
        temp3.append(element)
        # print("deleting " + element)
        # get_client().petrosa_usa["backtest_controller"].delete_many({"ticket": element})
        # get_client().petrosa_usa["backfill_controller_h1"].delete_many(
        #     {"ticker": element})
        # get_client().petrosa_usa["backfill_controller_d1"].delete_many(
        #     {"ticker": element})


get_client().petrosa_usa["backtest_controller"].delete_many(
    {"symbol": {"$in": temp3}})

get_client().petrosa_usa["backfill_controller_h1"].delete_many(
    {"ticker": {"$in": temp3}})
get_client().petrosa_usa["backfill_controller_d1"].delete_many(
    {"ticker": {"$in": temp3}})
get_client().petrosa_usa["ticker_list"].delete_many(
    {"Symbol": {"$in": temp3}})
print(temp3)