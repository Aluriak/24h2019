import time
import random
import laumio
from laumio import Laumio
import conf
from collections import namedtuple
import sys
import utils 

def main(server,port):
    allLaumio = Laumio.init_all(servername=server, port=port)
    for l in allLaumio:
        l.fill([25,25,112])
    
    client = utils.create_client(server,port)
    laumios = randomLaumio(client)
    
	for z in range(10):
	    for i in range(0,10):
	        laumios.laumio1.fill('white')
	        time.sleep(0.02)
	        laumios.laumio1.fill('black')
	    for i in range(0,10):
	        laumios.laumio2.fill('white')
	        time.sleep(0.02)
	        laumios.laumio2.fill('black')
	    for i in range(0,10):
	        laumios.laumio3.fill('white')
	        time.sleep(0.02)
	        laumios.laumio3.fill('black')
	    for i in range(0,10):    
	        laumios.laumio4.fill('white')
	        time.sleep(0.02)
	        laumios.laumio4.fill('black')


def randomLaumio(client):
    Laumios = namedtuple('Laumios',['laumio1', 'laumio2', 'laumio3', 'laumio4'])
    return Laumios(laumio1=Laumio(client, conf.SPATIAL_POSITION[random.randint(0,1)]),
            laumio2=Laumio(client, conf.SPATIAL_POSITION[random.randint(2,4)]),
            laumio3=Laumio(client, conf.SPATIAL_POSITION[random.randint(5,7)]),
            laumio4=Laumio(client, conf.SPATIAL_POSITION[random.randint(8,9)]))
        


if  __name__ == "__main__":
    if len(sys.argv) == 1:
        servername = 'localhost'
        port = 1883
    elif len(sys.argv) == 2:
        servername = sys.argv[1]
        port = 1883
    elif len(sys.argv) == 3:
        servername = sys.argv[1]
        port = sys.argv[2]
    main(servername, int(port))
