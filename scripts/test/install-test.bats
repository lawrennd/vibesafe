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

@test "Installation preserves existing README.md" {
  # Create an existing README.md with unique content
  echo "# Existing Project" > README.md
  echo "This is a custom README that should be preserved." >> README.md
  
  # Store the checksum of the original README
  README_CHECKSUM=$(md5sum README.md | awk '{print $1}')
  
  # Run the installation script
  bash "$INSTALL_SCRIPT"
  
  # Check that README.md still has the original content
  [ -f "README.md" ]
  
  # Verify checksum to ensure file wasn't modified
  NEW_CHECKSUM=$(md5sum README.md | awk '{print $1}')
  [ "$README_CHECKSUM" = "$NEW_CHECKSUM" ]
  
  # Also verify original text is present
  grep -q "Existing Project" "README.md"
  grep -q "custom README" "README.md"
}

@test "Installation works when templates directory is missing" {
  # Create a mock repo without templates
  MOCK_REPO="$(mktemp -d)"
  
  # Initialize a git repo
  git init "$MOCK_REPO"
  
  # Create a minimal README
  echo "# Mock Repo" > "$MOCK_REPO/README.md"
  
  # Create a modified version of the install script
  MODIFIED_SCRIPT="${TEST_DIR}/install-modified.sh"
  cp "$INSTALL_SCRIPT" "$MODIFIED_SCRIPT"
  
  # Update the script to use our mock repo instead of the actual repo
  sed -i.bak "s|REPO_URL=\"https://github.com/lawrennd/vibesafe.git\"|REPO_URL=\"file://$MOCK_REPO\"|g" "$MODIFIED_SCRIPT"
  
  # Run the modified installation script
  bash "$MODIFIED_SCRIPT"
  
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