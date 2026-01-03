#!/bin/bash
# Script to run Python tests with coverage

set -e

# Create coverage directory if it doesn't exist
COVERAGE_DIR="coverage"
mkdir -p "$COVERAGE_DIR"

# Check Python and dependencies
echo "Checking Python environment..."
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create and activate a virtual environment if it doesn't exist
VENV_DIR=".venv-vibesafe"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies in the virtual environment
echo "Installing test dependencies..."
python3 -m pip install pytest pytest-cov pyyaml python-frontmatter

# Run tests with coverage
echo "Running Python tests with coverage..."
python3 -m pytest tests/ --cov=scripts/ --cov-report=xml:$COVERAGE_DIR/python-coverage.xml --cov-report=html:$COVERAGE_DIR/python-html

# Deactivate virtual environment
deactivate

# Show summary
echo "Python tests completed."
echo "Coverage report generated in $COVERAGE_DIR/python-html/index.html" 