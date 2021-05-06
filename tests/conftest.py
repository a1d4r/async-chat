import asyncio

import pytest
from async_asgi_testclient import TestClient

from app.main import app


@pytest.fixture()
async def client():
    async with TestClient(app) as client:
        yield client


@pytest.fixture()
async def websocket(client):
    async with client.websocket_connect('/ws/1') as websocket:
        await asyncio.sleep(0.1)
        yield websocket
