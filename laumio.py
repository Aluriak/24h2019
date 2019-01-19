#/usr/bin/env python3
import utils
import conf 

class Laumio:
    """ 
    """

    def __init__(self, name):
        self.name = name
        self.client = utils.create_client()


    def off():
        """ Swith the laumio off. Meaning the color is set to black."""
        rgb = utils.rgb_from_colorname('black')
        topic = self.topic.format(
        name=self.name,
        cmd=fill.__name__
        )
        self.client.publish(topic, payload=rgb)

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


