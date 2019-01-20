# -*- coding: utf-8 -*-


import sensors
import utils
import conf

class ProxyLaumio():

    def __init__(self, laumio, domoticz_id):
        self.laumio = laumio
        self.topic = conf.DOMOTICZ_IN
        self.domoticz_id = domoticz_id


    def atmos(self):
        """Broadcast atmos data to domoticz topic
        Temperature + Humidity + Barometer sensor

        nValue is always 0,
        sValue is string with values separated by semicolon: Temperature;Humidity;Humidity Status;Barometer;Forecast
        Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
        Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain

        { "idx" : 0, "nvalue" : 0, "svalue" : "25;70;3;500;4" }
        """
        Atmos = self.laumio.atmos()

        json_data = {
            "idx": self.domoticz_id,
            "nvalue": 0,
            "svalue": "{TEMP};{HUM};{HUM_STATUS};{BARO};{BARO_FCST}".format(
                TEMP=Atmos.temperature,
                HUM=Atmos.humidite_abs,
                HUM_STATUS=utils.get_thermal_comfort(Atmos.humidite_abs),
                BARO=Atmos.pression,
                BARO_FCST=utils.get_forecast(Atmos.pression)
            )
        }

        self.laumio._send(self.topic, json_data)


