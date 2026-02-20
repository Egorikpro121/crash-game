#!/bin/bash
# Test script for running all tests

set -e

echo "=== Running Backend Tests ==="
cd "$(dirname "$0")/.."

# Set test environment
export SECRET_KEY="test-secret-key-for-testing-only"
export DATABASE_URL="sqlite:///./test.db"

# Run tests
python3 -m pytest tests/ -v --tb=short

echo "=== Tests Complete ==="
