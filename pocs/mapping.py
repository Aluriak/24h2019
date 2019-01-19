"""Helper to map precisely where are each laumio

Spatial organization:

    (0)  (1)
            (2)
    (3)  (4)
      (5)   (6)
         (7)
     (8)
           (9)            (10)

    And the one in the HAUM room: (11)


"""
import time
import itertools
from laumio import Laumio


LAST_RUN_YIELDED = {
    'Laumio_1D9486': 0,
    'Laumio_104A13': 1,
    'Laumio_0FBFBF': 2,
    'Laumio_104F03': 3,
    'Laumio_10508F': 4,
    'Laumio_10805F': 5,
    'Laumio_CD0522': 6
    'Laumio_0FC168': 7,
    'Laumio_D454DB': 8,
    'Laumio_107DA8': 9,
    'Laumio_88813D': 10,
    # 'Laumio_439BA9': 11,  # the one that the HAUM use to debug
}

colors = itertools.cycle(('sienna', 'cyan', 'brown', 'black', 'yellow'))
place = {}  # laumio name: physical place

for laumio in Laumio.init_all('mpd.lan', 1883):
    for _ in range(10):
        time.sleep(0.2)
        laumio.fill(next(colors))
    place[laumio.name] = input('> number? ')
    print(place)
