#!/bin/bash
# Script to run Bats tests with coverage using kcov

set -e

# Create coverage directory
COVERAGE_DIR="coverage"
mkdir -p "$COVERAGE_DIR"

# Function to run a command with a timeout and proper error handling
run_with_timeout() {
  local cmd="$1"
  local timeout_seconds="$2"
  local description="$3"
  
  echo "Running $description..."
  if ! timeout "$timeout_seconds" bash -c "$cmd"; then
    exit_code=$?
    if [ $exit_code -eq 124 ]; then
      echo "Error: $description timed out after $timeout_seconds seconds."
      return 124
    else
      echo "Warning: Error running $description. Exit code: $exit_code"
      return $exit_code
    fi
  fi
  return 0
}

# Check if kcov is installed
if ! command -v kcov >/dev/null 2>&1; then
  echo "Error: kcov is required but not installed."
  echo "Please install kcov and try again."
  echo "  - Ubuntu/Debian: apt-get install libdw-dev binutils-dev libcurl4-openssl-dev zlib1g-dev libiberty-dev cmake"
  echo "  - Then: git clone https://github.com/SimonKagstrom/kcov.git && cd kcov && mkdir build && cd build && cmake .. && make && make install"
  echo "  - macOS: brew install kcov"
  exit 1
fi

# First run kcov directly on the install script to get its coverage
if ! run_with_timeout "kcov --include-pattern=install-minimal.sh $COVERAGE_DIR ./scripts/install-minimal.sh" 30 "coverage for install script"; then
  if [ $? -eq 124 ]; then
    echo "Aborting due to timeout."
    exit 1
  fi
  echo "Continuing with tests despite error..."
fi

# Then run coverage for Bats tests with a timeout
if ! run_with_timeout "kcov --include-pattern=install-minimal.sh $COVERAGE_DIR bats scripts/test/install-test.bats" 60 "coverage for Bats tests"; then
  if [ $? -eq 124 ]; then
    echo "Aborting due to timeout."
    exit 1
  fi
  echo "Coverage may be incomplete, but continuing..."
fi

# Merge coverage reports for better results
echo "Merging coverage reports..."
if ! run_with_timeout "kcov --merge $COVERAGE_DIR/kcov-merged $COVERAGE_DIR/*/" 30 "merging coverage reports"; then
  echo "Failed to merge coverage reports, but individual reports should still be available."
fi

echo "Coverage report generated in $COVERAGE_DIR"
echo "Open $COVERAGE_DIR/kcov-merged/index.html to view the merged report"
echo "Or view individual test reports in the coverage directory" 