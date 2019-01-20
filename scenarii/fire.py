"""France scenario.

usage:
    python fire.py <servername> [port]
    python fire.py  # for localhost on 1883

"""

import sys
import time
import random
import laumio
from laumio import Laumio
import conf

## 21 anneaux en vertical
## 4 darkorange
##  5 orange
##  5 gold
## 7 yellow
## colors : yellow; gold; orange; darkorange

def main(laumios):
    laumios = tuple(laumios)
    colors= ['yellow', 'gold', 'orange', 'darkorange']
    #name = conf.SPATIAL_POSITION[9]
    
    
    for laumio in laumios:
        if laumio.name == conf.SPATIAL_POSITION[9] or laumio.name == conf.SPATIAL_POSITION[8]:
            laumio.fill('yellow')
        elif laumio.name == conf.SPATIAL_POSITION[7]:
            laumio.bottom_ring('yellow')
            laumio.middle_ring('gold')
            laumio.top_ring('gold')
        elif laumio.name == conf.SPATIAL_POSITION[6] or laumio.name == conf.SPATIAL_POSITION[5]:
            laumio.fill('gold')
        elif laumio.name == conf.SPATIAL_POSITION[3] or laumio.name == conf.SPATIAL_POSITION[4]:
            laumio.fill('orange')
        elif laumio.name == conf.SPATIAL_POSITION[2]:
            laumio.bottom_ring('orange')
            laumio.middle_ring('orange')
            laumio.top_ring('darkorange')
        else :
            laumio.fill('darkorange')
    time.sleep(3)
    for laumio in laumios:
        laumio.off()
    time.sleep(2)

   


if __name__ == "__main__":
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
    main(Laumio.init_all(servername=servername, port=port))
