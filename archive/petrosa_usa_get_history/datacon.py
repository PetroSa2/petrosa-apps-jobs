import datetime
import json
import logging
import os


import pandas as pd
import pymongo
import yfinance as yf
from kafka import KafkaProducer

COL_NAME = os.environ.get('COL_NAME', 'candles_d1')
INTERVAL = os.environ.get('INTERVAL', "1d")

logging.warning("COL_NAME: " + str(COL_NAME))
logging.warning("INTERVAL: " + str(INTERVAL))


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'), 
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client



def get_data(ticker, period, limit=999999999):

    client = get_client()
    db = client["petrosa_usa"]
    history = db[COL_NAME]

    results = history.find({'ticker': ticker},
                           sort=[('datetime', -1)]).limit(limit)
    results_list = list(results)

    if (len(results_list) == 0):
        return []

    data_df = pd.DataFrame(results_list)

    data_df = data_df.sort_values("datetime")

    data_df = data_df.rename(columns={"open": "Open",
                                      "high": "High",
                                      "low": "Low",
                                      "close": "Close"}
                             )

    data_df = data_df.set_index('datetime')

    return data_df



def get_asset_list():
    client = get_client()
    params = client.petrosa_usa['ticket_list'].find()
    params = list(params)

    return params



def insert_all(k_list) -> None:
    client = get_client()
    col = client.petrosa_usa[COL_NAME]
    try:
        col.insert_many(k_list, ordered=False)
    except Exception as e:
        logging.warning(e)



def upsert_all(k_list) -> None:
    client = get_client()
    col = client.petrosa_usa[COL_NAME]
    command_list = []
    try:
        for item in k_list:
            cmm = pymongo.UpdateOne({"ticker": item["ticker"],
                                     "datetime": item["datetime"]},
                                    {"$set": item}, upsert=True)
            command_list.append(cmm)
            
        col.bulk_write(command_list, ordered=False)

    except Exception as e:
        logging.warning(e)



def json_serial(obj) -> str:
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))



def send_all(k_list) -> None:
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_ADDRESS', 'localhost:9093')
    )
    topic = 'usa_candles_hotline'

    for item in k_list:
        item.pop("_id")
        msg = bytes(json.dumps(item, default=json_serial), 'utf-8')
        producer.send(topic, msg)
        


def get_ticker_data(symbol: str) -> None:
    try:
        symbol_action = yf.Ticker(symbol)
        hist = symbol_action.history(period="max",
                                     interval=INTERVAL, 
                                     timeout=60,
                                     start="2010-01-01",
                                     back_adjust=False)
        # hist = symbol_action.history(interval=INTERVAL, start=since)
        
        new_hist = hist.rename(columns={"Open": "open",
                                        "High": "high",
                                        "Low": "low",
                                        "Close": "close",
                                        "Volume": "vol"})
        new_hist = new_hist.assign(ticker=symbol)
        new_hist = new_hist.assign(origin="yfinance")
        new_hist = new_hist.assign(insert_timestamp=datetime.datetime.utcnow())
        new_hist = new_hist.drop(columns="Dividends")
        new_hist = new_hist.drop(columns="Stock Splits")
        
        new_hist.reset_index(inplace=True)
        
        new_hist = new_hist.rename(columns={"Date": "datetime"})
        
        new_hist['datetime'] = new_hist['datetime'].dt.tz_localize(None)
        
        k_list = new_hist.to_dict("records")
        
        upsert_all(k_list)

    except Exception as e:
        logging.error(e)
