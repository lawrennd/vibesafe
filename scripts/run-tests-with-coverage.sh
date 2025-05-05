#!/bin/bash
# Script to run Bats tests with coverage using kcov

set -e

# Create coverage directory
COVERAGE_DIR="coverage"
mkdir -p "$COVERAGE_DIR"

# Check if kcov is installed
if ! command -v kcov >/dev/null 2>&1; then
  echo "Error: kcov is required but not installed."
  echo "Please install kcov and try again."
  echo "  - Ubuntu/Debian: apt-get install kcov"
  echo "  - macOS: brew install kcov"
  exit 1
fi

# First run kcov directly on the install script to get its coverage
echo "Running coverage for install script..."
kcov --include-pattern=install-minimal.sh "$COVERAGE_DIR" ./scripts/install-minimal.sh

# Then run coverage for Bats tests
echo "Running coverage for Bats tests..."
# The below command might not work properly on all systems, as Bash script coverage is tricky
kcov --include-pattern=install-minimal.sh "$COVERAGE_DIR" bats scripts/test/install-test.bats

echo "Coverage report generated in $COVERAGE_DIR"
echo "Open $COVERAGE_DIR/index.html to view the report" 