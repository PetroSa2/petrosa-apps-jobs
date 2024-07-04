from petrosa.database import mongo
from petrosa.messaging import kafkaproducer
from datetime import datetime
import logging
import json
import time

logging.basicConfig(level=logging.INFO)

mg_db = mongo.get_client()['petrosa_crypto']
producer = kafkaproducer.get_producer()

time.sleep(20)

while True:
    backfill = mg_db['backfill'].find_one({"checked": True, "$or": [{"sql_status": 0}, {"sql_status": None}]}, sort=[("day", 1)])

    print(backfill)

    if backfill is not None:
        day = datetime.strptime(backfill['day'], "%Y-%m-%d")
        
        print(day)
        
        if backfill["period"] == "5m":
            col = "candles_m5"
        elif backfill["period"] == "15m":
            col = "candles_m15"
        elif backfill["period"] == "30m":
            col = "candles_m30"
        elif backfill["period"] == "1h":
            col = "candles_h1"
        else:
            logging.error("cant find this specific time frame")
        
        day_data = mongo.get_data_by_date(mongo_db="petrosa_crypto", 
                                        col_name=col,
                                        ticker=backfill['symbol'],
                                        start_date=day)
        day_data['datetime'] = day_data.index
        # print(day_data)
        for item in day_data.to_dict(orient="records"):
            to_send = {
                "k": {
                    "s": item['ticker'],
                    "t": round(item['datetime'].timestamp()*1000),
                    "o": item['open'],
                    "h": item['high'],
                    "l": item['low'],
                    "c": item['close'],
                    "T": round(item['close_time'].timestamp()*1000),
                    "x": True,
                    "n": item['qty'],
                    "i": backfill["period"]
                        }
                    }
            print(to_send)
            msg = json.dumps(to_send)
            msg = bytes(msg, encoding='utf8')
            producer.send(topic="binance_sql_backfiller", value=msg)
            
        mg_db['backfill'].update_one({"_id": backfill["_id"]}, {"$set": {"sql_status": 1}})


    else:
        logging.info("No backfill to process")
