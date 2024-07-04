import json
import logging
import os
import time


from petrosa.messaging import kafkaproducer


class PETROSASender(object):
    def __init__(self, topic):
        self.producer = kafkaproducer.get_producer()
        self.topic = topic
        self.total_sent = 0

        logging.warning('Kafka Brokers : ' + os.getenv('KAFKA_ADDRESS', 'localhost:9092'))
        logging.warning('Started Sender for: ' +  self.topic)
        self.start_time = time.time()
        self.last_time_shown = 0

    # Here we create a dual interface for list and for dict
    # Some subscriptions responds different than others, using lists or dicts


    
    def to_send(self, msg):
        if(type(msg) is list):
            for _msg in msg:
                self.send(_msg)
        else:
            self.send(msg)


    
    def send(self, msg) -> None:            
        msg['petrosa_timestamp'] = time.time()

        msg = json.dumps(msg)
        msg = bytes(msg, encoding='utf8')

        self.producer.send(self.topic, msg)
        self.total_sent += 1
