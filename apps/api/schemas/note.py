from typing import List, Optional

import strawberry

from ..resolvers.note import NoteResolver
from ..types.note import CreateNoteInput, Note, UpdateNoteInput
from .base import BaseSchemaGenerator


class NoteSchemaGenerator(
    BaseSchemaGenerator[NoteResolver, Note, CreateNoteInput, UpdateNoteInput]
):
    resolver_class = NoteResolver
    graphql_type = Note


@strawberry.type
class NoteQueries:
    @strawberry.field
    def notes(self) -> List[Note]:
        return NoteSchemaGenerator.get_all_query()

    @strawberry.field
    def note(self, id: int) -> Optional[Note]:
        return NoteSchemaGenerator.get_by_id_query(id)


@strawberry.type
class NoteMutations:
    @strawberry.field
    def create_note(self, input: CreateNoteInput) -> Note:
        return NoteSchemaGenerator.create_mutation(input)

    @strawberry.field
    def update_note(self, id: int, input: UpdateNoteInput) -> Optional[Note]:
        return NoteSchemaGenerator.update_mutation(id, input)

    @strawberry.field
    def delete_note(self, id: int) -> bool:
        return NoteSchemaGenerator.delete_mutation(id)
