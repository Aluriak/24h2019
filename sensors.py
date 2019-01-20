import time
import conf
import utils
from collections import namedtuple
import paho.mqtt.client as mqtt

def sub(client, topic, *, timeout=1):
    last_msg = None
    @utils.crash_on_error
    def set_last_msg(client, userdata, message):
        nonlocal last_msg
        #print('update last_msg')
        last_msg = message.payload.decode()

    client.on_message = set_last_msg
    client.subscribe(topic)
    #print(f'Subscribe to {topic}')
    first_time = time.time()
    while last_msg is None and (time.time()-first_time) < timeout:
        time.sleep(0.01)
    client.unsubscribe(topic)
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
    return sub(client, 'presence/state') == 'ON'

def get_remote(client, cmd):
    return sub(client, conf.REMOTE_CMD_TOPIC.format(cmd=cmd)) == 'ON'

def status(client, device):
    if device in conf.SENSORS_LIST:
        return sub(client, conf.CONNECTION_STATUS_SENSORS.format(sensors=device)) == 'ON'
    else:
        return sub(client, conf.CONNECTION_STATUS_TOPIC.format(name=device)) == 'ON'

def get_bp_led_status(client, numLed):
    return sub(client, conf.SENSORS_BP_LED.format(num=numLed)) == 'ON'

def get_bp_button_status(client, numButton):
    return sub(client, conf.SENSORS_BP_BUTTON.format(num=numButton)) == 'ON'

def set_bp_led(client, numLed, msg='ON'):
    utils.send_through_client(client, conf.SENSORS_BP_CMD_LED.format(num=numLed), msg)

def discover_laumio(client):
    topic = conf.COMMAND_ALL_TOPIC.format(cmd='discover')
    print(f'topic: {topic}')
    laumios = []
    @utils.crash_on_error
    def on_laumio_name(client, userdata, message):
        name = message.payload.decode()
        if name != 'discover':
            print(f'new laumio: {name}')
            laumios.append(name)
    client.on_message = on_laumio_name
    client.subscribe(conf.ANNOUNCE_TOPIC)
    print(f'… ({conf.ANNOUNCE_TOPIC})')
    utils.send_through_client(client, topic)
    time.sleep(3)
    client.unsubscribe(topic)
    print('DONE')
    return tuple(laumios)
