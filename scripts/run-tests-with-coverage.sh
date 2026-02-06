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

# Run Python tests if they exist
# VibeSafe dogfoods: canonical tooling lives under templates/, and runtime copies
# may not be present in this repository checkout.
if [ -d "tests" ] && [ -f "templates/scripts/whats_next.py" ]; then
  echo "Running Python tests..."
  # Make the script executable if it exists but isn't executable
  if [ -f "scripts/run-python-tests.sh" ]; then
    chmod +x scripts/run-python-tests.sh
    ./scripts/run-python-tests.sh
  else
    # If the script doesn't exist, run the tests directly using virtual environment
    if command -v python3 >/dev/null 2>&1; then
      # Create and activate a virtual environment if it doesn't exist
      VENV_DIR=".venv-vibesafe"
      if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
      fi
      
      echo "Activating virtual environment..."
      source "$VENV_DIR/bin/activate"
      
      # Install dependencies in the virtual environment
      python3 -m pip install --quiet pytest pytest-cov pyyaml python-frontmatter

      # Coverage: focus on canonical template code (templates/)
      python3 -m pytest tests/ --cov=templates --cov-report=xml:$COVERAGE_DIR/python-coverage.xml
      
      # Deactivate virtual environment
      deactivate
    else
      echo "Python 3 not found, skipping Python tests"
    fi
  fi
fi

# Merge coverage reports for better results
echo "Merging coverage reports..."
if ! run_with_timeout "kcov --merge $COVERAGE_DIR/kcov-merged $COVERAGE_DIR/*/" 30 "merging coverage reports"; then
  echo "Failed to merge coverage reports, but individual reports should still be available."
fi

echo "Coverage report generated in $COVERAGE_DIR"
echo "Open $COVERAGE_DIR/kcov-merged/index.html to view the merged report"
echo "Or view individual test reports in the coverage directory" 