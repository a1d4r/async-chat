from typing import Any, List

from broadcaster import Broadcast
from broadcaster._backends.redis import RedisBackend

from app.settings import settings


class ChatRedisBackend(RedisBackend):
    async def publish(self, channel: str, message: Any) -> None:
        await super().publish(channel, message)
        await self._pub_conn.lpush(channel, [message])
        await self._pub_conn.ltrim(channel, 0, settings.queue_length - 1)

    async def get_messages(self, channel: str) -> List[str]:
        return await (await self._pub_conn.lrange(channel, 0, -1)).aslist()


class ChatManager(Broadcast):
    def __init__(self, url: str):
        super().__init__(url)
        self._backend = ChatRedisBackend(url)

    async def get_messages(self, channel: str) -> List[str]:
        return await self._backend.get_messages(channel)
