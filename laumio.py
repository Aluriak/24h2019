#/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard imports
import utils

# Custom imports
import conf

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
        message = struct.pack('BBBB', led_num, red_value, green_value, blue_value)
        topic = self.topic.format(
            name=self.name,
            cmd=set_pixel.__name__
        )
        message = [led_num] + list(rgb_values)
        self._send(topic, message)


    def set_ring(ring_num, rgb_values):
        """Set the color of a ring.

        .. note:: Message strucure on 4 bytes: BBBB: ring number, RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=set_ring.__name__
        )
        message = [ring_num] + list(rgb_values)
        self._send(topic, message)


    def set_column(column_num, rgb_values):
        """Set the color of a column.

        .. note:: Message strucure on 4 bytes: BBBB: column number, RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=set_column.__name__
        )
        message = [column_num] + list(rgb_values)
        self._send(topic, message)


    def color_wipe(timeout, red_value, green_value, blue_value):
        """Progressive fill animation with color and duration.

        .. note:: Message strucure on 4 bytes: BBBB: RGB values, timeout
        """
        topic = self.topic.format(
            name=self.name,
            cmd=color_wipe.__name__
        )
        message = list(rgb_values) + [timeout]
        self._send(topic, message)


    def animate_rainbow():
        """Start rainbow animation.

        .. note:: No message needed.
        """
        topic = self.topic.format(
            name=self.name,
            cmd=animate_rainbow.__name__
        )
        self._send(topic, None)


    def fill(rgb_values):
        """Set all leds with the given color.

        .. note:: Message strucure on 3 bytes: BBB: RGB values
        """
        topic = self.topic.format(
            name=self.name,
            cmd=fill.__name__
        )
        self._send(topic, rgb_values)


    def send_JSON(json_data):
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
            cmd=get_command(send_JSON.__name__)
        )
        self._send(topic, json_data)


    def off():
        """Swith the laumio off. Meaning the color of the laumio is set to black."""
        black = utils.rgb_from_colorname('black')
        self.fill(black)


    # function changing the color of the whole laumio
    def all_blue(self):
        """ Change the color of all the LEDs of the laumio to blue"""
        blue = utils.rgb_from_colorname('blue')
        self.fill(blue)

    def all(color):
        """Change the color of all the LEDs of the laumio to chosen color"""
        rgb = utils.rgb_from_colorname(color)
        topic = COMMAND_TARGET_TOPIC.format(name=self.name, cmd="fill")
        self.client.publish(topic, payload=rgb)

    # functions dealing with the colors of the rings of the laumio 
    def bottom_ring(color):
        """ """
        topic = COMMAND_TARGET_TOPIC.format(name=self.name, cmd="set_ring")
        color = utils.get_color_from_rgb(color)
        message = 
        self.client.publish(topic, payload=message)

    def middle_ring():
        """ """
        ...
    
    def top_ring():
        """ """
        ...

    def _send(self, topic, message:str or [int]):
        """Wrapper around self.client.publish, allowing code to send either str or iterable of integers"""
        return utils.send_through_client(self.client, topic, message)


    @staticmethod
    def init_all():
        client = utils.create_client()
        # detect existing laumio
        # make class instances
        laumios = LaumioGroup(client)
        return  laumios # new GroupLaumio instance
