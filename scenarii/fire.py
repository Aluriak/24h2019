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

## 21 anneaux en vertical
## 4 darkorange
##  5 orange
##  5 gold
## 7 yellow
## colors : yellow; gold; orange; darkorange

def main(laumios):
    laumios = tuple(laumios)
    
    #Laumio 9 & 8 : color yellow


    #Laumio 8 : bottom & middle white yellow ; top : yellow
    
    

    while True:

        for laumio in random.sample(laumios, len(laumios) // 2):
            print(f'laumio: {laumio.name}')
            # if laumio.name.endswith('439BA9'):  # the one used by HAUM guys to debug
                # laumio.set_pixel(3, random.choice(('sienna', 'blue', 'green', 'red')))
                # laumio.set_column(1, random.choice(('sienna', 'blue', 'green', 'red')))
            laumio.bottom_ring('blue')
            laumio.middle_ring('white')
            laumio.top_ring('red')
        time.sleep(2)
        print('logoff…')

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
