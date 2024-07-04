import datetime
import logging

from app import bin_data


class BinanceCurrentKlines(object):

    def __init__(self, sender):
        self.sender = sender
        logging.warning('Starting backfiller')


    
    def send_it_forward(self, df, period, origin):
        send_list = df.to_dict('records')

        counter = 0

        for row in send_list:
            prep_row = {}
            prep_row['e'] = "kline"
            prep_row['s'] = row['s']
            prep_row['k'] = row
            prep_row['k']['i'] = period
            prep_row['k']['origin'] = origin
            prep_row['k']['petrosa_timestamp'] = datetime.datetime.utcnow().isoformat()

            counter += 1

            self.sender.send(prep_row)
    
    
    def manage_data(self, 
                    symbol: str, 
                    interval: str, 
                    origin: str):
        data = bin_data.get_data_bin(
            symbol=symbol,
            interval=interval
            )

        if data is not None:
            self.send_it_forward(data, interval, origin)
        return True
    