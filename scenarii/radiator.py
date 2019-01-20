"""A self-monitoring radiator.

Make heat.
Stops when it's hot enough.

The more laptops are making this, the best.

"""

import multiprocessing
from multiprocessing import Pool
from laumio import Laumio

# laumios = list(Laumio.init_all(servername='localhost'))
laumios = list(Laumio.init_all(servername='mpd.lan'))


TARGET = 30  # °C
NB_CPU = multiprocessing.cpu_count()

def make_heat_with_one_CPU(x):
    for _ in range(2**32):
        pass  # make heat

def make_heat_with_all_CPU():
    with Pool(NB_CPU) as p:
        p.map(make_heat_with_one_CPU, [1] * NB_CPU)

def make_heat_by_lighting():
    for laumio in laumios:
        laumio.fill('white')  # because white is more energetic, probably

if __name__ == '__main__':
    print('TEMP:', float(laumios[0].atmos.temperature))
    print('lighting everything…')
    make_heat_by_lighting()
    print('computing heat…')
    while float(laumios[0].atmos.temperature) < TARGET:
        make_heat_with_all_CPU()

