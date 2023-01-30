import json

import aioredis

from src.cache.base_cache import AbstractCache
from src.config import settings


class RedisCache(AbstractCache):

    def __init__(self, redis_url: str) -> None:
        self.redis = aioredis.from_url(redis_url)

    async def set_cache(self, data: dict | list, key: str) -> None:
        await self.redis.set(json.dumps(data), key)

    async def get_cache(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def delete_cache(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_many(self, key_parent: str) -> None:
        async for key in self.redis.scan_iter(f'{key_parent}*'):
            await self.redis.delete(key)


def get_cache() -> AbstractCache:
    return RedisCache(f'redis://{settings.REDIS_HOST}')
