from abc import abstractmethod
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import DeclarativeMeta

from src.database.database import AbstractAsyncSession


class BaseORM:

    @abstractmethod
    def __init__(self, model: DeclarativeMeta, db: AbstractAsyncSession):
        self.model = model
        self.db = db

    async def create(self, obj_in: BaseModel, **kwargs) -> DeclarativeMeta:
        async with self.db as db:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data, **kwargs)
            db.session.add(db_obj)
        return db_obj

    async def update(self, id_obj: UUID, obj_data: BaseModel) -> DeclarativeMeta | None:
        if updated_obj := await self.get(id_obj=id_obj):
            async with self.db as db:
                for key, value in obj_data.dict(exclude_unset=True).items():
                    setattr(updated_obj, key, value)
                db.session.add(updated_obj)
        return updated_obj

    async def remove(self, id_obj: UUID) -> bool:
        if result := await self.get(id_obj=id_obj):
            async with self.db as db:
                await db.session.delete(result)
        return True

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[DeclarativeMeta]:
        async with self.db as db:
            result = await db.session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def get(self, id_obj: UUID) -> DeclarativeMeta | None:
        async with self.db as db:
            result = await db.session.execute(select(self.model).filter(self.model.id == id_obj))
        return result.scalars().first()

    def serialize(self, obj: DeclarativeMeta | Row) -> dict:
        return jsonable_encoder(obj)
