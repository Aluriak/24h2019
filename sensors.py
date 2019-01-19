import paho.mqtt.client as mqtt
import time
    
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
    
