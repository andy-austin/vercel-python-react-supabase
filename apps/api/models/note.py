from sqlalchemy import Boolean, Column, String, Text

from apps.api.models.base import BaseModel


class Note(BaseModel):
    __tablename__ = "note"

    title = Column(String, nullable=False, index=True)
    content = Column(Text)
    is_published = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}')>"
