from abc import ABC, abstractmethod


class AbstractCache(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_cache(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def set_cache(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_cache(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, *args, **kwargs):
        raise NotImplementedError
