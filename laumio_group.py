import time
import sys
from utils import *
from sensors import discover_laumio 

class LaumioGroup:
    """Iterable over Laumio, taking care of their initialization"""

    def __init__(self, client):
        from laumio import Laumio
        self._laumios = []
        # retrieving of the laumios' names
        laumios_names = discover_laumio(client)
        for name in laumios_names:
            laumio = Laumio(client, name)
            self._laumios.append(laumio)

    def __iter__(self):
        return iter(list(self._laumios))

    def __len__(self):
        return len(self._laumios)

    def as_matrix(self):
        """As __iter__, but as a matrix matching the real world distribution of laumios"""
        ...


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servername = 'localhost'
        port = 1883
    elif len(sys.argv) == 2:
        servername = sys.argv[1]
        port = 1883
    elif len(sys.argv) == 3:
        servername = sys.argv[1]
        port = sys.argv[2]
    else:
        print(__doc__)
    
    from laumio import Laumio
    group = Laumio.init_all(servername=servername, port=port)
    laumios = tuple(group)
    laumio = laumios[0]
    laumio.off()
    time.sleep(1)
    laumio.red()
    time.sleep(1)
    if laumio.temperature < 10:
        laumio.all_blue()
    if laumio.temperature > 20:
        laumio.fill('red')
        laumio.bottom_ring([255, 255, 255])
    else:
        laumio.fill('green')
