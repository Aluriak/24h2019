# -*- coding: utf-8 -*-

import json
import time

from laumio import Laumio
import sensors
import utils
import conf

class ProxyLaumio():

    def __init__(self, laumio): # domoticz_id):
        self.laumio = laumio
        self.topic = conf.DOMOTICZ_IN
        #self.domoticz_id = domoticz_id


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
        self.laumio._send(self.topic, json.dumps(json_data))


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
        self.laumio._send(self.topic, json.dumps(json_data))



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
            self.laumio._send(topic, utils.rgb_from_colorname([0, 0, 0]))
            return

        color = json_data['Color']
#        print("couleur demandee")
        self.laumio._send(topic, utils.rgb_from_colorname([color['r'], color['g'], color['b']]))


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

        self.laumio._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchRed'],
            'nvalue': nvalue.get(red, None),
        }))
        self.laumio._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchYellow'],
            'nvalue': nvalue.get(blue, None),
        }))
        self.laumio._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchGreen'],
            'nvalue': nvalue.get(yellow, None),
        }))
        self.laumio._send(self.topic, json.dumps({
            'idx': conf.BUTTONS_IDX['SwitchBlue'],
            'nvalue': nvalue.get(green, None),
        }))


#    def set_selector_switch(self):
#        """
#        """
#
#
#        retval = sensors.sub(client, conf.DOMOTICZ_OUT)
#        if retval is None:
#            return
#
#        json_data = json.loads(retval)
#
#        if json_data['idx'] not in tuple(conf.BUTTONS_IDX.values()):
#            return
#
#        print(retval)
#
#
#        def check_json(json_data):
#
#            idx = json_data['idx']
#            BUTTONS_LAUMIO[idx]
#
#            _send(self, topic, message:str or [int]):

        #data = check_json(red)
#            if data:
#
#            elif check_json(blue):
#
#            elif check_json(yellow):
#
#            elif check_json(green):
#
#            print(json_data['nvalue'],
#                  json_data['svalue1']


if __name__ == "__main__":

    allLaumio = Laumio.init_all(servername="localhost")
    all_proxy = [ProxyLaumio(laumio) for laumio in allLaumio]

    while True:
        prox = all_proxy[0]
#        prox.atmos()
#        prox.distance()
        prox.led_switch()

        time.sleep(0.5)


#    import time
#    client = utils.create_client(servername="mpd.lan")
#    laumio = Laumio(client, "Laumio_1D9486")
#    proxy = ProxyLaumio(laumio)
#
#    i = 0
#    while(True):
#        print(i)
##        proxy.atmos()
##        proxy.distance()
#        proxy.led_switch()
##        proxy.get_selector_switch()
#        i += 1
#        time.sleep(0.2)
#
