#/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard imports
import utils

# Custom imports
import conf

class Laumio:
    """Laumio class dedicated to the gestion of 1 laumio."""

    def __init__(self, name):
        self.name = name
        self.client = utils.create_client()
        self.topic = conf.COMMAND_TARGET_TOPIC


    def set_pixel(self, led_num, red_value, green_value, blue_value):
        """Change the color of a LED.

        .. note:: Message strucure on 4 bytes: BBBB: LED number, RGB values
        """
        message = struct.pack('BBBB', led_num, red_value, green_value, blue_value)
        topic = self.topic.format(
            name=self.name,
            cmd=set_pixel.__name__
        )
        self.client.publish(topic, payload=message)


    def set_ring(ring_num, red_value, green_value, blue_value):
        """Set the color of a ring.

        .. note:: Message strucure on 4 bytes: BBBB: ring number, RGB values
        """
        message = struct.pack('BBBB', ring_num, red_value, green_value, blue_value)
        topic = self.topic.format(
            name=self.name,
            cmd=set_ring.__name__
        )
        self.client.publish(topic, payload=message)


    def set_column(column_num, red_value, green_value, blue_value):
        """Set the color of a column.

        .. note:: Message strucure on 4 bytes: BBBB: column number, RGB values
        """
        message = struct.pack('BBBB', column_num, red_value, green_value, blue_value)
        topic = self.topic.format(
            name=self.name,
            cmd=set_column.__name__
        )
        self.client.publish(topic, payload=message)


    def color_wipe(timeout, red_value, green_value, blue_value):
        """Progressive fill animation with color and duration.

        .. note:: Message strucure on 4 bytes: BBBB: RGB values, timeout
        """
        message = struct.pack('BBBB', red_value, green_value, blue_value, timeout)
        topic = self.topic.format(
            name=self.name,
            cmd=color_wipe.__name__
        )
        self.client.publish(topic, payload=message)


    def animate_rainbow():
        """Start rainbow animation.

        .. note:: No message needed.
        """
        topic = self.topic.format(
            name=self.name,
            cmd=animate_rainbow.__name__
        )
        self.client.publish(topic, payload=None)


    def fill(red_value, green_value, blue_value):
        """Set all leds with the given color.

        .. note:: Message strucure on 3 bytes: BBB: RGB values
        """
        message = struct.pack('BBB', red_value, green_value, blue_value)
        topic = self.topic.format(
            name=self.name,
            cmd=fill.__name__
        )
        self.client.publish(topic, payload=message)


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
        self.client.publish(topic, payload=json_data)


    def off():
        """ """
        ...

    # function changing the color of the whole laumio
    def all_blue(self):
        """ Change the color of all the LEDs of the laumio to blue"""
        blue = utils.rgb_from_colorname('blue')
        topic = COMMAND_TARGET_TOPIC.format(name=self.name, cmd="fill")
        self.client.publish(topic, payload=blue)

    def all_color([r, g, b]):
        ...

    def all_color(color):
        """ Change the color of all the LEDs of the laumio to chosen color"""
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


