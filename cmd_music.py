import music 
import sys
import utils

def main():
    cmd = sys.argv[1]
    client = utils.create_client(servername='mpd.lan', port=1883)
    if cmd == 'setval':
        music.music_control(client, cmd, sys.argv[2])
    
    else:
        music.music_control(client, cmd)

if __name__ == "__main__":
    main()
