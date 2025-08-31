from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from ..models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseResolver(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    @classmethod
    def get_all(cls, db: Session) -> List[ModelType]:
        return db.query(cls.model).all()

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Optional[ModelType]:
        return db.query(cls.model).filter(cls.model.id == id).first()

    @classmethod
    def create(cls, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.__dict__
        db_obj = cls.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(
        cls, db: Session, id: int, obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        db_obj = cls.get_by_id(db, id)
        if not db_obj:
            return None

        obj_data = obj_in.__dict__
        for field, value in obj_data.items():
            if value is not None:
                setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def delete(cls, db: Session, id: int) -> bool:
        db_obj = cls.get_by_id(db, id)
        if not db_obj:
            return False

        db.delete(db_obj)
        db.commit()
        return True
