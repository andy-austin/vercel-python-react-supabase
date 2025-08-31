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

- **`pyproject.toml`**: Unified configuration for black, isort, and flake8
- **`.pre-commit-config.yaml`**: Pre-commit hook configurations
- All tools configured for black compatibility and 88-character line length

### Commands

```bash
# Python linting (manual)
cd apps/api
source ../../.venv/bin/activate
python -m flake8 .     # Run flake8
python -m black .      # Format with black
python -m isort .      # Sort imports
python -m mypy . || true  # Type checking

# Root level (all packages)
pnpm lint         # Includes Python linting via pre-commit
pnpm lint:fix     # Auto-fix issues where possible
pnpm typecheck    # TypeScript type checking
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
- Known first party: ["schema"] for local imports
- Sections: FUTURE, STDLIB, THIRDPARTY, FIRSTPARTY, LOCALFOLDER

#### mypy

- Python version: 3.11
- Strict mode with comprehensive type checking
- Warns on unused configs and redundant casts

#### flake8

- Max line length: 88 (black compatible)
- Extends ignore: ["E203", "W503"] for black compatibility
- Excludes: [".git", "__pycache__", ".venv", "build", "dist"]

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
# Install pre-commit (done automatically by setup.sh)
uv tool install pre-commit

# Install hooks (done automatically by setup.sh)
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

**Python (apps/api):**

- `black` - Code formatting (88 char line length)
- `isort` - Import sorting with black profile
- `flake8` - Linting with black compatibility

**Note**: ESLint hooks removed from pre-commit to reduce complexity. Use `pnpm lint` for JavaScript/TypeScript linting.

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
rm -rf .venv && ./setup.sh

# Reset Node modules
rm -rf node_modules pnpm-lock.yaml && pnpm install

# Reset pre-commit
pre-commit clean && pre-commit install
```
