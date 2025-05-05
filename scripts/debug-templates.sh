#!/bin/bash
# Debug script to understand how the install script processes templates

# Store the original working directory
ORIGINAL_DIR="$(pwd)"

# Create test directory
TEST_DIR="$(mktemp -d)"
echo "Created test directory: $TEST_DIR"

# Create templates structure
echo "Creating templates directory structure..."
mkdir -p "$TEST_DIR/templates/backlog"
mkdir -p "$TEST_DIR/templates/cip"
mkdir -p "$TEST_DIR/templates/tenets"
mkdir -p "$TEST_DIR/templates/backlog/custom_subdirectory"

# Create test content
echo "# Custom Backlog" > "$TEST_DIR/templates/backlog/README.md"
echo "# Custom Subdirectory" > "$TEST_DIR/templates/backlog/custom_subdirectory/README.md"

# Create test workspace
WORKSPACE="$(mktemp -d)"
echo "Created workspace: $WORKSPACE"
cd "$WORKSPACE"

# Run the install script with debug
echo "Running install script with templates directory..."
VIBESAFE_DEBUG=true VIBESAFE_TEMPLATES_DIR="$TEST_DIR" bash "$ORIGINAL_DIR/scripts/install-minimal.sh"

# Check the results
echo ""
echo "Results:"
echo "--------"
echo "Checking directories:"
find . -type d | sort

echo ""
echo "Checking files:"
find . -type f | sort

echo ""
echo "Checking backlog README content:"
if [ -f "backlog/README.md" ]; then
  cat "backlog/README.md"
else
  echo "backlog/README.md does not exist"
fi

echo ""
echo "Checking custom subdirectory README content:"
if [ -f "backlog/custom_subdirectory/README.md" ]; then
  cat "backlog/custom_subdirectory/README.md"
else
  echo "backlog/custom_subdirectory/README.md does not exist"
fi

# Clean up
cd "$ORIGINAL_DIR"
rm -rf "$TEST_DIR" "$WORKSPACE" 