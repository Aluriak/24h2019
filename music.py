"""À écrire"""

import utils
import conf
import time
from mpd import MPDClient

def music_control(client, cmd, value=None):
    """
    param value used only for cmd='setvol', integer between 0 and 100
    """
    if isinstance(cmd, str):
        topic = conf.COMMAND_MUSIC.format(cmd=cmd)
        if cmd == 'setvol':
            utils.send_through_client(client, topic, value)
        elif cmd == 'getstate':
            status = None
            def on_state_music(client, userdata, message):
                nonlocal status
                status = message.payload.decode()
            client.on_message = on_state_music
            client.subscribe('music/status')
            utils.send_through_client(client, topic)
            time.sleep(2)
            return status
        elif cmd == 'getvol':
            volume = None
            def on_volume_music(client, userdata, message):
                nonlocal volume
                volume = message.payload.decode()
            client.on_message = on_volume_music
            client.subscribe('music/status')
            utils.send_through_client(client, topic)
            time.sleep(2)
            return volume
        else:
            utils.send_through_client(client, topic)
    else :
        print("Use a string for the 'cmd' parameter.")


def mpd_client(host, port):
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(host, port)
    return client

def mpd_play(client, songID):
    client.playid(songID)

#def find_song_id(client, song):
    




