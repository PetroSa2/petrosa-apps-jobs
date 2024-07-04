import logging
import time


import pandas as pd
import requests



def get_data_bin(symbol: str,
                 interval='1h',
                 limit=2):

    url = 'https://fapi.binance.com/fapi/v1/klines'

    result = requests.get(
        url, {'symbol': symbol,
              'interval': interval,
              'limit': limit
              }
              )

    if('code' in result.json()):
        logging.error('got an Error here',  result.json(), 'Will sleep 5s')
        if result.json()['code'] != -1023:
            time.sleep(5)
        logging.warning('waking up')
        return None

    df = pd.DataFrame()

    lticker, ldatetime, lopen, lhigh, llow, lclose, lclose_time, lclosed_candle, lqty, lvol, = [
        ], [], [], [], [], [], [], [], [], []

    candle = result.json()[0]
        
    lticker.append(symbol)
    ldatetime.append(candle[0])
    lopen.append(float(candle[1]))
    lhigh.append(float(candle[2]))
    llow.append(float(candle[3]))
    lclose.append(float(candle[4]))
    lvol.append(float(candle[5]))
    lclose_time.append(candle[6])
    lqty.append(float(candle[8]))
    lclosed_candle.append(True)

    df['s'] = lticker
    df['t'] = ldatetime
    df['o'] = lopen
    df['h'] = lhigh
    df['l'] = llow
    df['c'] = lclose
    df['T'] = lclose_time
    df['x'] = lclosed_candle
    df['n'] = lqty
    df['n'] = lvol

    # df = df.set_index('datetime')


    return df
