# Development Guide

## Local Development Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm 8.15.6+

### Quick Start

#### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./setup.sh

# Start all services
pnpm dev
```

#### Option 2: Manual Setup
```bash
# Install Node.js dependencies
pnpm install

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create virtual environment and install Python dependencies
uv venv .venv
uv pip install -r apps/api/requirements.txt --python .venv/bin/python

# Start all services
pnpm dev
```

This starts:

- Next.js dev server on <http://localhost:3000>
- FastAPI GraphQL server on <http://localhost:8000>

## Development Workflows

### Adding New Features

1. Implement frontend changes in `apps/web`
2. Add GraphQL schema/resolvers in `apps/api`
3. Update database schema in Supabase if needed
4. Run linting and type checking before committing

### Working with Types

- Database types: Configure Supabase client directly in `apps/web`
- GraphQL types: Define Strawberry types in `apps/api/schema.py`
- Frontend types: Add TypeScript types directly in relevant components

### Testing

- Frontend: Tests run with Next.js testing framework
- Python API: Tests in `apps/api/` (when implemented)
- Run all tests: `pnpm test` from root

### Code Quality

#### Linting Commands

```bash
# Root level (all packages)
pnpm lint         # Check all code (ESLint + flake8)
pnpm lint:fix     # Auto-fix issues (ESLint --fix + black + isort)
pnpm typecheck    # Type checking (TypeScript + mypy)

# Python API specific
cd apps/api
# Activate virtual environment first:
source ../../.venv/bin/activate
python -m flake8 .     # Python linting
python -m black .      # Format Python code
python -m isort .      # Sort imports
```

#### Linter Configurations

- **ESLint**: Configured for TypeScript + React with Next.js rules
- **flake8**: Python linting with black compatibility
- **black**: Python code formatting (88 char line length)
- **isort**: Python import sorting
- **mypy**: Python static type checking

## Debugging

### Common Issues

- **CORS errors**: Check FastAPI CORS middleware configuration
- **Type errors**: Ensure Supabase types are up to date
- **Import errors**: Check workspace configuration in pnpm-workspace.yaml
- **Python dependency issues**: Recreate .venv with `rm -rf .venv && ./setup.sh`
