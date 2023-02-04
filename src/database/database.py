from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = AsyncSession(bind=engine, expire_on_commit=False)
Base = declarative_base()


class AbstractAsyncSession(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError


class SQLSession(AbstractAsyncSession):
    def __init__(self, session: AsyncSession = async_session) -> None:
        self.session = session

    async def __aenter__(self) -> "SQLSession":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        try:
            await self.commit()
        except Exception:
            await self.rollback()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def get_db() -> AbstractAsyncSession:
    return SQLSession()
