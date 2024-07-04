import datacon
import concurrent.futures
import os
import logging

logging.basicConfig(level=logging.INFO)


client = datacon.get_client()

def thread_agg():
    while True:
        params = datacon.find_param(client)
        data_req = datacon.generate_data(params["ticker"], params["day"])
        candles = datacon.get_candles(data_req)

        print(params)

        if("results" in candles):
            procs = datacon.process_klines(params["ticker"], candles)
            comms = datacon.list_to_comms(procs)
            datacon.persist_comms(comms, client)
            datacon.update_param(params, 2, client)
            print(params, "Recorded")
        else:
            print("Not found, deleting param")
            col = client.petrosa_usa[os.getenv("COL_PARAM", "backfill_controller_d1")]
            col.delete_one({"_id": params["_id"]})


executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=int(os.getenv("GET_THREADS", 5)))
thread_list = []

for item in range(int(os.getenv("GET_THREADS", 5))):
    thread_list.append(executor.submit(thread_agg))

for _thread in thread_list:
    _thread.result()