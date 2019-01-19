
import json
import random
import asyncio
import websockets
# from laumio import Laumio

laumios = Laumio.init_all()
available_at = {l: 0 for l in laumios}


def render(data:dict):
    laumio = random.choice(tuple(l for l, at in tuple(available_at.items()) if time.time() > at))

    change_size = data['change_size']
    if data['is_bot']:
        laumio.top_ring('red')
    elif not data['is_anon']:
        laumio.top_ring('green')
    if change_size < 10:
        laumio.bottom_ring('orange')
        duration = 1
    elif change_size > 1000:
        laumio.middle_ring('yellow')
        duration = 3
    else:
        laumio.bottom_ring('cyan')
        duration = 6
    laumio.color_wipe(duration, 'black')
    available_at[laumio] = time.time() + duration


async def wk_feed(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            ans = await websocket.recv()
            render(json.loads(ans))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(wk_feed('ws://wikimon.hatnote.com/en/'))

