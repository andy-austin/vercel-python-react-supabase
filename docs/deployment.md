# Deployment Guide

## Vercel Configuration

### Main App Deployment

- **Build Command**: `cd apps/web && npm run build`
- **Output Directory**: `apps/web/.next`
- **Framework**: Next.js (auto-detected)

### Python API Deployment

- **Runtime**: python3.11
- **Function**: `apps/api/index.py`
- **Routes**:
  - `/api/graphql/*` → Python serverless function
  - GraphQL endpoint available at `/api/graphql`

### Environment Variables

Required in Vercel dashboard:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Build Process

### Frontend Build

1. Turbo builds shared packages first
2. Next.js builds web app with workspace dependencies
3. Static files generated in `apps/web/.next`

### Python Build

1. Dependencies installed from `apps/api/requirements.txt`
2. FastAPI app at `apps/api/index.py` becomes serverless function
3. Vercel handles Python runtime automatically

## Monitoring

### Health Checks

- Frontend: Standard Next.js health
- API: `/api/health` endpoint returns `{"ok": true}`
- GraphQL: `/api/graphql` provides GraphQL endpoint

### Logs

- Vercel Function Logs: Monitor Python API performance
- Next.js Logs: Frontend build and runtime logs
- Database: Supabase dashboard for query performance

## Production Considerations

### Performance

- Next.js automatic static optimization
- Python cold starts on Vercel (consider warming strategies)
- Supabase connection pooling for database efficiency

### Security

- CORS configured for production domains
- Supabase RLS (Row Level Security) for data protection
- Environment variables for sensitive configuration
