#!/bin/bash

# Helper script to run Python linting on staged files
# Usage: ./scripts/lint-python.sh <tool> <files...>

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <tool> <file1> [file2...]"
    exit 1
fi

TOOL=$1
shift

# Export PATH to include uv
export PATH="$HOME/.local/bin:$PATH"

# Change to graphql directory
cd packages/graphql

# Convert absolute paths to relative paths within graphql directory
RELATIVE_FILES=()
for file in "$@"; do
    # Remove the packages/graphql/ prefix if it exists
    relative_file="${file#packages/graphql/}"
    RELATIVE_FILES+=("$relative_file")
done

# Run the appropriate tool with the relative file paths
case "$TOOL" in
    "black")
        uv run --no-sync black "${RELATIVE_FILES[@]}"
        ;;
    "isort")
        uv run --no-sync isort "${RELATIVE_FILES[@]}"
        ;;
    "flake8")
        uv run --no-sync flake8 "${RELATIVE_FILES[@]}"
        ;;
    *)
        echo "Unknown tool: $TOOL"
        exit 1
        ;;
esac