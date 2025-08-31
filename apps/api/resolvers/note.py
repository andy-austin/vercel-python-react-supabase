from ..models.note import Note as NoteModel
from ..types.note import CreateNoteInput, UpdateNoteInput
from .base import BaseResolver


class NoteResolver(BaseResolver[NoteModel, CreateNoteInput, UpdateNoteInput]):
    model = NoteModel
