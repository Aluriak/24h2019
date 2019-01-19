import utils
import conf

def music_control(client, cmd, value=None):
    topic = conf.COMMAND_MUSIC.format(cmd=str(cmd))
    if str(cmd) == 'setvol':
        if value is not None :
            utils.send_through_client(client, topic, value)
        else:
            utils.send_through_client(client, topic, 0)
    else:
        utils.send_through_client(client, topic)

