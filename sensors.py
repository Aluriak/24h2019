import paho.mqtt.client as mqtt
from collections import namedtuple
import time
import conf

def sub(client, topic, *, timeout=1):
    last_msg = None
    def set_last_msg( message):
        last_msg = message.payload
    client.on_message = set_last_msg
    client.subscribe(topic)
    first_time = time.time()
    while last_msg is None and (time.time()-first_time) < timeout:
        time.sleep(0.01)
    return last_msg
   
def get_atmos(client):
    Atmos = namedtuple('Atmos',['temperature','pression','humidite_abs','humidite'])
    return Atmos(temperature=sub(client, 'atmosphere/temperature'), 
            pression=sub(client, 'atmosphere/pression'), 
            humidite_abs=sub(client, 'atmosphere/humidite_absolue'),
            humidite=sub(client, 'atmosphere/humidite'))

def get_dist(client):
    return sub(client, 'distance/value')

def get_detection(client):
    return sub(client, 'presence/state')


def status(client, device):
    return sub(client, CONNECTION_STATUS_SENSORS.format(sensors=device) == 'ON'
    
def laumio_status(client, name):
    return sub(client, CONNECTION_STATUS_TOPIC.format(name=name) == 'ON' 

