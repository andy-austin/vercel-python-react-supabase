from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class User:
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


@strawberry.input
class CreateUserInput:
    email: str
    full_name: Optional[str] = None


@strawberry.input
class UpdateUserInput:
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
