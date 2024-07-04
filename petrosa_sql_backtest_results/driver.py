import logging
import os
import sys

import dotenv
from petrosa.database import mongo
from petrosa.database import sql


dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

if (os.getenv("MARKET") == "CRYPTO"):
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_CRYPTO_SERVER", "")
    os.environ["MYSQL_USER"] = os.getenv("MYSQL_CRYPTO_USER", "")
    os.environ["MYSQL_PASSWORD"] = os.getenv("MYSQL_CRYPTO_PASSWORD", "")
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_CRYPTO_SERVER", "")
    os.environ["MYSQL_DB"] = os.getenv("MYSQL_CRYPTO_DB", "")
    MONGO_DB = "petrosa_crypto"
elif (os.getenv("MARKET") == "B3"):
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_B3_SERVER", "")
    os.environ["MYSQL_USER"] = os.getenv("MYSQL_B3_USER", "")
    os.environ["MYSQL_PASSWORD"] = os.getenv("MYSQL_B3_PASSWORD", "")
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_B3_SERVER", "")
    os.environ["MYSQL_DB"] = os.getenv("MYSQL_B3_DB", "")
    MONGO_DB = "petrosa_b3"
elif (os.getenv("MARKET") == "USA", ""):
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_USA_SERVER", "")
    os.environ["MYSQL_USER"] = os.getenv("MYSQL_USA_USER", "")
    os.environ["MYSQL_PASSWORD"] = os.getenv("MYSQL_USA_PASSWORD", "")
    os.environ["MYSQL_SERVER"] = os.getenv("MYSQL_USA_SERVER", "")
    os.environ["MYSQL_DB"] = os.getenv("MYSQL_USA_DB", "")
    MONGO_DB = "petrosa_usa"
else:
    sys.exit(1)


client = mongo.get_client()
backtest_results = list(client[MONGO_DB]["backtest_results"].find({}))

def build_delete_sql(ids_list, table):
    final_string = ""
    
    for item in ids_list:
        final_string += f"'{item}', "
    
    final_string = final_string[:-2]
    
    sql = f"DELETE FROM {table} WHERE _id IN ({final_string});"
    
    return sql

def delete_from_ids(ids, table):
    logging.info(f"Deleting {len(ids)} records from {table}")
    sql_state = build_delete_sql(ids, table)
    sql.run_generic_sql(sql_state)

start = 0
end = len(backtest_results)
logging.info(end)
step = 1000
for i in range(start, end, step):
    x = i
    logging.info(x)
    try:
        sql.update_sql(backtest_results[x:x+step], "backtest_results")
    except Exception as e:
        logging.error(e)
        continue

backtest_results_lists = list(
    client[MONGO_DB]["backtest_results_lists"].find({"n_trades": {"$gte": 1}}))


final_list = []

try:
    for item in backtest_results_lists:
        copy_item = item.copy()
        del (copy_item["trades_list"])
        for trade in item["trades_list"]:
            temp_item = trade
            temp_item = {**copy_item, **temp_item}
            final_list.append(temp_item)
except Exception as e:
    logging.info(e)



start = 0
end = len(final_list)
logging.info(end)
step = 1000
for i in range(start, end, step):
    x = i
    logging.info(x)

    da_bomb_list = final_list[x:x+step]
    
    uids = []
    
    for item in da_bomb_list:
        uids.append(item["_id"])
    
    uids = list(set(uids))
    

    try:
        delete_from_ids(uids, "backtest_results_lists")
        sql.update_sql(da_bomb_list, "backtest_results_lists")
    except Exception as e:
        logging.info(final_list[i])
        logging.error(e)
        continue