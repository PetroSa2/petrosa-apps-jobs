import concurrent.futures
import queue
from datetime import datetime
import os
import requests
import logging


from app import binance_current, sender

logging.basicConfig(level=logging.INFO)


start_datetime = datetime.utcnow()
sender_ins = sender.PETROSASender('binance_klines_current')
msg_queue = queue.Queue()


curr_klines = binance_current.BinanceCurrentKlines(sender_ins)

asset_list_raw = requests.get(
    'https://fapi.binance.com/fapi/v1/ticker/price').json()

asset_list_full = []
for item in asset_list_raw:
    if(item['symbol'][-4:] == 'USDT' or item['symbol'][-4:] == 'BUSD'):
        # print(item)
        asset_list_full.append(item)

period = os.getenv('PERIOD')

origin = "current_klines"

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for symbol in asset_list_full:
        executor.submit(curr_klines.manage_data,
                        symbol['symbol'], period, origin)
