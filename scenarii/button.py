import utils
from laumio import Laumio
import conf
import sensors
import sys

def main(server, port):
    laumios = Laumio.init_all(servername=server, port=port)
    client = utils.create_client('mpd.lan', 1883)
    dictColor = {'red':sensors.get_bp_button_status(client, 1), 
    'blue':sensors.get_bp_button_status(client, 2),
    'yellow':sensors.get_bp_button_status(client, 3),
    'green':sensors.get_bp_button_status(client, 4)}
    
    while True:
        for k,v in dictColor.values():
            if v: 
                for l in laumios:
                    l.fill(k)


if __name__ == "__main__":
    servname = sys.argv[1]
    port = sys.argv[2]
    main(servname, port)

