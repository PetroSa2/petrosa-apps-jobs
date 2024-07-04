import logging
import threading
import time

import datacon

logging.basicConfig(level=logging.INFO)

list_assets = datacon.get_asset_list()

thread_list = []
candle_list = []

for item in list_assets:
    thread_ = threading.Thread(
        target=datacon.get_ticker_data, args=(item['Symbol'], candle_list,)
        )
    thread_list.append(thread_)
    thread_.start()
    time.sleep(0.5)
    

for thread_o in thread_list:
    thread_o.join()
    
datacon.insert_all(candle_list)
datacon.send_all(candle_list)
logging.warning('AND NOW THE LAST BLACK NIGHT OF THE NIGHT')