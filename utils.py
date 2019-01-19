"""various helpers.

"""

import sys
import traceback
from functools import wraps


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


