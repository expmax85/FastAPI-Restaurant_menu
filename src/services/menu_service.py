from uuid import UUID

import aioredis

from src.database.actions import MenuAction
from src.models import Menu

REDIS = aioredis.from_url(
    "redis://web_redis", encoding="utf-8",
)


class MenuService(MenuAction):
    cache_key = 'menu_cache'
    redis = REDIS

    async def get_with_relates(self, menu_id: UUID) -> Menu | None:
        async with self.redis.client() as r:
            menu = await r.get(":".join([self.cache_key, str(menu_id)]))
            if not menu:
                print('not cache')
                menu = super().get_with_relates(menu_id)
                await r.set(":".join([self.cache_key, str(menu_id)]), str(menu))
        return menu


menu_service = MenuService()
