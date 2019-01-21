# -*- coding: utf-8 -*-

# Standard imports
import json
import time
import functools

# Custom imports
from laumio import Laumio
import sensors
import utils
import conf

class ProxyLaumio():

    def __init__(self, laumio): # domoticz_id):
        self.laumio = laumio
        self.topic = conf.DOMOTICZ_IN
        #self.domoticz_id = domoticz_id
        # Add some QoS for a support by flooded servers...
        self._send = functools.partial(self.laumio._send, qos=2, retain=True)


    def atmos(self):
        """Broadcast atmos data to domoticz topic
        Temperature + Humidity + Barometer sensor

        nValue is always 0,
        sValue is string with values separated by semicolon: Temperature;Humidity;Humidity Status;Barometer;Forecast
        Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
        Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain

        { "idx" : 0, "nvalue" : 0, "svalue" : "25;70;3;500;4" }
        """
        Atmos = self.laumio.atmos

        json_data = {
            "idx": conf.ATMOS_IDX,
            "nvalue": 0,
            "svalue": "{TEMP};{HUM};{HUM_STATUS};{BARO};{BARO_FCST}".format(
                TEMP=Atmos.temperature,
                HUM=Atmos.humidite_abs,
                HUM_STATUS=utils.get_thermal_comfort(Atmos.humidite_abs),
                BARO=Atmos.pression,
                BARO_FCST=utils.get_forecast(Atmos.pression)
            )
        }
        print(json_data)
        self._send(self.topic, json.dumps(json_data))


    def distance(self):
        """Broadcast distance value
        """

        dist_value = self.laumio.distance

        json_data = {
            "idx": conf.DIST_IDX,
            "nvalue": 0,
            "svalue": dist_value,
        }
        print(json_data)
        self._send(self.topic, json.dumps(json_data))



    def led_switch(self):
        """
        domoticz/out {
           "Battery" : 255,
           "Color" : null,
           "Level" : 13,
           "RSSI" : 12,
           "description" : "",
           "dtype" : "Color Switch",
           "id" : "00082005",
           "idx" : 5,
           "name" : "rgb switch",
           "nvalue" : 15,
           "stype" : "RGB",
           "svalue1" : "13",
           "switchType" : "Dimmer",
           "unit" : 1
        }

        domoticz/out {
           "Battery" : 255,
           "Color" : {
              "b" : 82,
              "cw" : 0,
              "g" : 255,
              "m" : 3,
              "r" : 156,
              "t" : 0,
              "ww" : 0
           },
           "Level" : 14,                    # intensite
           "RSSI" : 12,
           "description" : "",
           "dtype" : "Color Switch",
           "id" : "00082005",
           "idx" : 5,
           "name" : "rgb switch",
           "nvalue" : 10,                   # 0 si Off, 1+ is On.. ?
           "stype" : "RGB",
           "svalue1" : "14",                # intensite
           "switchType" : "Dimmer",
           "unit" : 1
        }
        """

        # Listen Domoticz
        retval = sensors.sub(self.laumio.client, conf.DOMOTICZ_OUT)
        if retval is None:
            return

        json_data = json.loads(retval)

#        print('idx', json_data['idx'], 'domo id', self.laumio.domoticz_id)
#
##        if json_data['idx'] == self.laumio.domoticz_id:
##            print(json_data.get('Color', None), json_data.get('Color'))

        if json_data['idx'] not in tuple(conf.LAUMIO_IDX.values()) or \
        not json_data.get('Color', None):
            return

        topic = conf.COMMAND_TARGET_TOPIC.format(
            name=conf.REVERSE_LAUMIO_IDX[json_data['idx']],
            cmd='fill'
        )
        print(json_data['nvalue'])
        # nvalue = 0 if Off
        if json_data['nvalue'] == 0:
            print("OFF")
            self._send(topic, utils.rgb_from_colorname([0, 0, 0]))
            return

        color = json_data['Color']
#        print("couleur demandee")
        self._send(topic, utils.rgb_from_colorname([color['r'], color['g'], color['b']]))


    def get_selector_switch(self):
        """Used for IR command

        idx, level

        Off:
        "nvalue" : 0,

        Level1/Red:
        "nvalue" : 1,

        """

        # Laumio subscribe
        red = sensors.sub(self.laumio.client, conf.SENSORS_BP_LED.format(num=1))
        blue = sensors.sub(self.laumio.client, conf.SENSORS_BP_LED.format(num=2))
        yellow = sensors.sub(self.laumio.client, conf.SENSORS_BP_LED.format(num=3))
        green = sensors.sub(self.laumio.client, conf.SENSORS_BP_LED.format(num=4))

        # Broadcast to domoticz
        nvalue = {
            'ON': 1,
            'OFF': 0,
        }

        self._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchRed'],
            'nvalue': nvalue.get(red, None),
        }))
        self._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchYellow'],
            'nvalue': nvalue.get(blue, None),
        }))
        self._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchGreen'],
            'nvalue': nvalue.get(yellow, None),
        }))
        self._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchBlue'],
            'nvalue': nvalue.get(green, None),
        }))


#    def set_selector_switch(self):
#        """
#        """


if __name__ == "__main__":

    # MPD.lan server
    #allLaumio = Laumio.init_all(servername="mpd.lan")
    # Local test server
    allLaumio = Laumio.init_all(servername="localhost")
    all_proxy = [ProxyLaumio(laumio) for laumio in allLaumio]

    # TODO: do not instantiate all laumios because only 1 is needed
    # TODO: make a loop_forever with callbacks instead of a time.sleep...
    # TODO: Some messages are lost (see paho-mqtt limitations), it is better to
    # use callbacks like on_publish()
    i = 0
    while True:
        prox = all_proxy[0]
        if i % 15 == 0:
            # Avoid flooding the topic
            # Get atmos/distance sensors every few seconds
            prox.atmos()
            prox.distance()
        # Get and broadcast LED settings as soon as possible
        prox.led_switch()

        time.sleep(0.2)
        i += 1
