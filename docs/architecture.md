# System Architecture

## Overview

Full-stack application combining React frontend with Python GraphQL API, deployed on Vercel with Supabase backend.

## Components

### Frontend (apps/web)

- **Framework**: Next.js 14 with App Router
- **Deployment**: Vercel static site generation
- **Dependencies**: Imports `shared` and `db` workspace packages

### GraphQL API (packages/graphql)

- **Framework**: FastAPI with Strawberry GraphQL
- **Runtime**: Python 3.11 serverless function on Vercel
- **Endpoint**: `/api/graphql` (proxied via Vercel routing)
- **Features**: CORS enabled, basic User queries/mutations

### Database (packages/db)

- **Service**: Supabase PostgreSQL
- **Client**: @supabase/supabase-js
- **Types**: Generated TypeScript definitions in `supabase/types.ts`
- **Environment**: Requires `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Shared Code (packages/shared)

- **Purpose**: Common utilities, types, and React components
- **Structure**: Modular exports for utils, types, components
- **Usage**: Imported by web app and potentially other packages

## Data Flow

1. Next.js frontend makes GraphQL requests to `/api/graphql`
2. Vercel routes to Python serverless function
3. FastAPI + Strawberry processes GraphQL queries
4. Python API can interact with Supabase for data persistence
5. TypeScript types ensure type safety across frontend and database
