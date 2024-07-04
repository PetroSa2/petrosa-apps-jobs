import logging
import time

import datacon

logging.basicConfig(level=logging.INFO)

list_assets = datacon.get_asset_list()


thread_list = []
candle_list = []

for item in list_assets:
    datacon.get_ticker_data(symbol=item['Symbol'])
    time.sleep(0.5)
    

logging.warning('AND NOW THE LAST BLACK NIGHT OF THE NIGHT')