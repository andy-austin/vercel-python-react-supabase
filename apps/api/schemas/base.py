from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from ..database import get_db
from ..resolvers.base import BaseResolver

ResolverType = TypeVar("ResolverType", bound=BaseResolver)
GraphQLType = TypeVar("GraphQLType")
CreateInputType = TypeVar("CreateInputType")
UpdateInputType = TypeVar("UpdateInputType")


class BaseSchemaGenerator(
    Generic[ResolverType, GraphQLType, CreateInputType, UpdateInputType]
):
    resolver_class: Type[ResolverType]
    graphql_type: Type[GraphQLType]

    @classmethod
    def model_to_graphql(cls, model_instance: Any) -> GraphQLType:
        """Convert SQLAlchemy model instance to GraphQL type"""
        model_dict = {}

        # Get all GraphQL type fields using __annotations__
        graphql_fields = getattr(cls.graphql_type, "__annotations__", {})

        for field_name in graphql_fields.keys():
            if hasattr(model_instance, field_name):
                model_dict[field_name] = getattr(model_instance, field_name)

        return cls.graphql_type(**model_dict)

    @classmethod
    def get_all_query(cls) -> List[GraphQLType]:
        db: Session = next(get_db())
        try:
            models = cls.resolver_class.get_all(db)
            return [cls.model_to_graphql(model) for model in models]
        finally:
            db.close()

    @classmethod
    def get_by_id_query(cls, id: int) -> Optional[GraphQLType]:
        db: Session = next(get_db())
        try:
            model = cls.resolver_class.get_by_id(db, id)
            if not model:
                return None
            return cls.model_to_graphql(model)
        finally:
            db.close()

    @classmethod
    def create_mutation(cls, input: CreateInputType) -> GraphQLType:
        db: Session = next(get_db())
        try:
            model = cls.resolver_class.create(db, input)
            return cls.model_to_graphql(model)
        finally:
            db.close()

    @classmethod
    def update_mutation(cls, id: int, input: UpdateInputType) -> Optional[GraphQLType]:
        db: Session = next(get_db())
        try:
            model = cls.resolver_class.update(db, id, input)
            if not model:
                return None
            return cls.model_to_graphql(model)
        finally:
            db.close()

    @classmethod
    def delete_mutation(cls, id: int) -> bool:
        db: Session = next(get_db())
        try:
            return cls.resolver_class.delete(db, id)
        finally:
            db.close()
