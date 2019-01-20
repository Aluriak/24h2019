# -*- coding: utf-8 -*-
"""various helpers.

"""

# Standard imports
import uuid
import struct
import traceback
import PIL.ImageColor
from functools import wraps
from matplotlib import colors

import paho.mqtt.client as mqtt


def get_thermal_comfort(humidity_percentage):
    """Return thermal comfort sensation according to the given humidity.

    Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
    """
    if humidity_percentage <= 30:
        # Dry
        return 2
    elif humidity_percentage <= 40:
        # Normal
        return 0
    elif humidity_percentage <= 65:
        # Comfort
        return 1
    else:
        # Wet
        return 3


def get_forecast(atmospheric_pressure):
    """
    Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain
    """

    if not isinstance(atmospheric_pressure, int):  # None
        return 0
    if atmospheric_pressure < 900:  # Rain
        return 4
    elif atmospheric_pressure < 980:  # Cloudy
        return 3
    elif atmospheric_pressure < 1013:  # PartlyCloudy
        return 2
    else:  # Sunny
        return 1


def crash_on_error(func):
    """Decorator for paho callbacks, ensuring the raising of any raised exception"""
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(traceback.format_exc())
            exit(1)
    return wrapped


def create_client(servername:str='localhost', port:int=1883, id_prefix:str='TBC_'):
    """Return a new client initialized with given args"""
    client = mqtt.Client(client_id=id_prefix + str(uuid.uuid4()))
    client.connect(servername, port=int(port))
    client.loop_start()
    return client

@crash_on_error
def send_through_client(client, topic:str, message:str or [int] or None=None):
    """Wrapper around client.publish, allowing code to send either str or iterable of integers"""
    if isinstance(message, (bytes, str)) or message is None:  # it's a message to send
        pass  # nothing to do (message is already correctly initialized)
    else:  # must be an iterable of integers
        integers = tuple(message)
        assert not any(not isinstance(integer, int) or integer > 255 for integer in integers), integers
        message = struct.pack('B' * len(integers), *integers)  # NOPE
        # message = ''.join(map(chr, integers))   # NOPE
        # message = ','.join(map(str, integers))  # NOPE
        # message = bytearray(integers)           # NOPE
        # message = ''.join(map(str, integers))   # NOPE
        # message = bytearray([0, 255, 0, 0])     # NOPE
        # message = ''.join(map(str, integers))   # NOPE
        # print(f'{integers} -> {message}')  # merci Florent pour le fix
    return client.publish(topic, payload=message).wait_for_publish()


def rgb_from_colorname(name:str) -> (int, int, int):
    """

    >>> rgb_from_colorname('red')
    (255, 0, 0)
    >>> rgb_from_colorname('blue')
    (0, 0, 255)
    >>> rgb_from_colorname((70, 113, 125))
    (70, 113, 125)
    >>> rgb_from_colorname('sienna')
    (160, 82, 45)

    """
    if isinstance(name, (tuple, list)):
        if len(name) != 3:
            raise ValueError(f"Given color '{name}' is not a valid RBG color")
        return name
    def from_matplotlib(name:str):
        float_to_int = lambda x: int(round(x*255, 0))
        return tuple(map(float_to_int, colors.to_rgba(name)[:3]))
    hex = PIL.ImageColor.colormap.get(name)
    if hex is None:
        rgb = from_matplotlib(name)
        if rgb is None:
            raise ValueError(f"Unknow color name {name} (see https://stackoverflow.com/a/54165440/3077939 )")
        return rgb
    return tuple(bytes.fromhex(hex[1:]))


