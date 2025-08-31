from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session

from .database import get_db
from .resolvers import user as user_resolver
from .types.user import CreateUserInput, UpdateUserInput, User


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def users(self, info) -> List[User]:
        db: Session = next(get_db())
        try:
            users = user_resolver.get_users(db)
            return [
                User(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
                for user in users
            ]
        finally:
            db.close()

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        db: Session = next(get_db())
        try:
            user = user_resolver.get_user_by_id(db, id)
            if not user:
                return None
            return User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        finally:
            db.close()


@strawberry.type
class Mutation:
    @strawberry.field
    def create_user(self, input: CreateUserInput) -> User:
        db: Session = next(get_db())
        try:
            user = user_resolver.create_user(db, input)
            return User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        finally:
            db.close()

    @strawberry.field
    def update_user(self, id: int, input: UpdateUserInput) -> Optional[User]:
        db: Session = next(get_db())
        try:
            user = user_resolver.update_user(db, id, input)
            if not user:
                return None
            return User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        finally:
            db.close()

    @strawberry.field
    def delete_user(self, id: int) -> bool:
        db: Session = next(get_db())
        try:
            return user_resolver.delete_user(db, id)
        finally:
            db.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
