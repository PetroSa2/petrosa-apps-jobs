import json
import logging
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random


import pymongo
import requests



def get_client() -> pymongo.MongoClient:
    
    return  pymongo.MongoClient(
            os.getenv(
                'MONGO_URI', 'mongodb://root:9M1RSaFuut@localhost:27017'),
            readPreference='secondaryPreferred',
            appname='petrosa-apps-jobs'
        )

    

def polygon_naming_conversion(kline) -> dict:    
    try:
        converted = {}
        converted['datetime'] = datetime.fromtimestamp(kline['t']/1000.0)
        converted['open'] = kline['o']
        converted['high'] = kline['h']
        converted['low'] = kline['l']
        converted['close'] = kline['c']
        converted['closed_candle'] = True
        converted['petrosa_timestamp'] = datetime.utcnow()
        if('vw' in kline):
            converted['volume_weighted_average_price'] = kline['vw']
        converted['volume'] = kline['v']
        if('vw' in kline and 'v' in kline):
            converted['vol'] = float(kline['v']) * float(kline['vw'])
        if('v' in kline):
            converted['qty'] = kline['v']

        return converted

    except Exception as e:
        logging.exception(e)



def ticker_settings(tf, from_day=None, to_day=None) -> dict:
    config = dict()

    default_settings = {}
    default_settings['m1'] = {}
    default_settings['m1']['multiplier'] = 1
    default_settings['m1']['timespan'] = 'minute'
    default_settings['m1']['timespan_timedelta'] = 'minutes'
    default_settings['m1']['daystokeep'] = 3
    default_settings['m5'] = {}
    default_settings['m5']['multiplier'] = 5
    default_settings['m5']['timespan'] = 'minute'
    default_settings['m5']['timespan_timedelta'] = 'minutes'
    default_settings['m5']['daystokeep'] = 9
    default_settings['m15'] = {}
    default_settings['m15']['multiplier'] = 15
    default_settings['m15']['timespan'] = 'minute'
    default_settings['m15']['timespan_timedelta'] = 'minutes'
    default_settings['m15']['daystokeep'] = 9
    default_settings['m30'] = {}
    default_settings['m30']['multiplier'] = 30
    default_settings['m30']['timespan'] = 'minute'
    default_settings['m30']['timespan_timedelta'] = 'minutes'
    default_settings['m30']['daystokeep'] = 15
    default_settings['h1'] = {}
    default_settings['h1']['multiplier'] = 1
    default_settings['h1']['timespan'] = 'hour'
    default_settings['h1']['timespan_timedelta'] = 'hours'
    default_settings['h1']['daystokeep'] = 30
    default_settings['d1'] = {}
    default_settings['d1']['multiplier'] = 1
    default_settings['d1']['timespan'] = 'day'
    default_settings['d1']['daystokeep'] = 270
    default_settings['w1'] = {}
    default_settings['w1']['multiplier'] = 1
    default_settings['w1']['timespan'] = 'week'
    default_settings['w1']['timespan_timedelta'] = 'weeks'

    default_settings['w1']['daystokeep'] = 1000

    config = default_settings[tf]
    if (from_day is not None):
        config['from_day'] = from_day
    else:
        config['from_day'] = datetime.now(
        ) - timedelta(days=config['daystokeep'])
        config['from_day'] = config['from_day'].date()

    if (to_day is not None):
        config['to_day'] = to_day
    else:
        config['to_day'] = datetime.now().date()

    return config



def build_url(ticker, ticker_config, limit) -> str:
    base_url = "https://api.polygon.io/v2/aggs/ticker/"
    ticker = ticker
    
    full_url = base_url + ticker + '/range/' + str(ticker_config['multiplier'])
    full_url += '/' + ticker_config['timespan'] + '/'
    full_url += str(ticker_config['from_day']) + \
        '/' + str(ticker_config['to_day'])
    full_url += '?adjusted=true&sort=desc&limit=' + limit + '&apiKey='
    full_url += os.environ.get('POLYGON_API_KEY')
    
    return full_url



def process_klines(ticker, results_list) -> list:
    
    if(isinstance(results_list, str)):
        results_list = json.loads(results_list)
    
    time_now = datetime.utcnow()
    kline_list = []

    for _line in results_list['results']:
        try:
            def_kline = polygon_naming_conversion(_line)

            def_kline['origin'] = "polygon"
            def_kline['ticker'] = ticker

            kline_list.append(def_kline)
        except Exception as e:
            logging.exception(e)
            
    return kline_list



def list_to_comms(kline_list) -> list:
    comm_list = []
    for _item in kline_list:
        cmd = pymongo.UpdateOne({"datetime": _item["datetime"],
                                 "ticker": _item["ticker"]}, 
                                {"$set": _item}, upsert=True)
        comm_list.append(cmd)
        
    return comm_list



def get_candles(req_data: dict) -> list:

    ticker_config = ticker_settings(req_data['timeframe'],
                                    req_data.get('from_day', None),
                                    req_data.get('to_day', None)
                                    )

    # print('ticker_config', ticker_config)
    limit = str(req_data.get('limit', 49999))
    full_url = build_url(req_data['ticker'], ticker_config, limit)
    response = requests.get(full_url)
    data = json.loads(response.text)

    return data



def get_end(day: str) -> str:
    le_date = datetime.fromisoformat(day)
    end = le_date + relativedelta(months=1)

    return end.date().isoformat()



def find_param(client) -> dict:
    col = client.petrosa_usa[os.getenv("COL_PARAM", "backfill_controller_h1")]

    param = list(col.find({"status": 0}).limit(200))
    param = random.choices(param)[0]
    
    if(param == {} or param is None):
        param = list(col.find({"status": 1}).limit(200))
        param = random.choices(param)[0]

        if (param == {} or param is None):
            sys.exit(1)
    
    update_param(param=param, status=1, client=client)

    
    return param



def update_param(param, status, client):
    col = client.petrosa_usa[os.getenv("COL_PARAM", "backfill_controller_d1")]
    res = col.update_one({"_id": param["_id"]}, {"$set": {"status": status,
                                                          "petrosa_timestamp": datetime.now()}})
    return res



def generate_data(ticker, start):
       
    data_req = {
        "ticker": ticker,
        "timeframe": os.getenv("INTERVAL", "d1"),
        "from_day": start,
        "to_day": get_end(start),
    }
    
    return data_req
    


def persist_comms(comms, client):
    col = client.petrosa_usa[os.getenv("COL_NAME", "candles_d1")]
    if(len(comms) > 0):
        col.bulk_write(comms, ordered=False)
    else:
        print("EMPTY COMM LIST")