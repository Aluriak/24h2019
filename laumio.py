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
        """ """
        ...

    # function changing the color of the whole laumio
    def all_blue(self):
        """ Change the color of all the LEDs of the laumio to blue"""
        blue = utils.get_color_from_rgb('blue')
        topic = COMMAND_TARGET_TOPIC.format(name=self.name, cmd="fill")
        self.client.publish(topic, payload=blue)

    def all_color():
        ...


    # functions dealing with the colors of the rings of the laumio 
    def bottom_ring():
        """ """
        ...

    def middle_ring():
        """ """
        ...
    
    def top_ring():
        """ """
        ...


