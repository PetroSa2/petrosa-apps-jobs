import datetime
import logging
import os


import pymongo


def get_client():
    client = pymongo.MongoClient(
        os.getenv("MONGO_URI", "mongodb://root:N8ojM1GUhx@localhost:27017"),
        readPreference="secondaryPreferred",
        appname="add_crypto_backfiller_day",
    )

    return client


def write_bulk_list(update_list_commands):
    db = get_client().petrosa_crypto
    collection = db['backfill']
    logging.warning('Writing to mongo... NOW')
    collection.bulk_write(update_list_commands)

    return True


def generate_update_commands(item_list):
    update_list_commands = []

    base_item = {}
    base_item['state'] = 0
    base_item['checked'] = False
    base_item['petrosa_timestamp'] = datetime.datetime.utcnow()

    logging.warning('Creating DB commands')
    for item in item_list:
        cmm = pymongo.UpdateOne(item, {
            "$setOnInsert": {**item, **base_item}
        }, upsert=True)

        update_list_commands.append(cmm)

    return update_list_commands


periods = ['5m', '15m', '30m', '1h']

days_prior = 10

current_klines_period_table = 'candles_h1'
current_klines_period = 24
current_klines_time = datetime.datetime.utcnow(
) - datetime.timedelta(hours=current_klines_period)

logging.warning(
    'Connecting to db to look for current_klines updates in the last current_klines_period')
asset_list_raw_table = get_client().petrosa_crypto[current_klines_period_table]
symbols_last_period = []
asset_list_raw_list = asset_list_raw_table.find(
    {"datetime": {"$gte": current_klines_time}, "origin": 'current_klines'})
asset_list_raw_list = list(asset_list_raw_list)


for item in asset_list_raw_list:
    symbols_last_period.append(item['ticker'])

symbols_last_period = list(dict.fromkeys(symbols_last_period))


logging.warning(str(len(symbols_last_period)) +
                ' unique tickers from current_klines on the last current_klines_period')


days_list = []

for _ in range(1, days_prior):
    start_date = (datetime.date.today()
                  - datetime.timedelta(days=_)).isoformat()
    days_list.append(start_date)

item_list = []
for symbol in symbols_last_period:
    for day_item in days_list:
        for period in periods:
            item = {}
            item['symbol'] = symbol
            item['day'] = day_item
            item['period'] = period
            item_list.append(item)

    logging.warning('Size of the long tail: ' +
                    str(len(item_list)) + ' for symbol ' + symbol)
    update_list = generate_update_commands(item_list)
    write_bulk_list(update_list)
    item_list = []


logging.warning('Bye')
