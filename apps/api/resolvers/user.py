from typing import Optional

from sqlalchemy.orm import Session

from apps.api.models.user import User

from ..models.user import User as UserModel
from ..types.user import CreateUserInput, UpdateUserInput


def get_users(db: Session) -> list[type[User]]:
    return db.query(UserModel).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user_input: CreateUserInput) -> UserModel:
    # Check if user with this email already exists
    existing_user = get_user_by_email(db, user_input.email)
    if existing_user:
        raise ValueError(f"User with email {user_input.email} already exists")

    db_user = UserModel(email=user_input.email, full_name=user_input.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user_id: int, user_input: UpdateUserInput
) -> Optional[UserModel]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    if user_input.full_name is not None:
        db_user.full_name = user_input.full_name
    if user_input.is_active is not None:
        db_user.is_active = user_input.is_active

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
