import logging
from typing import Any

from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.templating import Jinja2Templates

from app.managers import ChatManager
from app.settings import settings

app = FastAPI()
templates = Jinja2Templates(directory='templates')
manager = ChatManager(settings.redis_url)


logger = logging.getLogger(__name__)


@app.on_event('startup')
async def set_connection() -> None:
    await manager.connect()


@app.on_event('shutdown')
async def close_connection() -> None:
    await manager.disconnect()


@app.get('/messages')
async def get_last_messages() -> Any:
    messages = await manager.get_messages(settings.chat_channel)
    return {'messages': messages}


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> Any:
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver, {'websocket': websocket, 'client_id': client_id}),
        (chatroom_ws_sender, {'websocket': websocket, 'client_id': client_id}),
    )


async def chatroom_ws_receiver(websocket: WebSocket, client_id: str) -> Any:
    async for data in websocket.iter_text():
        message = f'Client {client_id} says: {data}'
        logger.info(message)
        await manager.publish(channel=settings.chat_channel, message=message)


async def chatroom_ws_sender(websocket: WebSocket, client_id: str) -> Any:
    async with manager.subscribe(channel=settings.chat_channel) as subscriber:
        logger.info(f'Subscribed client {client_id}')
        async for event in subscriber:
            logger.info(f'Sending message to client {client_id}: {event.message}')
            await websocket.send_text(event.message)
