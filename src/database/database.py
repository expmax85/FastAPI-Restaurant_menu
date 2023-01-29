from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import SQLALCHEMY_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class SQLSession:
    def __init__(self, session: AsyncSession = async_session()) -> None:
        self.session = session

    async def __aenter__(self) -> 'SQLSession':
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


def get_db():
    return SQLSession()
