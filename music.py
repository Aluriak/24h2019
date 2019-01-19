import utils
import conf

def music_control(client, cmd, value=None):
    if isinstance(cmd, str):
        topic = conf.COMMAND_MUSIC.format(cmd=cmd)
        if cmd == 'setvol':
            if value is not None :
                utils.send_through_client(client, topic, value)
            else:
                utils.send_through_client(client, topic, 0)
        elif cmd == 'getstate':
            def on_state_music(client, userdata, message):
                status = message.payload.decode()
            client.on_message = on_state_music
            client.subscribe('music/status')
            utils.send_through_client(client, topic)
            return status
        elif cmd == 'getvol':
            def on_volume_music(client, userdata, message):
                volume = message.payload.decode()
            client.on_message = on_volume_music
            client.subscribe('music/status')
            utils.send_through_client(client, topic)
            return volume
        else:
            utils.send_through_client(client, topic)
    else :
        print("Use a string for the 'cmd' parameter.")
