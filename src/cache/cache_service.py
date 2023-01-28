import json

import aioredis

from src.config import settings


class RedisCache:

    def __init__(self, redis_url: str) -> None:
        self.redis = aioredis.from_url(redis_url)

    async def set_cache(self, data: dict, key: str) -> None:
        await self.redis.set(json.dumps(data), key)

    async def get_cache(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def delete_cache(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_all(self, key_parent: str) -> None:
        async for key in self.redis.scan_iter(f"{key_parent}*"):
            await self.redis.delete(key)


cache = RedisCache(f"redis://{settings.REDIS_HOST}")
