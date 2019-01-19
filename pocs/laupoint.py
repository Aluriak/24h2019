"""Implementation of laupoint, like a breakpoint but with laumio.

Improvements:
- async, to handle fading time
- argument to laupoint, making it fun to use
- handle more gracefully when there's more laumio

"""

import time
import syne
import laumio


class Laupoint(metaclass=syne.synepoint.Synepoint):
    """A laupoint associate to one breakpoint a laumio.

    """

    def new_point(self):
        "Return a new laumio to handle"
        return [next(self.options['remaining_laumios'], None)]

    def on_point(self, laumio):
        "Action to do when encountering a point with given laumio"
        if self.options['last_laumio']:
            self.options['last_laumio'].off()
        if laumio is None:
            raise RuntimeError(f"Not enough Laumio to render code ({len(self.options['laumios'])} were available)")
        laumio.fill(self.options['color'])
        time.sleep(self.options['duration'])
        print(f"{self.options['color']} for {self.options['duration']}s")
        self.options['last_laumio'] = laumio

    def set_opt(self, color:str='green', host:str='localhost', port:int=1883, duration:float=0.9):
        "Populate config based on given args"
        laumios = tuple(laumio.Laumio.init_all(servername=host, port=port))
        return {
            'color': str(color),
            # 'fading_time': float(fading_time),
            'duration': duration,
            'laumios': laumios,
            'laumios': laumios,
            'remaining_laumios': iter(laumios),
            'last_laumio': None
        }

laupoint = syne.synepoint.laupoint
