from dateutil.relativedelta import relativedelta
import datetime

def get_end(day: str) -> str:
    le_date = datetime.datetime.fromisoformat(day)
    end = le_date + relativedelta(months=1)


    return end.date().isoformat()

print(get_end('2023-01-01'))
