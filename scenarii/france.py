
import time
from laumio import Laumio

laumios = Laumio.init_all()


while True:

    for laumio in laumios:
        laumio.bottom_ring('blue')
        laumio.middle_ring('white')
        laumio.top_ring('red')
    time.sleep(1)

    for laumio in laumios:
        laumio.off()
    time.sleep(1)
