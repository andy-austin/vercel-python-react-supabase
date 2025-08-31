# Development Guide

## Local Development Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm 8.15.6+

### Quick Start

```bash
# Install Node.js dependencies
pnpm install

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Install Python dependencies
cd packages/graphql && pnpm py:install && cd ../..

# Start all services
pnpm dev
```

This starts:

- Next.js dev server on <http://localhost:3000>
- FastAPI GraphQL server on <http://localhost:8000>

## Development Workflows

### Adding New Features

1. Determine which package the feature belongs to
2. Update shared types in `packages/shared` if needed
3. Implement frontend in `apps/web`
4. Add GraphQL schema/resolvers in `packages/graphql`
5. Update database schema and regenerate types if needed

### Working with Types

- Database types: Run `pnpm gen-types` in `packages/db`
- Shared types: Add to `packages/shared/src/types/index.ts`
- GraphQL types: Define Strawberry types in Python API

### Testing

- Frontend: Tests run with Next.js testing framework
- Python API: pytest in `packages/graphql/tests/`
- Run all tests: `pnpm test` from root

### Code Quality

#### Linting Commands

```bash
# Root level (all packages)
pnpm lint         # Check all code (ESLint + flake8)
pnpm lint:fix     # Auto-fix issues (ESLint --fix + black + isort)
pnpm typecheck    # Type checking (TypeScript + mypy)

# Package-specific
cd packages/graphql
pnpm py:lint      # Python linting with flake8
pnpm py:lint:fix  # Format Python code with black + isort
pnpm py:typecheck # Python type checking with mypy
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
- **Import errors**: Verify workspace dependencies in package.json files
- **Python dependency issues**: Use `uv sync` to reset Python environment
