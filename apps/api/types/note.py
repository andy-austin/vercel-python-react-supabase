from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class Note:
    id: int
    title: str
    content: Optional[str]
    is_published: bool
    created_at: datetime
    updated_at: datetime


@strawberry.input
class CreateNoteInput:
    title: str
    content: Optional[str] = None
    is_published: bool = False


@strawberry.input
class UpdateNoteInput:
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
