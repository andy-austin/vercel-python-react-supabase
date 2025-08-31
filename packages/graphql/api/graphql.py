from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import sys
import os

# Add the src directory to Python path to import our app
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import schema

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Create FastAPI app for Vercel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="")

# Export handler for Vercel
handler = app