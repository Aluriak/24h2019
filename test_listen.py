
import time
import paho.mqtt.client as mqtt
from test import on_message, on_publish, on_connect

def on_subscribe(client, userdata, mid, granted_qos):
    print(f'SUBSCRIBE: client: {client} userdata: {userdata}  mid:{mid}  granted_qos:{granted_qos}')

help(mqtt.Client(client_id="912898V7938"))

if __name__ == '__main__':
    clientB = mqtt.Client(client_id="912898V7938")
    clientB.connect('localhost', port=1883)
    clientB.on_message = on_message
    clientB.on_connect = on_connect
    clientB.on_publish = on_publish
    clientB.on_subscribe = on_subscribe

    # clientB.loop_start()
    clientB.subscribe('sensor/temperature')
    # time.sleep(10)
    clientB.loop_forever()
