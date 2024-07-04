import datetime
import json
import logging
import os
import time

from petrosa.database import mongo 
from petrosa.messaging import kafkaproducer

logging.basicConfig(level=logging.INFO)


class IntradayBackfiller(object):
    
    def __init__(self) -> None:
        self.client_mg = mongo.get_client()
        
        self.start = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        self.end = end = datetime.datetime.utcnow()
        self.producer = kafkaproducer.get_producer()
        self.topic = 'binance_intraday_backfilling'

        logging.warning('Kafka Brokers : ' +
                        os.getenv('KAFKA_ADDRESS', 'localhost:9092'))
        logging.warning('Started Sender for: ' + self.topic)


    
    def generate_benchmark_list(self, period: str):
        
        if period == '5m':
            minutes = 5
        elif period == '15m':
            minutes = 15
        elif period == '30m':
            minutes = 30
        elif period == '1h':
            minutes = 60
        else:
            minutes = 0

        datepointer = self.start        
        division_list = []
        
        while datepointer <= self.end:
            if(datepointer.minute % minutes == 0):
                division_list.append(datepointer.replace(second=0, microsecond=0).strftime('%s'))
            
            datepointer = datepointer + datetime.timedelta(minutes=1)
        
        division_list.pop(-1)
        
        return division_list


    
    def get_ticker_times(self, ticker: str, period: str):
        if period == '5m':
            suffix = 'm5'
        elif period == '15m':
            suffix = 'm15'
        elif period == '30m':
            suffix = 'm30'
        elif period == '1h':
            suffix = 'h1'
        else:
            suffix = 'nononononono'
            
        col = self.client_mg.petrosa_crypto['candles_' + suffix]
        time_found = col.find({"ticker": ticker, 
                               "datetime": {"$gte": self.start}}, 
                              {"datetime": 1})
                
        ret = []
        for row in list(time_found):
            ret.append(row['datetime'].strftime('%s'))
        
        return ret


    
    def xor_roots(self, ticker, period):
        benchmark = self.generate_benchmark_list(period)
        actual = self.get_ticker_times(ticker, period)
        
        lacking = []
        
        for item in benchmark:
            if item not in actual:
                lacking.append(item)
                
        return lacking


    
    def get_ticker_list(self):
        current_klines_period_table = 'candles_h1'
        current_klines_period = 20
        current_klines_time = datetime.datetime.utcnow(
            ) - datetime.timedelta(days=current_klines_period)

        logging.warning(
            'Connecting to db to look for current_klines updates in the last current_klines_period')
        asset_list_raw_table = self.client_mg.petrosa_crypto[current_klines_period_table]

        asset_list_raw_list = asset_list_raw_table.find(
            {"datetime": {"$gte": current_klines_time}, "origin": 'current_klines'})

        def_ticker_list = {}
        for item in asset_list_raw_list:
            def_ticker_list[item['ticker']] = 'oi'
            
        symbols_last_period = list(dict.fromkeys(def_ticker_list))

        return symbols_last_period
    
    
    
    def send_info(self) -> None:
        ticker_list = self.get_ticker_list()
        period_list = ['5m', '15m', '30m', '1h']
        
        for ticker in ticker_list:
            for period in period_list:
                missing_times = self.xor_roots(ticker,period)
                if len(missing_times) > 0:
                    logging.info('Missing ' + str(len(missing_times)) + ' candles for ' + ticker + ' ' + period)
                    msg = {}
                    msg['ticker'] = ticker
                    msg['period'] = period
                    msg['max'] = max(missing_times)
                    msg['min'] = min(missing_times)
                    logging.warning(msg)
                    self.producer.send(self.topic, bytes(json.dumps(msg), 'utf8'))
                    time.sleep(0.05)
                else:
                    continue

ibf = IntradayBackfiller()
ibf.send_info()
logging.warning('Thank you, WE LOVE YOU ALLLLLLL')