from pydantic import BaseSettings, Field, RedisDsn


class Settings(BaseSettings):
    redis_url: RedisDsn = Field('redis://localhost:6379', env='REDIS_URL')
    chat_channel: str = 'chatroom'
    queue_length: int = 50


settings = Settings()
