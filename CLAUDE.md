# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a monorepo using **pnpm workspaces** and **Turbo** for build orchestration, combining React, Python, and Supabase technologies for Vercel deployment.

### Structure Overview

- **apps/web**: Next.js React frontend application
- **packages/shared**: Shared TypeScript utilities, types, and React components used across apps
- **packages/db**: Supabase client configuration and type definitions  
- **packages/graphql**: FastAPI Python GraphQL API using Strawberry GraphQL

### Key Technologies

- **Frontend**: Next.js 14, React 18, TypeScript
- **Backend**: FastAPI with Strawberry GraphQL, Python 3.11+
- **Database**: Supabase with generated TypeScript types
- **Deployment**: Vercel (hybrid Next.js + Python serverless functions)
- **Package Management**: pnpm with workspace dependencies

## Development Commands

### Root Level Commands (uses Turbo)
```bash
pnpm dev          # Start all services in development mode
pnpm build        # Build all packages and apps
pnpm lint         # Lint all TypeScript and Python code
pnpm test         # Run all tests (TypeScript and Python)
pnpm clean        # Clean all build artifacts
```

### Package-Specific Commands

#### Next.js Web App (apps/web)
```bash
cd apps/web
pnpm dev          # Start Next.js dev server (port 3000)
pnpm build        # Build for production
pnpm lint         # ESLint + Next.js linting
pnpm type-check   # TypeScript type checking
```

#### Python GraphQL API (packages/graphql)
```bash
cd packages/graphql
pnpm py:install   # Install Python dependencies with uv
pnpm py:dev       # Start FastAPI dev server (port 8000)
pnpm py:test      # Run pytest tests
pnpm py:lint      # Run flake8 linting
pnpm py:typecheck # Run mypy type checking
```

#### Supabase Package (packages/db)
```bash
cd packages/db
pnpm gen-types    # Generate TypeScript types from Supabase schema
```

## Deployment Configuration

### Vercel Setup
- Main build targets Next.js app in `apps/web`
- Python GraphQL API deployed as serverless function
- Routes `/api/graphql/*` proxy to Python function
- Requires `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` environment variables

### Python Dependencies
Uses **uv** for fast Python dependency management. Python code requires Python 3.11+ with FastAPI, Strawberry GraphQL, and Supabase client.

## Workspace Dependencies
The web app imports shared packages using workspace protocol:
- `shared`: Common utilities, types, and React components
- `db`: Supabase client and database types

Always use workspace dependencies rather than duplicating code across packages.

## Documentation

The `docs/` folder contains detailed project documentation:

- **docs/architecture.md**: System architecture and component relationships
- **docs/development.md**: Development workflows, debugging, and local setup
- **docs/deployment.md**: Deployment processes and Vercel configuration
- **docs/README.md**: Documentation overview and file descriptions

Reference these files for detailed context when working on specific aspects of the project. The documentation provides deeper technical details beyond this high-level overview.