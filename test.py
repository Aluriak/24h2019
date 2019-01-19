
import time
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    print(f'MESSAGE: client: {client}   userdata: {userdata}    message: "{message.payload}" (topic: {message.topic})')
def on_publish(*args):
    print(f'PUBLISH: {publish}')
def on_connect(client, userdata, flags, rc):
    print(f'CONNECT: client: {client}   userdata: {userdata}  flags: {flags}  rc: {rc})')


if __name__ == '__main__':

    clientA = mqtt.Client(client_id="192873909187290J")
    clientA.connect('localhost', port=1883)
    clientA.on_connect = on_connect
    clientA.on_publish = on_publish

    # help(client)

    clientA.loop_start()
    clientA.publish('sensor/temperature', payload='24.5')
    clientA.publish('sensor/temperature', payload='24.5')
    clientA.publish('sensor/temperature', payload='24.5')

    clientA.loop_stop()
