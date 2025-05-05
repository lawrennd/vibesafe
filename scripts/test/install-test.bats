#!/usr/bin/env bats

setup() {
  # Create a temporary directory for testing
  TEST_DIR="$(mktemp -d)"
  
  # Store the original working directory
  ORIGINAL_DIR="$(pwd)"
  
  # Store the path to the install script
  INSTALL_SCRIPT="${ORIGINAL_DIR}/scripts/install-minimal.sh"
  
  # Navigate to the test directory
  cd "$TEST_DIR"
}

teardown() {
  # Return to original directory
  cd "$ORIGINAL_DIR"
  
  # Clean up the test directory
  rm -rf "$TEST_DIR"
}

@test "Installation script exists and is executable" {
  [ -f "$INSTALL_SCRIPT" ]
  [ -x "$INSTALL_SCRIPT" ]
}

@test "Installation creates required directories" {
  # Run the installation script
  bash "$INSTALL_SCRIPT"
  
  # Check that key directories were created
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -d "backlog/documentation" ]
  [ -d "backlog/features" ]
  [ -d "backlog/infrastructure" ]
  [ -d "backlog/bugs" ]
}

@test "Installation creates required template files" {
  # Run the installation script
  bash "$INSTALL_SCRIPT"
  
  # Check that key template files were created
  [ -f "cip/README.md" ]
  [ -f "cip/cip_template.md" ]
  [ -f "backlog/README.md" ]
  [ -f "backlog/task_template.md" ]
  [ -f "tenets/README.md" ]
  [ -f "tenets/tenet_template.md" ]
}

@test "Installation creates project README.md" {
  # Run the installation script
  bash "$INSTALL_SCRIPT"
  
  # Check that README.md exists and contains expected content
  [ -f "README.md" ]
  grep -q "VibeSafe" "README.md"
  grep -q "Project Structure" "README.md"
  grep -q "Getting Started" "README.md"
}

@test "Installation works when templates directory is missing" {
  # Create a mock repo without templates
  MOCK_REPO="$(mktemp -d)"
  
  # Initialize a git repo
  git init "$MOCK_REPO"
  
  # Create a minimal README
  echo "# Mock Repo" > "$MOCK_REPO/README.md"
  
  # Mock the git clone by temporarily overriding the git function
  git() {
    if [[ "$1" == "clone" ]]; then
      cp -r "$MOCK_REPO/." "$3"
      return 0
    else
      command git "$@"
    fi
  }
  export -f git
  
  # Run the installation script
  bash "$INSTALL_SCRIPT"
  
  # Check that key directories and files were still created
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -f "README.md" ]
  
  # Clean up
  rm -rf "$MOCK_REPO"
}

@test "Installation script returns success status" {
  # Run the installation script and capture exit code
  run bash "$INSTALL_SCRIPT"
  
  # Check exit status
  [ "$status" -eq 0 ]
  
  # Also check for success message in output
  [[ "$output" == *"VibeSafe has been successfully installed"* ]]
} 