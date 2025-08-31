# Code Quality and Linting

This document describes the linting and code quality tools configured for the project.

## Overview

The project uses different linting tools for different languages:

- **TypeScript/JavaScript**: ESLint with TypeScript and React rules
- **Python**: flake8, black, isort, and mypy

## TypeScript/JavaScript Linting

### Configuration
- **Root config**: `.eslintrc.json` with base rules
- **Package configs**: Individual `.eslintrc.json` files that extend the root config
- **Rules**: TypeScript, React, and Next.js specific rules

### Commands
```bash
# Lint all TypeScript/JavaScript code
pnpm lint

# Auto-fix linting issues
pnpm lint:fix

# Package-specific linting
cd apps/web && pnpm lint
cd packages/shared && pnpm lint
cd packages/db && pnpm lint
```

### Rules Highlights
- No unused variables (with underscore prefix exception)
- React hooks rules enforced
- TypeScript strict mode recommended
- Next.js core web vitals rules

## Python Linting

### Tools Used
- **flake8**: Code linting and style checking
- **black**: Code formatting (88 character line limit)
- **isort**: Import sorting
- **mypy**: Static type checking

### Configuration Files
- `pyproject.toml`: Tool configurations for black, isort, mypy
- `.flake8`: Flake8 specific configuration
- Compatible with black formatting

### Commands
```bash
# Python linting
cd packages/graphql
pnpm py:lint      # Run flake8
pnpm py:lint:fix  # Format with black + isort
pnpm py:typecheck # Run mypy

# Root level (all packages)
pnpm lint         # Includes Python linting
pnpm lint:fix     # Includes Python formatting
pnpm typecheck    # Includes mypy
```

### Configuration Details

#### Black
- Line length: 88 characters
- Target Python version: 3.11+
- Excludes build directories and virtual environments

#### isort  
- Profile: "black" (compatible with black formatting)
- Multi-line output format: 3
- Line length: 88 characters

#### mypy
- Python version: 3.11
- Strict mode with comprehensive type checking
- Warns on unused configs and redundant casts

#### flake8
- Max line length: 88 (black compatible)
- Ignores black-incompatible warnings (E203, W503)
- Per-file ignores for `__init__.py` imports

## IDE Integration

### VS Code
Install these extensions:
- ESLint
- Prettier
- Python
- Pylance
- Black Formatter

### Settings
Add to your VS Code `settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  }
}
```

## Pre-commit Hooks

This project comes with pre-configured pre-commit hooks for automatic code quality checking.

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install hooks (done automatically when you run pnpm install)
pre-commit install

# Run hooks on all files manually
pre-commit run --all-files
```

### Available Approaches

#### 1. Husky + lint-staged (Node.js-based)
Automatically configured with the template:
- Runs on `git commit`
- Uses `lint-staged` to only check modified files
- Integrated with npm/pnpm workflow

#### 2. Pre-commit framework (Python-based)  
Configured in `.pre-commit-config.yaml`:
- More comprehensive hook ecosystem
- Language-agnostic
- Can be used with CI/CD

### Hooks Configured

**Python (packages/graphql):**
- `black` - Code formatting
- `isort` - Import sorting  
- `flake8` - Linting
- `mypy` - Static type checking

**TypeScript/JavaScript:**
- `eslint` - Linting with auto-fix
- Configured for React, Next.js, and TypeScript

**General:**
- Trailing whitespace removal
- End-of-file fixer
- YAML, JSON, TOML validation
- Merge conflict detection
- Large file prevention

## Troubleshooting

### Common Issues

1. **ESLint errors in workspace packages**
   - Ensure tsconfig.json paths are correct
   - Check that package dependencies are installed

2. **Python import errors in mypy**
   - Verify virtual environment is activated
   - Check that all dependencies are installed with `uv sync`

3. **Black and flake8 conflicts**
   - Use provided `.flake8` config which ignores black-incompatible rules
   - Always run `black` before `flake8`

### Reset Commands
```bash
# Reset Python environment
cd packages/graphql && rm -rf .venv && pnpm py:install

# Reset Node modules
rm -rf node_modules package-lock.json && pnpm install
```