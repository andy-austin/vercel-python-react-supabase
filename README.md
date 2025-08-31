# vercel-python-react-supabase

A full-stack monorepo template combining React, Python, and Supabase, optimized for Vercel deployment. Features a Next.js frontend with a FastAPI GraphQL backend, organized using pnpm workspaces and Turbo for efficient development.

## ✨ Features

- **Frontend**: Next.js 14 with TypeScript and React 18
- **Backend**: FastAPI with Strawberry GraphQL (Python 3.11+)
- **Database**: Supabase PostgresSQL with generated TypeScript types
- **Deployment**: Vercel with hybrid Next.js + Python serverless functions
- **Monorepo**: pnpm workspaces with Turbo build orchestration
- **Type Safety**: End-to-end TypeScript integration

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm 8.15.6+

### Installation

#### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd vercel-python-react-supabase

# Run the setup script
./setup-hooks.sh
```

#### Option 2: Manual Setup

```bash
# Clone the repository
git clone <repository-url>
cd vercel-python-react-supabase

# Install Node.js dependencies
pnpm install

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on macOS: brew install uv
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add uv to PATH (for current session)
export PATH="$HOME/.local/bin:$PATH"
# Or restart your shell, or add to your shell profile (.bashrc, .zshrc, etc.)

# Install Python dependencies
cd packages/graphql && pnpm py:install && cd ../..

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Environment Setup

Copy the example environment file and configure your Supabase credentials:

```bash
cp .env.local.example .env.local
```

Then edit `.env.local` with your Supabase project details:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

Get these values from your [Supabase project dashboard](https://app.supabase.com).

### Development

```bash
# Start all services in development mode
pnpm dev
```

This will start:
- Next.js frontend: http://localhost:3000
- FastAPI GraphQL API: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql

## 📁 Project Structure

```
├── apps/
│   └── web/                 # Next.js frontend application
├── packages/
│   ├── shared/              # Shared utilities, types, and components
│   ├── db/                  # Supabase client and type definitions
│   └── graphql/             # FastAPI GraphQL API
├── docs/                    # Detailed project documentation
├── CLAUDE.md               # AI assistant guidance
└── turbo.json              # Turbo build configuration
```

## 🛠 Development Commands

### Root Level (Turbo)
```bash
pnpm dev          # Start all services
pnpm build        # Build all packages and apps
pnpm lint         # Lint all code (ESLint + flake8)
pnpm lint:fix     # Fix linting issues (ESLint --fix + black + isort)
pnpm test         # Run all tests
pnpm typecheck    # Run TypeScript and mypy type checking
pnpm clean        # Clean build artifacts
```

### Package-Specific
```bash
# Next.js (apps/web)
cd apps/web
pnpm type-check   # TypeScript checking

# Python API (packages/graphql)
cd packages/graphql
pnpm py:test      # Run pytest
pnpm py:lint      # Run flake8
pnpm py:lint:fix  # Format with black and isort
pnpm py:typecheck # Run mypy

# Database (packages/db)
cd packages/db
pnpm gen-types    # Generate Supabase types
```

## 🚢 Deployment

### Vercel Setup

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Environment Variables

Required in Vercel:
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 📚 Documentation

Detailed documentation is available in the [`docs/`](./docs/) folder:

- [Architecture](./docs/architecture.md) - System design and component relationships
- [Development](./docs/development.md) - Workflows, debugging, and setup  
- [Deployment](./docs/deployment.md) - Vercel configuration and monitoring
- [API](./docs/api.md) - GraphQL schema and endpoint documentation
- [Database](./docs/database.md) - Supabase setup and type generation
- [Linting](./docs/linting.md) - Code quality tools and configurations

## 🏗 Architecture Overview

- **Frontend**: Next.js app consuming GraphQL API
- **API**: FastAPI with Strawberry GraphQL deployed as Vercel function
- **Database**: Supabase PostgreSQL with generated TypeScript types
- **Routing**: `/api/graphql/*` proxied to Python serverless function
- **Packages**: Shared code organized as workspace dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting (`pnpm lint` and `pnpm test`)
5. Pre-commit hooks will automatically run on commit
6. Submit a pull request

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install hooks for this repository
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

**Hooks configured:**
- **Python**: black, isort, flake8, mypy
- **TypeScript/JavaScript**: ESLint with auto-fix
- **General**: trailing whitespace, end-of-file fixer, YAML/JSON validation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.