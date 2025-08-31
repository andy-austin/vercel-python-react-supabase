# System Architecture

## Overview

Full-stack application combining React frontend with Python GraphQL API, deployed on Vercel with Supabase backend.

## Project Structure

```
vercel-python-react-supabase/
├── apps/
│   ├── api/           # FastAPI GraphQL API (Python 3.11+)
│   └── web/           # Next.js React frontend
├── docs/              # Project documentation
├── .venv/             # Python virtual environment
├── pyproject.toml     # Python dependencies and tool config
├── package.json       # Node.js workspace root
├── pnpm-workspace.yaml # pnpm workspace configuration
└── turbo.json         # Turbo build orchestration
```

## Components

### Frontend (apps/web)

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript with React 18
- **Deployment**: Vercel static site generation
- **Database**: Direct Supabase client integration
- **Dependencies**: Self-contained Next.js application

### GraphQL API (apps/api)

- **Framework**: FastAPI with Strawberry GraphQL
- **Runtime**: Python 3.11 serverless function on Vercel
- **Entry Point**: `apps/api/index.py` 
- **Endpoint**: `/api/graphql` (proxied via Vercel routing)
- **Features**: CORS enabled, GraphQL schema with models and resolvers
- **Database**: SQLAlchemy with Alembic migrations
- **Dependencies**: Managed via requirements.txt and virtual environment

### Database

- **Service**: Supabase PostgreSQL
- **Frontend Client**: @supabase/supabase-js (in apps/web)
- **Backend ORM**: SQLAlchemy with Alembic migrations (in apps/api)
- **Environment**: Requires `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Data Flow

1. Next.js frontend makes GraphQL requests to `/api/graphql`
2. Vercel routes requests to Python serverless function at `apps/api/index.py`
3. FastAPI + Strawberry processes GraphQL queries using resolvers
4. Python API uses SQLAlchemy models to interact with Supabase PostgreSQL
5. Frontend can also directly query Supabase for simple operations
6. TypeScript types ensure type safety across frontend and database
