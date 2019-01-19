import utils
import conf

def music_control(client, cmd, value=None):
    topic = conf.COMMAND_MUSIC.format(cmd=cmd)
    if cmd == 'setvol':
        utils.send_though_client(client, topic, value)
    else:
        utils.send_though_client(client, topic)

