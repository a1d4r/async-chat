import asyncio
import sys
from datetime import datetime
from typing import List

import requests
import websockets
from aioconsole import ainput, aprint

WS_URI = 'ws://localhost:8000/ws'
MESSAGES_URL = 'http://localhost:8000/messages'


def get_last_messages() -> List[str]:
    return requests.get('http://localhost:8000/messages').json()['messages']


async def sender(websocket: websockets.WebSocketClientProtocol) -> None:
    while True:
        await websocket.send(await ainput())


async def receiver(websocket: websockets.WebSocketClientProtocol) -> None:
    while True:
        await aprint(await websocket.recv())


async def main() -> None:
    try:
        for message in reversed(get_last_messages()):
            print(message)
    except requests.RequestException as e:
        print(f'Failed to fetch last messages: {e}')
        sys.exit(1)

    client_id = input('Enter your name: ')

    try:
        async with websockets.connect(f'{WS_URI}/{client_id}') as websocket:
            sender_task = asyncio.create_task(sender(websocket))
            receiver_task = asyncio.create_task(receiver(websocket))
            await asyncio.gather(sender_task, receiver_task)
    except websockets.WebSocketException as e:
        print(f'Websocket error: {e}')


asyncio.run(main())
