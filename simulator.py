"""Simulator of Laumio"""

import time
import conf
import utils
from utils import create_client, send_through_client, crash_on_error
from conf import SPATIAL_POSITION


class Laumio:
    def __init__(self, space_id, name:str, host, port):
        self.name = str(name)
        self.client = create_client(servername=host, port=port, id_prefix=f'{space_id}-')
        print('CLIENT:', self.client)
        self.client.on_message = self.on_message
        self.client.subscribe('#')
        # self.client.loop_start()

    @crash_on_error
    def on_message(self, client, userdata, message):
        print(f'MESSAGE({self.name}): {message.payload} (topic: {message.topic})')
        if message.topic == conf.COMMAND_ALL_TOPIC.format(cmd='discover'):
            self.send(conf.ANNOUNCE_TOPIC, self.name)
        else:
            print(f'\tUNKNOW MESSAGE: {message.payload} (topic: {message.topic})')
        print('DONE SENDING')

    def send(self, topic:str, message:str or [int]):
        print(f'SENDING: {message} (topic: {topic})')
        return send_through_client(self.client, topic, message)

    def update(self):
        self.client.loop()
        # print('update')
        pass


class Simulator:
    def __init__(self, host:str='localhost', port:int=1883):
        self.host, self.port = host, int(port)
        self.objects = tuple(
            (laumio_id, name)
            for laumio_id, name in tuple(SPATIAL_POSITION.items())
            if isinstance(laumio_id, int)
        )
        self.objects = tuple(
            Laumio(laumio_id, name, self.host, self.port)
            for laumio_id, name in self.objects[:1]
            if isinstance(laumio_id, int)
        )

    def run(self):
        print('START')
        while True:
            for obj in self.objects:
                obj.update()
            time.sleep(1)


if __name__ == '__main__':
    Simulator().run()
