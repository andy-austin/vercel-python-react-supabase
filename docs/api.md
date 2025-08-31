# API Documentation

## GraphQL API

The FastAPI GraphQL API provides data access through Strawberry GraphQL schema.

### Endpoint

- **Development**: <http://localhost:8000/graphql>
- **Production**: <https://your-app.vercel.app/api/graphql>

### Schema

#### Types

```python
@strawberry.type
class User:
    id: str
    email: str
    name: str | None = None
```

#### Queries

```graphql
type Query {
  hello: String!
  users: [User!]!
}
```

**Example Query:**

```graphql
query GetUsers {
  users {
    id
    email
    name
  }
}
```

#### Mutations

```graphql
type Mutation {
  createUser(email: String!, name: String): User!
}
```

**Example Mutation:**

```graphql
mutation CreateUser($email: String!, $name: String) {
  createUser(email: $email, name: $name) {
    id
    email
    name
  }
}
```

## REST Endpoints

### Health Check

- **GET** `/health`
- **Response**: `{"status": "healthy"}`

### Root

- **GET** `/`
- **Response**: `{"message": "GraphQL API is running"}`

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
