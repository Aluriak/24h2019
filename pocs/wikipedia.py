
import json
import time
import random
import asyncio
import websockets
from laumio import Laumio
from conf import NEXT_TO, SPATIAL_POSITION


class _Laumio:
# class Laumio:
    def __init__(self, name):
        self.name = name
        self.print = lambda *a, **k: None
        # self.print = print
    def top_ring(self, color):
        self.print('COLOR TOP WITH:', color)
    def middle_ring(self, color):
        self.print('COLOR MIDDLE WITH:', color)
    def bottom_ring(self, color):
        self.print('COLOR BOTTOM WITH:', color)
    def color_wipe(self, duration, color):
        self.print('COLOR BOTTOM WITH:', duration, color)

    @staticmethod
    def init_all(*args, **kwargs):
        for name_or_id in SPATIAL_POSITION:
            if isinstance(name_or_id, str):  # it's a name
                yield Laumio(name_or_id)

laumios = Laumio.init_all(servername='mpd.lan', port=1883)
available_at = {l: 0 for l in laumios}

def laumio_of_name(name:str):
    global laumios
    for laumio in laumios:
        print('NAMING:', laumio.name, name)
        if laumio.name == name:
            return laumio

def render(data:dict):
    print('DATA: ', data)
    laumio = random.choice(tuple(l for l, at in tuple(available_at.items()) if time.time() > at))
    change_size = data['change_size']
    if data['is_bot']:
        laumio.top_ring('red')
    elif not data['is_anon']:
        laumio.top_ring('green')
    if int(change_size) < 10:
        laumio.bottom_ring('orange')
        duration = 1
    elif change_size > 1000:
        # make it true for all neighbors of the laumio
        laumio.middle_ring('yellow')
        for nei_id in NEXT_TO[SPATIAL_POSITION[laumio.name]]:
            assert isinstance(SPATIAL_POSITION[nei_id], str), (nei_id, SPATIAL_POSITION[nei_id])
            nei = laumio_of_name(SPATIAL_POSITION[nei_id])
            # print(f'NEI of {laumio.name} ({SPATIAL_POSITION[laumio.name]}): {nei} ({nei_id})')
            if nei:
                nei.color_wipe(1, 'yellow')
            else:
                print(f'UNKNOWN NEI of {laumio.name} ({SPATIAL_POSITION[laumio.name]}): {nei} ({nei_id})')
        duration = 6
    else:
        laumio.bottom_ring('cyan')
        duration = 3
    laumio.color_wipe(duration, 'black')
    available_at[laumio] = time.time() + duration


async def wk_feed(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            ans = await websocket.recv()
            render(json.loads(ans))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(wk_feed('ws://wikimon.hatnote.com/en/'))

    # def gen_data():
        # while True:
            # yield {
                # 'is_bot': random.randint(1, 5) == 1,
                # 'is_anon': random.randint(1, 3) == 1,
                # 'change_size': random.choice((1, 400, 1001)),
            # }
    # import time
    # for data in gen_data():
        # render(data)
        # time.sleep(random.randint(1, 5) / 2)

