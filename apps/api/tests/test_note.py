from fastapi.testclient import TestClient

from apps.api.index import app

client = TestClient(app)


class TestNoteGraphQLEndpoints:
    def test_notes_query_accessible(self):
        """Test that notes query is accessible via GraphQL"""
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
        # Should have notes data (can be empty or with items)
        assert "data" in data
        assert "notes" in data["data"]
        assert isinstance(data["data"]["notes"], list)

    def test_note_by_id_query_accessible(self):
        """Test that note by ID query is accessible via GraphQL"""
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
        # Should have note data (likely null for non-existent ID)
        assert "data" in data
        assert "note" in data["data"]

    def test_create_note_mutation_accessible(self):
        """Test that create note mutation is accessible via GraphQL"""
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

    def test_create_note_mutation_minimal(self):
        """Test creating a note with only title"""
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

    def test_update_note_mutation_accessible(self):
        """Test that update note mutation is accessible via GraphQL"""
        # First create a note
        create_mutation = """
        mutation {
            createNote(input: {
                title: "Note to Update"
                content: "Original content"
                isPublished: false
            }) {
                id
            }
        }
        """

        create_response = client.post("/graphql", json={"query": create_mutation})
        create_data = create_response.json()
        note_id = create_data["data"]["createNote"]["id"]

        # Then update it
        update_mutation = f"""
        mutation {{
            updateNote(id: {note_id}, input: {{
                title: "Updated Note Title"
                isPublished: true
            }}) {{
                id
                title
                content
                isPublished
            }}
        }}
        """

        response = client.post("/graphql", json={"query": update_mutation})
        assert response.status_code == 200

        data = response.json()
        assert "errors" not in data or not data["errors"]

        if data["data"]["updateNote"] is not None:
            updated_note = data["data"]["updateNote"]
            assert updated_note["title"] == "Updated Note Title"
            assert updated_note["isPublished"] is True

    def test_delete_note_mutation_accessible(self):
        """Test that delete note mutation is accessible via GraphQL"""
        # First create a note to delete
        create_mutation = """
        mutation {
            createNote(input: {
                title: "Note to Delete"
                content: "This note will be deleted"
                isPublished: false
            }) {
                id
            }
        }
        """

        create_response = client.post("/graphql", json={"query": create_mutation})
        create_data = create_response.json()
        note_id = create_data["data"]["createNote"]["id"]

        # Then delete it
        delete_mutation = f"""
        mutation {{
            deleteNote(id: {note_id})
        }}
        """

        response = client.post("/graphql", json={"query": delete_mutation})
        assert response.status_code == 200

        data = response.json()
        assert "errors" not in data or not data["errors"]
        assert "data" in data
        assert "deleteNote" in data["data"]
        # The result should be a boolean
        assert isinstance(data["data"]["deleteNote"], bool)

    def test_graphql_schema_includes_note_types(self):
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

    def test_invalid_note_mutation_returns_error(self):
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
