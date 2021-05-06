import asyncio

import pytest


@pytest.mark.asyncio
async def test_client_message_echo(websocket):
    await websocket.send_text('Hello WebSocket')
    received = await websocket.receive_text()

    assert 'Hello WebSocket' in received


@pytest.mark.asyncio
async def test_last_messages(websocket, client):
    await websocket.send_text('I\'m in history')
    await asyncio.sleep(0.1)
    response = await client.get('/messages')

    print(response.json())
    assert 'I\'m in history' in response.json()['messages'][0]
