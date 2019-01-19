"""Radio scenario.

usage:
    python radio.py <servername> [port]
    python radio.py  # for localhost on 1883

"""

import sys
import time
import random
import music
import utils


def complete_manipulation(client):
    commands = ['toggle', 'toggle', 'stop', 'play', 'next', 'pause', 'play', 'previous', 'setvol', 'setvol', 'stop']
    volume = [35, 15]
    nb_vol = 0
    for cmd in commands:
        if cmd != 'setvol' :
            music.music_control(client, cmd, value=None)
        else:
            if nb_vol < len(volume):
                music.music_control(client, cmd, value=volume[nb_vol])
                nb_vol+=1
        time.sleep(2)

def toggle_manip(client):
    music.music_control(client, 'toggle', value=None)
    time.sleep(2)
    music.music_control(client, 'toggle', value=None)
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
    toggle_manip(utils.create_client(servername, port))
