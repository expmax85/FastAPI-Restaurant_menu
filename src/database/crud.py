from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.schema import Generic, TypeVar
from sqlalchemy.orm import Session

from src.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise AttributeError('Need to define model')

    def create(self, db: Session, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, **kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id_obj: int) -> bool:
        obj = db.query(self.model).get(id_obj)
        db.delete(obj)
        db.commit()
        return True

    def update(self, db: Session, id_obj: int, obj_data: UpdateSchemaType) -> int:
        updated = db.query(self.model).filter(self.model.id == id_obj).update(obj_data.dict(exclude_unset=True))
        db.commit()
        return updated

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[tuple]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id_obj: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id_obj).first()

    def serialize(self, obj: ModelType) -> dict:
        data = {'id': str(obj.id),
                'title': obj.title,
                'description': obj.description
                }
        return data
