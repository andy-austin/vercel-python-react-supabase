from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session

from .database import get_db
from .resolvers.note import NoteResolver
from .types.note import CreateNoteInput, Note, UpdateNoteInput


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def notes(self) -> List[Note]:
        db: Session = next(get_db())
        try:
            notes = NoteResolver.get_notes(db)
            return [
                Note(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    is_published=note.is_published,
                    created_at=note.created_at,
                    updated_at=note.updated_at,
                )
                for note in notes
            ]
        finally:
            db.close()

    @strawberry.field
    def note(self, id: int) -> Optional[Note]:
        db: Session = next(get_db())
        try:
            note = NoteResolver.get_note_by_id(db, id)
            if not note:
                return None
            return Note(
                id=note.id,
                title=note.title,
                content=note.content,
                is_published=note.is_published,
                created_at=note.created_at,
                updated_at=note.updated_at,
            )
        finally:
            db.close()


@strawberry.type
class Mutation:
    @strawberry.field
    def create_note(self, input: CreateNoteInput) -> Note:
        db: Session = next(get_db())
        try:
            note = NoteResolver.create_note(db, input)
            return Note(
                id=note.id,
                title=note.title,
                content=note.content,
                is_published=note.is_published,
                created_at=note.created_at,
                updated_at=note.updated_at,
            )
        finally:
            db.close()

    @strawberry.field
    def update_note(self, id: int, input: UpdateNoteInput) -> Optional[Note]:
        db: Session = next(get_db())
        try:
            note = NoteResolver.update_note(db, id, input)
            if not note:
                return None
            return Note(
                id=note.id,
                title=note.title,
                content=note.content,
                is_published=note.is_published,
                created_at=note.created_at,
                updated_at=note.updated_at,
            )
        finally:
            db.close()

    @strawberry.field
    def delete_note(self, id: int) -> bool:
        db: Session = next(get_db())
        try:
            return NoteResolver.delete_note(db, id)
        finally:
            db.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
