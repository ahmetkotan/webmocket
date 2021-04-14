# Standard Library
import re
import sys
import json
import logging
from typing import Any, Dict, Callable

# Third Party
import asyncio
import websockets
from asgiref.sync import sync_to_async

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO, stream=sys.stdout)


class MockServer:
    stack = []
    url_pattern = re.compile(r"/(?P<bare>[\w\-.]+)")
    mapping: Dict[str, Callable]

    def __init__(self):
        self.mapping = {
            "mock": self.mock,
            "last": self.last,
            "all": self.all,
            "clear": self.clear,
        }

    async def send_data(self, websocket: websockets.WebSocketServerProtocol, data: Any):
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)

        await websocket.send(data)

    async def mock(self, websocket: websockets.WebSocketServerProtocol):
        data = await websocket.recv()
        await sync_to_async(self.stack.append)(data)
        await sync_to_async(logging.info)("Added new data: %s", data)

    async def last(self, websocket: websockets.WebSocketServerProtocol):
        data = await sync_to_async(self.stack.pop)()
        await self.send_data(websocket=websocket, data=data)
        await sync_to_async(logging.info)("Data has been sent in last: %s", data)

    async def all(self, websocket: websockets.WebSocketServerProtocol):
        await self.send_data(websocket=websocket, data=self.stack)
        await sync_to_async(logging.info)("All data has been sent: %s", self.stack)

    async def clear(self, **_):
        await sync_to_async(self.stack.clear)()
        await sync_to_async(logging.info)("Cleared all data")

    async def index(self, websocket: websockets.WebSocketServerProtocol, index: int):
        data = await sync_to_async(self.stack.pop)(index=index)
        await self.send_data(websocket=websocket, data=data)
        await sync_to_async(logging.info)("Data has been sent in %s index: %s", index, data)

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        await sync_to_async(logging.info)("Handled: %s", path)
        search: re.Match
        if search := await sync_to_async(self.url_pattern.search)(path):
            bare: str = await sync_to_async(search.group)("bare")
            if func := self.mapping.get(bare):
                await func(websocket=websocket)
            elif bare.isdecimal():
                await self.index(websocket=websocket, index=int(bare))
            else:
                await sync_to_async(logging.warning)("No match: %s", path)


def serve(bind: str = "0.0.0.0", port: int = 8765):
    logging.info("Started server at %s:%s", bind, port)
    backend = MockServer()
    server = websockets.serve(backend.handler, bind, port)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    loop.run_forever()


if __name__ == "__main__":
    # Standard Library
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bind",
        "-b",
        metavar="ADDRESS",
        default="0.0.0.0",
        help="Specify alternate bind address " "[default: 0.0.0.0]",
    )
    parser.add_argument(
        "--port",
        "-p",
        metavar="PORT",
        action="store",
        default=8765,
        type=int,
        nargs="?",
        help="Specify alternate port [default: 8765]",
    )
    args = parser.parse_args()
    serve(bind=args.bind, port=args.port)
