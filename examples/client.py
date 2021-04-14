# Third Party
import asyncio
import websockets


async def send_data(data):
    uri = "ws://localhost:8765/mock"
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)


async def get_last_data():
    uri = "ws://localhost:8765/last"
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()
        print(data)


async def get_all_data():
    uri = "ws://localhost:8765/all"
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()
        print(data)

asyncio.get_event_loop().run_until_complete(send_data("data-1"))
asyncio.get_event_loop().run_until_complete(send_data("data-2"))
asyncio.get_event_loop().run_until_complete(send_data("data-3"))
asyncio.get_event_loop().run_until_complete(get_last_data())
asyncio.get_event_loop().run_until_complete(get_all_data())
