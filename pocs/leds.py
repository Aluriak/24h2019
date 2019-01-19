#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard imports
import struct
import json

# Custom imports
import conf

# TODO: self.topic = conf.COMMAND_TARGET_TOPIC
def set_pixel(self, led_num, red_value, green_value, blue_value):
    """Change the color of a LED.

    .. note:: Message strucure on 4 bytes: BBBB: LED number, RGB values
    """
    message = struct.pack('BBBB', led_num, red_value, green_value, blue_value)
    topic = self.topic.format(
        name=self.name,
        cmd=set_pixel.__name__
    )


def set_ring(ring_num, red_value, green_value, blue_value):
    """Set the color of a ring.

    .. note:: Message strucure on 4 bytes: BBBB: ring number, RGB values
    """
    message = struct.pack('BBBB', ring_num, red_value, green_value, blue_value)
    topic = self.topic.format(
        name=self.name,
        cmd=set_ring.__name__
    )


def set_column(column_num, red_value, green_value, blue_value):
    """Set the color of a column.

    .. note:: Message strucure on 4 bytes: BBBB: column number, RGB values
    """
    message = struct.pack('BBBB', column_num, red_value, green_value, blue_value)
    topic = self.topic.format(
        name=self.name,
        cmd=set_column.__name__
    )


def color_wipe(timeout, red_value, green_value, blue_value):
    """Progressive fill animation with color and duration.

    .. note:: Message strucure on 4 bytes: BBBB: RGB values, timeout
    """
    message = struct.pack('BBBB', red_value, green_value, blue_value, timeout)
    topic = self.topic.format(
        name=self.name,
        cmd=color_wipe.__name__
    )


def animate_rainbow():
    """Start rainbow animation.

    .. note:: No message needed.
    """
    topic = self.topic.format(
        name=self.name,
        cmd=animate_rainbow.__name__
    )


def fill(red_value, green_value, blue_value):
    """Set all leds with the given color.

    .. note:: Message strucure on 3 bytes: BBB: RGB values
    """
    message = struct.pack('BBB', red_value, green_value, blue_value)
    topic = self.topic.format(
        name=self.name,
        cmd=fill.__name__
    )


def send_JSON(json_data):
    """Send JSON commands.

    .. note:: JSON data is verified here.
    """
    print(__name__)
    try:
        # Test JSON data
        json.dumps(json_data)
    except ValueError as exc:
        # No JSON object could be decoded
        raise exc

    topic = self.topic.format(
        name=self.name,
        cmd=get_command(send_JSON.__name__)
    )




if __name__ == "__main__":
    # Ex:
    #set_pixel(1, 2, 3, 4)
    #send_JSON(json.dumps({"test": "foo"}))
    pass
