
import time
import paho.mqtt.client as mqtt
from test import on_message, on_publish, on_connect
from utils import crash_on_error

@crash_on_error
def on_subscribe(client, userdata, mid, granted_qos):
    print(f'SUBSCRIBE: client: {client} userdata: {userdata}  mid:{mid}  granted_qos:{granted_qos}')


if __name__ == '__main__':
    clientB = mqtt.Client(client_id="912898V7938")
    clientB.connect('localhost', port=1883)
    clientB.on_message = on_message
    clientB.on_connect = on_connect
    clientB.on_publish = on_publish
    clientB.on_subscribe = on_subscribe

    clientB.subscribe('sensor/temperature')
    clientB.loop_forever()
