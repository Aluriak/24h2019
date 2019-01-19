
import json
import asyncio
import websockets
# from laumio import Laumio

# laumios = Laumio.init_all()

def render(data:dict):
    print(data)
    is_bot = data['is_bot']
    is_anon = data['is_anon']
    change_size = data['change_size']


async def wk_feed(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            ans = await websocket.recv()
            render(json.loads(ans))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(wk_feed('ws://wikimon.hatnote.com/en/'))

