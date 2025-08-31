# API Documentation

## GraphQL API

The FastAPI GraphQL API provides data access through Strawberry GraphQL schema with modular resolvers and types.

### Endpoint

- **Development**: <http://localhost:8000/graphql>
- **Production**: <https://your-app.vercel.app/api/graphql>

### Schema

#### Types

```python
@strawberry.type
class Note:
    id: int
    title: str
    content: str | None
    is_published: bool
    created_at: datetime
    updated_at: datetime

@strawberry.type  
class HealthStatus:
    status: str
    timestamp: str
    api: ServiceStatus
    database: DatabaseStatus
```

#### Queries

```graphql
type Query {
  # Health checks
  health: HealthStatus!
  
  # Notes
  notes: [Note!]!
  note(id: Int!): Note
}
```

**Example Queries:**

```graphql
# Get all notes
query GetNotes {
  notes {
    id
    title
    content
    is_published
    created_at
    updated_at
  }
}

# Get single note
query GetNote($id: Int!) {
  note(id: $id) {
    id
    title
    content
    is_published
  }
}

# Health check
query HealthCheck {
  health {
    status
    api {
      status
    }
    database {
      status
      connection
    }
  }
}
```

#### Mutations

```graphql
type Mutation {
  createNote(input: CreateNoteInput!): Note!
  updateNote(id: Int!, input: UpdateNoteInput!): Note
  deleteNote(id: Int!): Boolean!
}
```

**Example Mutations:**

```graphql
# Create note
mutation CreateNote($input: CreateNoteInput!) {
  createNote(input: $input) {
    id
    title
    content
    is_published
  }
}

# Update note
mutation UpdateNote($id: Int!, $input: UpdateNoteInput!) {
  updateNote(id: $id, input: $input) {
    id
    title
    content
    is_published
  }
}

# Delete note
mutation DeleteNote($id: Int!) {
  deleteNote(id: $id)
}
```

## REST Endpoints

### Health Check

- **GET** `/api/health`
- **Response**: `{"ok": true}`

## API Architecture

The API is organized using a modular pattern:

- **Types** (`apps/api/types/`): Strawberry GraphQL type definitions
- **Schemas** (`apps/api/schemas/`): Query and mutation definitions  
- **Resolvers** (`apps/api/resolvers/`): Business logic implementation
- **Models** (`apps/api/models/`): SQLAlchemy database models
- **Entry Point**: `apps/api/index.py` exports FastAPI app

## Authentication

Currently using basic setup. To implement authentication:

1. Add authentication middleware to FastAPI
2. Integrate with Supabase Auth
3. Use JWT tokens from frontend
4. Implement user context in GraphQL resolvers

## Error Handling

GraphQL errors are automatically formatted by Strawberry. Custom error handling can be added through:

- Field-level error handling in resolvers
- Global exception handlers in FastAPI
- Validation errors for input types
