import sensors
from laumio import Laumio

for laumio in Laumio.init_all('mpd.lan', 1883):
    print(sensors.get_atmos(laumio.client))
    break
