#!/bin/bash
# Start backend server

set -e

cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Start server
echo "Starting backend server..."
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
