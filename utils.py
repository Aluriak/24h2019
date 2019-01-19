"""various helpers.

"""

import sys
import uuid
from matplotlib import colors
import traceback
from functools import wraps

import paho.mqtt.client as mqtt


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
    client.connect(servername, port=port)
    return client


def colorname_to_rgb(name:str) -> (int, int, int):
    """

    >>> colorname_to_rgb('red')
    (255, 0, 0)
    >>> colorname_to_rgb('blue')
    (0, 0, 255)

    """
    float_to_int = lambda x: int(round(x*255, 0))
    return tuple(map(float_to_int, colors.to_rgba(name)[:3]))

