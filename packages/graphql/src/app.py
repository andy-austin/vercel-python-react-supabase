from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List

@strawberry.type
class User:
    id: str
    email: str
    name: str | None = None

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL!"
    
    @strawberry.field
    def users(self) -> List[User]:
        return [
            User(id="1", email="user@example.com", name="Test User")
        ]

@strawberry.type
class Mutation:
    @strawberry.field
    def create_user(self, email: str, name: str | None = None) -> User:
        return User(id="new", email=email, name=name)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="GraphQL API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="")

@app.get("/")
def read_root():
    return {"message": "GraphQL API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}