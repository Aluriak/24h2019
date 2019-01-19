"""Implementation of laupoint, like a breakpoint but with laumio.

Improvements:
- async, to handle fading time
- argument to laupoint, making it fun to use
- handle more gracefully when there's more laumio

"""

import laumio
import syne


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
        self.options['last_laumio'] = laumio

    def set_opt(self, color:str='green'):
        "Populate config based on given args"
        laumios = tuple(laumio.Laumio.init_all())
        return {
            'color': str(color),
            # 'fading_time': float(fading_time),
            'laumios': laumios,
            'remaining_laumios': iter(laumios),
            'last_laumio': None
        }

laupoint = syne.synepoint.laupoint
