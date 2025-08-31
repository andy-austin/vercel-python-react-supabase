from ..models.note import Note as NoteModel
from ..types.note import CreateNoteInput, UpdateNoteInput
from .base import BaseResolver


class NoteResolver(BaseResolver[NoteModel, CreateNoteInput, UpdateNoteInput]):
    model = NoteModel

    # Alias methods to maintain existing API
    @classmethod
    def get_notes(cls, db):
        return cls.get_all(db)

    @classmethod
    def get_note_by_id(cls, db, note_id):
        return cls.get_by_id(db, note_id)

    @classmethod
    def create_note(cls, db, note_input):
        return cls.create(db, note_input)

    @classmethod
    def update_note(cls, db, note_id, note_input):
        return cls.update(db, note_id, note_input)

    @classmethod
    def delete_note(cls, db, note_id):
        return cls.delete(db, note_id)
