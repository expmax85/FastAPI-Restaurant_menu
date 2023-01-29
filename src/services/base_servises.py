from abc import ABC, abstractmethod


class Service(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.service_orm = None
        self.cache = None

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def remove(self, *args, **kwargs):
        raise NotImplementedError
