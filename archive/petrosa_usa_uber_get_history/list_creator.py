import os
from datetime import date, timedelta

import pymongo
from dateutil.relativedelta import relativedelta


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:9M1RSaFuut@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-apps-jobs'
    )

    return client

# col = get_client().petrosa_usa["ticker_list"]
# ticket_list = list(col.find({}))


ticket_list = [{
    "Symbol": "CPER"
}, {
    "Symbol": "GDX"
}, {
    "Symbol": "TLT"
},
               
]

start_dt = date(2010, 1, 1)
end_dt = date(2023, 4, 1)

delta = relativedelta(months=1)

scan_list = []

for ticker in ticket_list:
    running_dt = start_dt
    batch_list = []
    while running_dt <= end_dt:
        # add current date to list by converting  it to iso format
        # increment start date by timedelta
        item = {}
        item["day"] = running_dt.isoformat()
        item["ticker"] = ticker['Symbol']
        item["status"] = 0
        scan_list.append(item)
        batch_list.append(item)
        running_dt += delta
        
    try:
        get_client().petrosa_usa["backfill_controller_d1"].insert_many(
            batch_list, ordered=False)
        get_client().petrosa_usa["backfill_controller_h1"].insert_many(
            batch_list, ordered=False)
    except:
        pass
    
    
# get_client().petrosa_usa["backfill_controller_d1"].insert_many(scan_list, ordered=False)
# get_client().petrosa_usa["backfill_controller_h1"].insert_many(scan_list, ordered=False)