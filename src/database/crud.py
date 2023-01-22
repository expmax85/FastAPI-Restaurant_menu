from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.schema import Generic, TypeVar
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise AttributeError('Need to define model')

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, **kwargs)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, id_obj: str, obj_data: UpdateSchemaType) -> int:
        obj_in_data = jsonable_encoder(obj_data)
        updated = await db.execute(update(self.model).filter(self.model.id == id_obj)
                                   .values(**obj_in_data)
                                   .returning(self.model))
        await db.commit()
        return updated.fetchone()

    async def remove(self, db: AsyncSession, id_obj: str) -> bool:
        obj = await db.execute(select(self.model).filter(self.model.id == id_obj))
        result = obj.scalars().first()
        await db.delete(result)
        await db.commit()
        return True

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[tuple]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def get(self, db: AsyncSession, id_obj: str) -> ModelType | None:
        result = await db.execute(select(self.model).filter(self.model.id == id_obj))
        return result.scalars().first()
