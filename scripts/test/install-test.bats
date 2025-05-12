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
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
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
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
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
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
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
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
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
  # Run the installation script with environment variable to skip cloning
  # This tests the fallback logic without modifying the script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that key directories and files were created
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -f "README.md" ]
  [ -f "backlog/README.md" ]
  [ -f "cip/README.md" ]
  [ -f "tenets/README.md" ]
}

@test "Installation script returns success status" {
  # Run the installation script and capture exit code
  # Correct the approach for setting environment variables with 'run'
  export VIBESAFE_SKIP_CLONE=true
  run bash "$INSTALL_SCRIPT"
  
  # Check exit status
  [ "$status" -eq 0 ]
  
  # Also check for success message in output
  [[ "$output" == *"VibeSafe has been successfully installed"* ]]
}

@test "Installation works with custom templates directory" {
  # Create directory structure for custom templates
  mkdir -p "$TEST_DIR/custom_templates"
  mkdir -p "$TEST_DIR/custom_templates/templates"
  mkdir -p "$TEST_DIR/custom_templates/templates/backlog"
  mkdir -p "$TEST_DIR/custom_templates/templates/cip"
  mkdir -p "$TEST_DIR/custom_templates/templates/tenets"
  
  # Create custom template files
  echo "# Custom Backlog System" > "$TEST_DIR/custom_templates/templates/backlog/README.md"
  echo "# Custom CIP System" > "$TEST_DIR/custom_templates/templates/cip/README.md"
  echo "# Custom Tenets System" > "$TEST_DIR/custom_templates/templates/tenets/README.md"
  
  # Run the script with the custom templates directory
  VIBESAFE_TEMPLATES_DIR="$TEST_DIR/custom_templates" bash "$INSTALL_SCRIPT"
  
  # Verify that the custom templates were used
  [ -f "backlog/README.md" ]
  [ -f "cip/README.md" ]
  [ -f "tenets/README.md" ]
  grep -q "Custom Backlog System" "backlog/README.md"
  grep -q "Custom CIP System" "cip/README.md"
  grep -q "Custom Tenets System" "tenets/README.md"
}

@test "Installation preserves custom directory structure" {
  # Create complete directory structure for custom templates
  mkdir -p "$TEST_DIR/custom_templates"
  mkdir -p "$TEST_DIR/custom_templates/templates"
  mkdir -p "$TEST_DIR/custom_templates/templates/backlog"
  mkdir -p "$TEST_DIR/custom_templates/templates/backlog/custom_subdirectory"
  mkdir -p "$TEST_DIR/custom_templates/templates/cip"
  mkdir -p "$TEST_DIR/custom_templates/templates/cip/examples"
  mkdir -p "$TEST_DIR/custom_templates/templates/tenets"
  
  # Create standard README files
  echo "# Custom Backlog System" > "$TEST_DIR/custom_templates/templates/backlog/README.md"
  echo "# Custom CIP System" > "$TEST_DIR/custom_templates/templates/cip/README.md"
  echo "# Custom Tenets System" > "$TEST_DIR/custom_templates/templates/tenets/README.md"
  
  # Create custom subdirectory files
  echo "# Custom Backlog Subdirectory" > "$TEST_DIR/custom_templates/templates/backlog/custom_subdirectory/README.md"
  echo "# Example CIP" > "$TEST_DIR/custom_templates/templates/cip/examples/example.md"
  
  # Run the script with the custom templates directory
  VIBESAFE_TEMPLATES_DIR="$TEST_DIR/custom_templates" bash "$INSTALL_SCRIPT"
  
  # Verify that the custom directory structure was preserved
  [ -d "backlog/custom_subdirectory" ]
  [ -d "cip/examples" ]
  [ -f "backlog/custom_subdirectory/README.md" ]
  [ -f "cip/examples/example.md" ]
  
  # Verify content was preserved
  grep -q "Custom Backlog Subdirectory" "backlog/custom_subdirectory/README.md"
  grep -q "Example CIP" "cip/examples/example.md"
}

@test "Installation works with debug output enabled" {
  # Run the installation script with debug output
  # Use correct approach for setting environment variables with 'run'
  export VIBESAFE_DEBUG=true
  export VIBESAFE_SKIP_CLONE=true
  run bash "$INSTALL_SCRIPT"
  
  # Check for debug output in the output
  [[ "$output" == *"[DEBUG]"* ]]
  
  # Check that installation still succeeded
  [ "$status" -eq 0 ]
}

@test "Installation handles non-existent repository gracefully" {
  # Run the installation script with a non-existent repository
  # Use a timeout to avoid hanging and the correct way to set env vars
  export VIBESAFE_REPO_URL="https://github.com/nonexistent/repo.git"
  run timeout 10 bash "$INSTALL_SCRIPT"
  
  # Check that installation completed (may not be success)
  [[ "$output" == *"VibeSafe has been successfully installed"* ]]
  
  # Check that key directories and files were created anyway
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -f "README.md" ]
}

@test "What's Next installation can be skipped using environment variable" {
  # Create scripts directory and add a mock whats_next.py
  mkdir -p scripts
  echo '#!/usr/bin/env python3' > scripts/whats_next.py
  echo 'print("This is a mock whats_next.py")' >> scripts/whats_next.py
  chmod +x scripts/whats_next.py
  
  # Run the installation with What's Next installation disabled
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=false
  run bash "$INSTALL_SCRIPT"
  
  # Check that installation completed successfully
  [ "$status" -eq 0 ]
  
  # Verify What's Next files were not created
  [ ! -f "whats-next" ]
  [ ! -f "install-whats-next.sh" ]
  [ ! -d ".venv" ]
}

@test "What's Next script is properly installed when Python is available" {
  # This test assumes Python 3 is available on the system running the tests
  
  # Create scripts directory and add a mock whats_next.py
  mkdir -p scripts
  echo '#!/usr/bin/env python3' > scripts/whats_next.py
  echo 'print("This is a mock whats_next.py")' >> scripts/whats_next.py
  chmod +x scripts/whats_next.py
  
  # Check if Python 3 is available, skip test if not
  if ! command -v python3 >/dev/null 2>&1; then
    skip "Python 3 is not available, skipping test"
  fi
  
  # Run the installation with What's Next installation enabled
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$INSTALL_SCRIPT"
  
  # Check that installation completed successfully
  [ "$status" -eq 0 ]
  
  # Verify What's Next files were created
  [ -f "whats-next" ]
  [ -f "install-whats-next.sh" ]
  [ -d ".venv" ]
  
  # Check that the wrapper script is executable
  [ -x "whats-next" ]
  
  # Check that the installation script mentions "What's Next" in the next steps
  [[ "$output" == *"Run the 'What's Next' script"* ]]
}

@test "What's Next installation handles missing python gracefully" {
  # Create scripts directory and add a mock whats_next.py
  mkdir -p scripts
  echo '#!/usr/bin/env python3' > scripts/whats_next.py
  echo 'print("This is a mock whats_next.py")' >> scripts/whats_next.py
  chmod +x scripts/whats_next.py
  
  # Create a wrapper script that wraps the install script and overrides the python3 command
  cat > "$TEST_DIR/mock_install.sh" << 'EOL'
#!/bin/bash
# Mock the python3 command to make it fail
function python3() {
  # This function will be called instead of the real python3
  # Make it fail when attempting to create a virtual environment
  if [[ "$*" == *"-m venv"* ]]; then
    return 1
  fi
  # Otherwise delegate to the real python3
  command python3 "$@"
}

# Export the function so it's available to the install script
export -f python3

# Run the original install script with our mocked python3
bash "$1"
EOL
  chmod +x "$TEST_DIR/mock_install.sh"
  
  # Run the mock installation script
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$TEST_DIR/mock_install.sh" "$INSTALL_SCRIPT"
  
  # Check that installation completed with a warning but still succeeded
  [ "$status" -eq 0 ]
  [[ "$output" == *"Warning: Failed to create virtual environment"* ]]
  
  # Verify basic installation still worked
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -f "README.md" ]
  
  # Verify What's Next files were not created due to the failure
  [ ! -d ".venv" ]
  [ ! -f "whats-next" ]
} 