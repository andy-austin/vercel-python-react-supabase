from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import sys
import os

# Add the packages/graphql/src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'packages', 'graphql', 'src'))

from app import schema

# Create the GraphQL router directly as the app
graphql_app = GraphQLRouter(schema)

# Add CORS middleware to the GraphQL router
graphql_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Export handler for Vercel  
handler = graphql_app