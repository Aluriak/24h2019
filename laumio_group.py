import time
from utils import *
from sensors import discover_laumio 

class LaumioGroup:
    """Iterable over Laumio, taking care of their initialization"""

    def __init__(self, client):
        from laumio import Laumio
        self._laumios = []
        # retrieving of the laumios' names
        laumios_names= discover_laumio(client)
        for name in laumios_names:
            laumio = Laumio(client, name)
            self._laumios.append(laumio)

    def __iter__(self):
        return iter(list(self._laumios))

    def as_matrix(self):
        """As __iter__, but as a matrix matching the real world distribution of laumios"""
        ...


if __name__ == '__main__':
    group = Laumio.init_all()
    laumios = tuple(group)
    laumio = laumios[0]
    laumio.off()
    time.sleep(1)
    laumio.red()
    time.sleep(1)
    if laumio.temperature < 10:
        laumio.all_blue()
    if laumio.temperature > 20:
        laumio.all_red()
        laumio.bottom_ring([255, 255, 255])
    else:
        laumio.all_green()
