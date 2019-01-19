#/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import json


# Custom imports
import conf
from laumio_group import LaumioGroup


class Laumio:
    """Laumio class dedicated to the gestion of 1 laumio."""

    def __init__(self, client, name):
        self.name = name
        self.client = client
        self.topic = conf.COMMAND_TARGET_TOPIC


    def set_pixel(self, led_num, rgb_values):
        """Change the color of a LED.

        .. note:: Message strucure on 4 bytes: BBBB: LED number, RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.set_pixel.__name__
        )
        message = [led_num] + list(rgb_values)
        self._send(topic, message)


    def set_ring(self, ring_num, rgb_values):
        """Set the color of a ring.

        .. note:: Message strucure on 4 bytes: BBBB: ring number, RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.set_ring.__name__
        )
        message = [ring_num] + list(rgb_values)
        self._send(topic, message)


    def set_column(self, column_num, rgb_values):
        """Set the color of a column.

        .. note:: Message strucure on 4 bytes: BBBB: column number, RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.set_column.__name__
        )
        message = [column_num] + list(rgb_values)
        self._send(topic, message)


    def color_wipe(self, timeout, rgb_values):
        """Progressive fill animation with color and duration.

        .. note:: Message strucure on 4 bytes: BBBB: RGB values, timeout
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.color_wipe.__name__
        )
        message = list(rgb_values) + [timeout]
        self._send(topic, message)


    def animate_rainbow(self):
        """Start rainbow animation.

        .. note:: No message needed.
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.animate_rainbow.__name__
        )
        self._send(topic, None)


    def fill(self, rgb_values):
        """Set all leds with the given color.

        .. note:: Message strucure on 3 bytes: BBB: RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=self.fill.__name__
        )
        self._send(topic, rgb_values)

    # Alias to fill
    all = fill


    def send_JSON(self, json_data):
        """Send JSON commands.

        .. note:: JSON data is verified here.
        """
        try:
            # Test JSON data
            json.dumps(json_data)
        except ValueError as exc:
            # No JSON object could be decoded
            raise exc

        topic = self.topic.format(
            name=self.name,
            cmd=conf.get_command(self.send_JSON.__name__)
        )
        self._send(topic, json_data)


    def off(self):
        """Swith the laumio off. Meaning the color of the laumio is set to black."""
        black = utils.rgb_from_colorname('black')
        self.fill(black)


    # function changing the color of the whole laumio
    def all_blue(self):
        """ Change the color of all the LEDs of the laumio to blue"""
        blue = utils.rgb_from_colorname('blue')
        self.fill(blue)


    # functions dealing with the colors of the rings of the laumio
    def bottom_ring(self, color):
        """ """
        self.set_ring(conf.RINGS['BOTTOM'], utils.rgb_from_colorname(color))

    def middle_ring(self, color):
        """ """
        self.set_ring(conf.RINGS['MIDDLE'], utils.rgb_from_colorname(color))

    def top_ring(self, color):
        """ """
        self.set_ring(conf.RINGS['TOP'], utils.rgb_from_colorname(color))

    def _send(self, topic, message:str or [int]):
        """Wrapper around self.client.publish, allowing code to send either str or iterable of integers"""
        return utils.send_through_client(self.client, topic, message)


    @staticmethod
    def init_all(servername='localhost', port=1883):
        client = utils.create_client(servername, int(port))
        return LaumioGroup(client)
