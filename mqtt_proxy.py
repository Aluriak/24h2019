# -*- coding: utf-8 -*-

import json

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


        retval = sensors.sub(client, conf.DOMOTICZ_OUT)
        print(retval)
        if retval is None:
            return

        json_data = json.loads(retval)

        if json_data['idx'] != self.laumio.domoticz_id and \
        json_data.get('Color', None) is None:
            return

        # nvalue = 0 if Off
        if json_data['nvalue'] == 0:
            self.laumio.fill([0, 0, 0])

        color = json_data['Color']
        self.laumio.fill([color['r'], color['g'], color['b']])


    def get_selector_switch(self):
        """Used for IR command

        idx, level

        Off:
        "nvalue" : 0,

        Level1/Red:
        "nvalue" : 1,

        """

        # Laumio subscribe
        red = sensors.sub(client, conf.SENSORS_BP_LED.format(num=1))
        blue = sensors.sub(client, conf.SENSORS_BP_LED.format(num=2))
        yellow = sensors.sub(client, conf.SENSORS_BP_LED.format(num=3))
        green = sensors.sub(client, conf.SENSORS_BP_LED.format(num=4))

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







if __name__ == "__main__":

    import time
    client = utils.create_client()
    laumio = Laumio(client, "Laumio_1D9486")
    proxy = ProxyLaumio(laumio)

    i = 0
    while(i < 150):
        print(i)
        #proxy.atmos()
        #proxy.distance()
        #proxy.led_switch()
        proxy.get_selector_switch()
#        proxy.set_selector_switch()
        i += 1
        time.sleep(1)

