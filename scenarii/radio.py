"""Radio scenario.

usage:
    python radio.py <servername> [port]
    python radio.py  # for localhost on 1883

"""

import sys
import time
import random
import laumio
from laumio import Laumio


def main(laumios):
    laumios = tuple(laumios)

    while True:

        for laumio in random.sample(laumios, len(laumios) // 2):
            print(f'laumio: {laumio.name}')
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
