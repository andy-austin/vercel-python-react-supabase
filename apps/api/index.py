from starlette.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from schema import schema

# Create GraphQL ASGI app
graphql_app = GraphQL(schema)

# Wrap with CORS middleware
app = CORSMiddleware(
    graphql_app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Export handler for Vercel
handler = app
