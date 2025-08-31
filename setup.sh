#!/bin/bash

echo "🚀 Setting up development environment..."

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
pnpm install

# Set up uv and Python dependencies
echo "🐍 Setting up Python environment..."
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create or activate virtual environment in root
echo "Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    echo "Creating .venv in root directory..."
    uv venv .venv
else
    echo ".venv already exists"
fi

# Install Python dependencies from apps/api/requirements.txt
if [ -f "apps/api/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    uv pip install -r apps/api/requirements.txt --python .venv/bin/python
    echo "✅ Python dependencies installed in .venv!"
else
    echo "⚠️  No requirements.txt found in apps/api/"
fi

# Set up pre-commit hooks (optional)
echo "🔧 Setting up pre-commit hooks..."
if command -v python3 &> /dev/null; then
    if ! command -v pre-commit &> /dev/null; then
        echo "Installing pre-commit..."
        uv tool install pre-commit
    fi

    echo "Installing pre-commit hooks..."
    pre-commit install

    echo "✅ Pre-commit hooks installed!"
else
    echo "⚠️  Python not found. Skipping pre-commit setup."
    echo "   You can install it later with: uv tool install pre-commit && pre-commit install"
fi

# Test linting
echo "🧪 Testing linting configuration..."
pnpm lint
echo "✅ Linting test passed!"

echo ""
echo "🎉 Setup complete! You're ready to develop."
echo ""
echo "Quick commands:"
echo "  pnpm dev          - Start development servers"
echo "  pnpm lint         - Run all linters"
echo "  pnpm lint:fix     - Fix linting issues"
echo "  pnpm test         - Run tests"
echo "  pnpm typecheck    - Check types"
echo ""
echo "Pre-commit hooks will run automatically on commit."
echo "Run 'pre-commit run --all-files' to check all files manually."
