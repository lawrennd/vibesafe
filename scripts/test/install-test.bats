#!/usr/bin/env bats
# Tests for VibeSafe Clean Installation Philosophy (CIP-000E)
# Verifies: System files overwritten, User content preserved

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

@test "Clean installation creates required directories" {
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that key directories were created
  [ -d "cip" ]
  [ -d "backlog" ]
  [ -d "tenets" ]
  [ -d "ai-requirements" ]
  [ -d "backlog/documentation" ]
  [ -d "backlog/features" ]
  [ -d "backlog/infrastructure" ]
  [ -d "backlog/bugs" ]
}

@test "Clean installation creates all system template files" {
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that all system template files were created
  [ -f "cip/README.md" ]
  [ -f "cip/cip_template.md" ]
  [ -f "backlog/README.md" ]
  [ -f "backlog/task_template.md" ]
  [ -f "tenets/README.md" ]
  [ -f "tenets/tenet_template.md" ]
  [ -f "ai-requirements/README.md" ]
}

@test "System files contain expected VibeSafe content" {
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify system files contain VibeSafe-specific content
  grep -q "Backlog System" "backlog/README.md"
  grep -q "Code Improvement Proposals" "cip/README.md"
  grep -q "Tenets" "tenets/README.md"
  grep -q "AI-Assisted Requirements" "ai-requirements/README.md"
}

@test "PRESERVE: Project README.md created when missing" {
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that project README.md exists and contains expected content
  [ -f "README.md" ]
  grep -q "VibeSafe" "README.md"
  grep -q "Project Structure" "README.md"
  grep -q "Getting Started" "README.md"
}

@test "PRESERVE: Existing project README.md is never touched" {
  # Create an existing README.md with unique content
  echo "# Existing Project" > README.md
  echo "This is a custom README that should be preserved." >> README.md
  echo "Last modified: $(date)" >> README.md
  
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

@test "PRESERVE: Existing user tasks are never overwritten" {
  # Create some existing user tasks
  mkdir -p backlog/features
  echo "# Task: User Created Task" > "backlog/features/2025-07-26_user-task.md"
  echo "This is user content that should be preserved." >> "backlog/features/2025-07-26_user-task.md"
  
  # Store checksum
  TASK_CHECKSUM=$(md5sum "backlog/features/2025-07-26_user-task.md" | awk '{print $1}')
  
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify user task was preserved
  [ -f "backlog/features/2025-07-26_user-task.md" ]
  NEW_CHECKSUM=$(md5sum "backlog/features/2025-07-26_user-task.md" | awk '{print $1}')
  [ "$TASK_CHECKSUM" = "$NEW_CHECKSUM" ]
  grep -q "User Created Task" "backlog/features/2025-07-26_user-task.md"
}

@test "PRESERVE: Existing user CIPs are never overwritten" {
  # Create some existing user CIPs
  mkdir -p cip
  echo "# CIP-0001: User Created CIP" > "cip/cip0001.md"
  echo "This is user content that should be preserved." >> "cip/cip0001.md"
  
  # Store checksum
  CIP_CHECKSUM=$(md5sum "cip/cip0001.md" | awk '{print $1}')
  
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify user CIP was preserved
  [ -f "cip/cip0001.md" ]
  NEW_CHECKSUM=$(md5sum "cip/cip0001.md" | awk '{print $1}')
  [ "$CIP_CHECKSUM" = "$NEW_CHECKSUM" ]
  grep -q "User Created CIP" "cip/cip0001.md"
}

@test "PRESERVE: Virtual environment is preserved if exists" {
  # Create a mock virtual environment
  mkdir -p .venv/bin
  echo "#!/bin/bash" > .venv/bin/python
  echo "echo 'Mock Python'" >> .venv/bin/python
  chmod +x .venv/bin/python
  
  # Store checksum
  VENV_CHECKSUM=$(md5sum ".venv/bin/python" | awk '{print $1}')
  
  # Run the installation script  
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify .venv was preserved
  [ -f ".venv/bin/python" ]
  NEW_CHECKSUM=$(md5sum ".venv/bin/python" | awk '{print $1}')
  [ "$VENV_CHECKSUM" = "$NEW_CHECKSUM" ]
}

@test "OVERWRITE: System files are always updated on reinstall" {
  # Run initial installation
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Modify a system file to simulate old version
  echo "# Old VibeSafe System File" > "backlog/README.md"
  echo "This should be overwritten." >> "backlog/README.md"
  
  # Store checksum to verify it changes
  OLD_CHECKSUM=$(md5sum "backlog/README.md" | awk '{print $1}')
  
  # Run installation again (reinstall)
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify system file was overwritten
  [ -f "backlog/README.md" ]
  NEW_CHECKSUM=$(md5sum "backlog/README.md" | awk '{print $1}')
  [ "$OLD_CHECKSUM" != "$NEW_CHECKSUM" ]
  
  # Verify it now contains proper VibeSafe content
  grep -q "Backlog System" "backlog/README.md"
  ! grep -q "Old VibeSafe System File" "backlog/README.md"
}

@test "OVERWRITE: Template files are always updated on reinstall" {
  # Run initial installation
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Modify template files to simulate old versions
  echo "# Old Template" > "backlog/task_template.md"
  echo "# Old CIP Template" > "cip/cip_template.md"
  
  # Run installation again
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Verify templates were overwritten with proper content
  [ -f "backlog/task_template.md" ]
  [ -f "cip/cip_template.md" ]
  ! grep -q "Old Template" "backlog/task_template.md"
  ! grep -q "Old CIP Template" "cip/cip_template.md"
}

@test "Installation works with custom templates directory" {
  # Create directory structure for custom templates
  mkdir -p "$TEST_DIR/custom_templates"
  mkdir -p "$TEST_DIR/custom_templates/templates"
  mkdir -p "$TEST_DIR/custom_templates/templates/backlog"
  mkdir -p "$TEST_DIR/custom_templates/templates/cip"
  mkdir -p "$TEST_DIR/custom_templates/templates/tenets"
  
  # Create custom template files
  echo "# Custom Backlog System v2.0" > "$TEST_DIR/custom_templates/templates/backlog/README.md"
  echo "# Custom CIP System v2.0" > "$TEST_DIR/custom_templates/templates/cip/README.md"
  echo "# Custom Tenets System v2.0" > "$TEST_DIR/custom_templates/templates/tenets/README.md"
  
  # Run the script with the custom templates directory
  VIBESAFE_TEMPLATES_DIR="$TEST_DIR/custom_templates" bash "$INSTALL_SCRIPT"
  
  # Verify that the custom templates were used
  [ -f "backlog/README.md" ]
  [ -f "cip/README.md" ]
  [ -f "tenets/README.md" ]
  grep -q "Custom Backlog System v2.0" "backlog/README.md"
  grep -q "Custom CIP System v2.0" "cip/README.md"
  grep -q "Custom Tenets System v2.0" "tenets/README.md"
}

@test "Installation script returns success status" {
  # Run the installation script and capture exit code
  export VIBESAFE_SKIP_CLONE=true
  run bash "$INSTALL_SCRIPT"
  
  # Check exit status
  [ "$status" -eq 0 ]
  
  # Check for clean installation philosophy message
  [[ "$output" == *"VibeSafe has been successfully installed"* ]]
  [[ "$output" == *"Clean Installation Philosophy"* ]]
  [[ "$output" == *"System files will be updated"* ]]
  [[ "$output" == *"User content will be preserved"* ]]
}

@test "Installation gracefully handles missing Python for What's Next" {
  # Temporarily hide Python to test fallback behavior
  export PATH="/usr/bin:/bin"  # Remove common Python paths
  export VIBESAFE_SKIP_CLONE=true
  
  run bash "$INSTALL_SCRIPT"
  
  # Should still succeed overall
  [ "$status" -eq 0 ]
  
  # Should warn about Python
  [[ "$output" == *"Warning"* ]] || [[ "$output" == *"Python"* ]]
}

@test "GENERATE: Cursor rules are created from project tenets" {
  # Create a test tenet file
  mkdir -p tenets/test
  cat > tenets/test/test-tenet.md << 'EOF'
## Tenet: test-tenet

**Title**: Test Tenet

**Description**: This is a test tenet for testing cursor rule generation.

**Quote**: *"Test quote for testing"*

**Examples**:
- Example 1: Test example
- Example 2: Another test example

**Counter-examples**:
- Counter-example 1: Bad test
- Counter-example 2: Another bad test

**Conflicts**:
- Can conflict with other tenets
- Resolution: Test resolution

**Version**: 1.0 (2025-07-28)
EOF

  # Copy the actual combine_tenets.py script for testing
  cp "$BATS_TEST_DIRNAME/../../tenets/combine_tenets.py" tenets/combine_tenets.py

  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that cursor rules directory exists
  [ -d ".cursor/rules" ]
  
  # Check that the test tenet rule was generated
  [ -f ".cursor/rules/project_tenet_test-tenet.mdc" ]
  
  # Verify the generated rule contains expected content
  grep -q "Project Tenet: Test Tenet" ".cursor/rules/project_tenet_test-tenet.mdc"
  grep -q "This is a test tenet for testing cursor rule generation" ".cursor/rules/project_tenet_test-tenet.mdc"
  grep -q "Test quote for testing" ".cursor/rules/project_tenet_test-tenet.mdc"
  grep -q "Example 1: Test example" ".cursor/rules/project_tenet_test-tenet.mdc"
  grep -q "Counter-example 1: Bad test" ".cursor/rules/project_tenet_test-tenet.mdc"
}

@test "PRESERVE: Existing cursor rules are not overwritten" {
  # Create an existing cursor rule
  mkdir -p .cursor/rules
  cat > .cursor/rules/project_tenet_existing.mdc << 'EOF'
---
description: "Existing rule that should be preserved"
globs: "**/*"
alwaysApply: true
---

# Existing Rule

This rule should not be overwritten.
EOF

  # Store the checksum of the existing rule
  EXISTING_RULE_CHECKSUM=$(md5sum .cursor/rules/project_tenet_existing.mdc | awk '{print $1}')
  
  # Create a test tenet that would generate the same rule
  mkdir -p tenets/test
  cat > tenets/test/existing.md << 'EOF'
## Tenet: existing

**Title**: Existing Tenet

**Description**: This tenet would generate a rule that already exists.

**Version**: 1.0 (2025-07-28)
EOF

  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Check that the existing rule was preserved (same checksum)
  NEW_CHECKSUM=$(md5sum .cursor/rules/project_tenet_existing.mdc | awk '{print $1}')
  [ "$EXISTING_RULE_CHECKSUM" = "$NEW_CHECKSUM" ]
  
  # Verify the content is still the original
  grep -q "Existing rule that should be preserved" ".cursor/rules/project_tenet_existing.mdc"
  grep -q "This rule should not be overwritten" ".cursor/rules/project_tenet_existing.mdc"
}

@test "Debug mode provides detailed output" {
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_DEBUG=true
  
  run bash "$INSTALL_SCRIPT"
  
  [ "$status" -eq 0 ]
  [[ "$output" == *"[DEBUG]"* ]]
} 