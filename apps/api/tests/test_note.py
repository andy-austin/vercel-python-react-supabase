import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Mock environment variable before any imports
os.environ["POSTGRES_URL_NON_POOLING"] = "postgresql://test:test@localhost:5432/test_db"

# Mock database engine creation to prevent actual connection
with patch("apps.api.database.create_engine") as mock_create_engine:
    mock_create_engine.return_value = MagicMock()
    from apps.api.index import app
    from apps.api.models.note import Note as NoteModel


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def mock_note():
    """Create a mock note object"""
    note = MagicMock(spec=NoteModel)
    note.id = 1
    note.title = "Test Note"
    note.content = "Test content"
    note.is_published = False
    note.created_at = datetime.now(timezone.utc)
    note.updated_at = datetime.now(timezone.utc)
    return note


class TestNoteGraphQLEndpoints:
    @patch("apps.api.schemas.base.get_db")
    def test_notes_query_accessible(self, mock_get_db, client):
        """Test that notes query is accessible via GraphQL"""
        # Mock database session and empty result
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        with patch("apps.api.resolvers.note.NoteResolver.get_all") as mock_get_all:
            mock_get_all.return_value = []

            query = """
            query {
                notes {
                    id
                    title
                    content
                    isPublished
                    createdAt
                    updatedAt
                }
            }
            """

            response = client.post("/graphql", json={"query": query})
            assert response.status_code == 200

            data = response.json()
            # Should not have GraphQL errors
            assert "errors" not in data or not data["errors"]
            # Should have notes data (empty list)
            assert "data" in data
            assert "notes" in data["data"]
            assert isinstance(data["data"]["notes"], list)

    @patch("apps.api.schemas.base.get_db")
    def test_note_by_id_query_accessible(self, mock_get_db, client):
        """Test that note by ID query is accessible via GraphQL"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        with patch("apps.api.resolvers.note.NoteResolver.get_by_id") as mock_get_by_id:
            mock_get_by_id.return_value = None  # Non-existent note

            query = """
            query {
                note(id: 999) {
                    id
                    title
                    content
                    isPublished
                    createdAt
                    updatedAt
                }
            }
            """

            response = client.post("/graphql", json={"query": query})
            assert response.status_code == 200

            data = response.json()
            # Should not have GraphQL errors
            assert "errors" not in data or not data["errors"]
            # Should have note data (null for non-existent)
            assert "data" in data
            assert "note" in data["data"]

    @patch("apps.api.schemas.base.get_db")
    def test_create_note_mutation_accessible(self, mock_get_db, client, mock_note):
        """Test that create note mutation is accessible via GraphQL"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        # Set up mock note with expected values
        mock_note.title = "Test Note from GraphQL"
        mock_note.content = "This is a test note created via GraphQL mutation"
        mock_note.is_published = False

        with patch("apps.api.resolvers.note.NoteResolver.create") as mock_create:
            mock_create.return_value = mock_note

            mutation = """
            mutation {
                createNote(input: {
                    title: "Test Note from GraphQL"
                    content: "This is a test note created via GraphQL mutation"
                    isPublished: false
                }) {
                    id
                    title
                    content
                    isPublished
                    createdAt
                    updatedAt
                }
            }
            """

            response = client.post("/graphql", json={"query": mutation})
            assert response.status_code == 200

            data = response.json()
            # Should not have GraphQL errors
            assert "errors" not in data or not data["errors"]
            # Should have created note data
            assert "data" in data
            assert "createNote" in data["data"]
            created_note = data["data"]["createNote"]

            # Verify the created note has the expected structure
            assert "id" in created_note
            assert created_note["title"] == "Test Note from GraphQL"
            assert (
                created_note["content"]
                == "This is a test note created via GraphQL mutation"
            )
            assert created_note["isPublished"] is False
            assert "createdAt" in created_note
            assert "updatedAt" in created_note

    @patch("apps.api.schemas.base.get_db")
    def test_create_note_mutation_minimal(self, mock_get_db, client, mock_note):
        """Test creating a note with only title"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        # Set up mock note for minimal creation
        mock_note.title = "Minimal Note"
        mock_note.content = None
        mock_note.is_published = False

        with patch("apps.api.resolvers.note.NoteResolver.create") as mock_create:
            mock_create.return_value = mock_note

            mutation = """
            mutation {
                createNote(input: {
                    title: "Minimal Note"
                }) {
                    id
                    title
                    content
                    isPublished
                }
            }
            """

            response = client.post("/graphql", json={"query": mutation})
            assert response.status_code == 200

            data = response.json()
            assert "errors" not in data or not data["errors"]

            created_note = data["data"]["createNote"]
            assert created_note["title"] == "Minimal Note"
            assert created_note["content"] is None
            assert created_note["isPublished"] is False

    @patch("apps.api.schemas.base.get_db")
    def test_update_note_mutation_accessible(self, mock_get_db, client, mock_note):
        """Test that update note mutation is accessible via GraphQL"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        # Set up updated mock note
        updated_note = MagicMock(spec=NoteModel)
        updated_note.id = 1
        updated_note.title = "Updated Note Title"
        updated_note.content = "Original content"
        updated_note.is_published = True
        updated_note.created_at = mock_note.created_at
        updated_note.updated_at = datetime.now(timezone.utc)

        with patch("apps.api.resolvers.note.NoteResolver.update") as mock_update:
            mock_update.return_value = updated_note

            mutation = """
            mutation {
                updateNote(id: 1, input: {
                    title: "Updated Note Title"
                    isPublished: true
                }) {
                    id
                    title
                    content
                    isPublished
                }
            }
            """

            response = client.post("/graphql", json={"query": mutation})
            assert response.status_code == 200

            data = response.json()
            assert "errors" not in data or not data["errors"]

            if data["data"]["updateNote"] is not None:
                updated_note_data = data["data"]["updateNote"]
                assert updated_note_data["title"] == "Updated Note Title"
                assert updated_note_data["isPublished"] is True

    @patch("apps.api.schemas.base.get_db")
    def test_delete_note_mutation_accessible(self, mock_get_db, client):
        """Test that delete note mutation is accessible via GraphQL"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.__next__.return_value = MagicMock()

        with patch("apps.api.resolvers.note.NoteResolver.delete") as mock_delete:
            mock_delete.return_value = True

            mutation = """
            mutation {
                deleteNote(id: 1)
            }
            """

            response = client.post("/graphql", json={"query": mutation})
            assert response.status_code == 200

            data = response.json()
            assert "errors" not in data or not data["errors"]
            assert "data" in data
            assert "deleteNote" in data["data"]
            # The result should be a boolean
            assert isinstance(data["data"]["deleteNote"], bool)

    def test_graphql_schema_includes_note_types(self, client):
        """Test that GraphQL schema includes note-related types"""
        introspection_query = """
        query {
            __schema {
                types {
                    name
                    kind
                }
            }
        }
        """

        response = client.post("/graphql", json={"query": introspection_query})
        assert response.status_code == 200

        data = response.json()
        assert "errors" not in data or not data["errors"]

        type_names = [t["name"] for t in data["data"]["__schema"]["types"]]

        # Check that our note-related types are in the schema
        assert "Note" in type_names
        assert "CreateNoteInput" in type_names
        assert "UpdateNoteInput" in type_names

    def test_invalid_note_mutation_returns_error(self, client):
        """Test that invalid mutations return appropriate errors"""
        # Try to create note without required title
        invalid_mutation = """
        mutation {
            createNote(input: {
                content: "Note without title"
            }) {
                id
                title
            }
        }
        """

        response = client.post("/graphql", json={"query": invalid_mutation})
        assert response.status_code == 200

        data = response.json()
        # Should have GraphQL validation errors
        assert "errors" in data
        assert len(data["errors"]) > 0
