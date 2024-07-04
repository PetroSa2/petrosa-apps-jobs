import del_tickers
import pymongo 
import os


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client

client = get_client()

for item in del_tickers.instead:
    client.petrosa_usa['ticket_list'].delete_one({"Symbol": item})
    print(item)

