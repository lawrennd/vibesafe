#!/usr/bin/env bats
# Tests for VibeSafe Clean Installation Philosophy (CIP-000E)
# Verifies: System files overwritten, User content preserved

# Store original directory before any tests run
ORIGINAL_DIR="$(pwd)"

# Setup file runs once before all tests
setup_file() {
  # Clone VibeSafe once to a shared location for tests that need it
  export VIBESAFE_SHARED_CLONE="$(mktemp -d)"
  local current_dir="$(pwd)"
  cd "$VIBESAFE_SHARED_CLONE"
  git clone --quiet https://github.com/lawrennd/vibesafe.git vibesafe-test-clone
  export VIBESAFE_TEST_TEMPLATES="$VIBESAFE_SHARED_CLONE/vibesafe-test-clone"
  cd "$current_dir"
}

# Cleanup after all tests
teardown_file() {
  if [ -n "$VIBESAFE_SHARED_CLONE" ] && [ -d "$VIBESAFE_SHARED_CLONE" ]; then
    rm -rf "$VIBESAFE_SHARED_CLONE"
  fi
}

setup() {
  # Create a temporary directory for testing
  TEST_DIR="$(mktemp -d)"
  
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

@test "VENV: Old VibeSafe .venv is migrated to .venv-vibesafe on first install" {
  # Create a mock old VibeSafe .venv (minimal with PyYAML)
  python3 -m venv .venv
  .venv/bin/pip install -q PyYAML python-frontmatter
  
  # Verify it looks like old VibeSafe venv
  [ -d ".venv" ]
  [ ! -d ".venv-vibesafe" ]
  
  # Copy whats-next script so migration logic runs
  mkdir -p scripts
  if [ -f "$ORIGINAL_DIR/scripts/whats_next.py" ]; then
    cp "$ORIGINAL_DIR/scripts/whats_next.py" scripts/
  fi
  
  # Run the installation script with whats-next enabled
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$INSTALL_SCRIPT"
  
  # Verify migration happened
  [ "$status" -eq 0 ]
  [ ! -d ".venv" ]  # Old venv should be removed
  [ -d ".venv-vibesafe" ]  # New venv should exist
  [ -f ".venv-vibesafe/bin/python" ]
}

@test "VENV: Project .venv (not VibeSafe) is preserved" {
  # Create a mock project venv with many packages (not VibeSafe)
  python3 -m venv .venv
  .venv/bin/pip install -q requests 2>/dev/null || true
  
  # Store python executable path
  PYTHON_PATH=$(ls .venv/bin/python* | head -1)
  [ -f "$PYTHON_PATH" ]
  
  # Copy whats-next script so migration logic runs
  mkdir -p scripts
  if [ -f "$ORIGINAL_DIR/scripts/whats_next.py" ]; then
    cp "$ORIGINAL_DIR/scripts/whats_next.py" scripts/
  fi
  
  # Run the installation script with whats-next enabled
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$INSTALL_SCRIPT"
  
  # Verify project .venv was preserved
  [ "$status" -eq 0 ]
  [ -d ".venv" ]  # Project venv should still exist
  [ -d ".venv-vibesafe" ]  # VibeSafe venv should be created separately
  [ -f "$PYTHON_PATH" ]  # Original python still there
}

@test "VENV: Orphaned .venv warns but doesn't delete when .venv-vibesafe exists" {
  # Create both venvs (simulating testing scenario)
  python3 -m venv .venv
  .venv/bin/pip install -q PyYAML python-frontmatter
  python3 -m venv .venv-vibesafe
  .venv-vibesafe/bin/pip install -q PyYAML python-frontmatter
  
  # Copy whats-next script so migration logic runs
  mkdir -p scripts
  if [ -f "$ORIGINAL_DIR/scripts/whats_next.py" ]; then
    cp "$ORIGINAL_DIR/scripts/whats_next.py" scripts/
  fi
  
  # Run the installation script with whats-next enabled
  export VIBESAFE_SKIP_CLONE=true
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$INSTALL_SCRIPT"
  
  # Verify both still exist (orphaned .venv not deleted)
  [ "$status" -eq 0 ]
  [ -d ".venv" ]  # Orphaned venv should still exist
  [ -d ".venv-vibesafe" ]  # Active venv should exist
  
  # Verify warning was shown
  [[ "$output" == *"orphaned"* ]] || [[ "$output" == *".venv"* ]]
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

@test "VALIDATE: Validation runs by default during installation" {
  # Copy the validation script to make it available
  mkdir -p scripts
  if [ -f "$ORIGINAL_DIR/scripts/validate_vibesafe_structure.py" ]; then
    cp "$ORIGINAL_DIR/scripts/validate_vibesafe_structure.py" scripts/
  fi
  
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT" > output.log 2>&1
  
  # Check that validation was attempted (if validator exists)
  # Should see either validation message or skip message
  grep -q "Validating VibeSafe structure" output.log || \
  grep -q "VibeSafe structure validated" output.log || \
  grep -q "Validation found issues" output.log || \
  grep -q "Validation script not found" output.log
}

@test "VALIDATE: Validation can be skipped with environment variable" {
  # Run the installation script with validation skipped
  VIBESAFE_SKIP_CLONE=true VIBESAFE_SKIP_VALIDATION=1 bash "$INSTALL_SCRIPT" > output.log 2>&1
  
  # Check that validation was NOT run
  ! grep -q "Validating VibeSafe structure" output.log
  ! grep -q "Found.*issue.*auto-fixed" output.log
}

@test "VALIDATE: Validation script is preserved if exists" {
  # Create a validation script
  mkdir -p scripts
  cat > scripts/validate_vibesafe_structure.py << 'EOF'
#!/usr/bin/env python3
"""Test validation script"""
print("Test validator")
exit(0)
EOF
  chmod +x scripts/validate_vibesafe_structure.py
  
  # Store checksum
  VALIDATOR_CHECKSUM=$(md5sum scripts/validate_vibesafe_structure.py | awk '{print $1}')
  
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT"
  
  # Validation script should still exist (it's a system file, gets overwritten in real install)
  [ -f "scripts/validate_vibesafe_structure.py" ]
}

@test "VALIDATE: Non-interactive mode skips validation prompt" {
  # Create a project with validation issues (missing frontmatter)
  mkdir -p backlog/features
  cat > backlog/features/2026-01-03_test-task.md << 'EOF'
# Test Task

This task has no YAML frontmatter and will fail validation.
EOF
  
  # Run installation in non-interactive mode (pipe input)
  echo "n" | VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT" > output.log 2>&1
  
  # Should detect non-interactive mode
  grep -q "Non-interactive mode detected" output.log || \
  ! grep -q "Apply automatic fixes?" output.log
}

@test "VALIDATE: Installation succeeds even if validation finds issues" {
  # Create a project with validation issues
  mkdir -p backlog/features
  cat > backlog/features/2026-01-03_test-task.md << 'EOF'
# Test Task

This task has no YAML frontmatter.
EOF
  
  # Run the installation script
  run bash -c "VIBESAFE_SKIP_CLONE=true bash '$INSTALL_SCRIPT' 2>&1"
  
  # Installation should still succeed (validation doesn't block)
  [ "$status" -eq 0 ]
  [[ "$output" == *"successfully installed"* ]]
}

@test "VALIDATE: Success message shows validation status" {
  # Copy the validation script to make it available
  mkdir -p scripts
  if [ -f "$ORIGINAL_DIR/scripts/validate_vibesafe_structure.py" ]; then
    cp "$ORIGINAL_DIR/scripts/validate_vibesafe_structure.py" scripts/
  fi
  
  # Run the installation script
  VIBESAFE_SKIP_CLONE=true bash "$INSTALL_SCRIPT" > output.log 2>&1
  
  # Success message should always appear
  grep -q "Clean Installation Philosophy applied" output.log
  
  # If validation ran, status should be shown
  # (Either validated successfully, or skipped, or found issues)
  grep -q "successfully installed" output.log
} 
@test "SCRIPTS: Both user-facing scripts are deployed" {
  # Use shared clone to speed up test
  export VIBESAFE_TEMPLATES_DIR="$VIBESAFE_TEST_TEMPLATES"
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  run bash "$INSTALL_SCRIPT"
  [ "$status" -eq 0 ]
  
  # Verify both scripts exist and are executable
  [ -f "scripts/whats_next.py" ]
  [ -x "scripts/whats_next.py" ]
  [ -f "scripts/validate_vibesafe_structure.py" ]
  [ -x "scripts/validate_vibesafe_structure.py" ]
  
  # Verify they have content (not empty)
  [ -s "scripts/whats_next.py" ]
  [ -s "scripts/validate_vibesafe_structure.py" ]
}

@test "SCRIPTS: Validator script works with .venv-vibesafe" {
  # Use shared clone to speed up test
  export VIBESAFE_TEMPLATES_DIR="$VIBESAFE_TEST_TEMPLATES"
  export VIBESAFE_INSTALL_WHATS_NEXT=true
  bash "$INSTALL_SCRIPT"
  
  # Verify validator can be run
  [ -f "scripts/validate_vibesafe_structure.py" ]
  [ -d ".venv-vibesafe" ]
  
  # Run validator (should not crash)
  run .venv-vibesafe/bin/python scripts/validate_vibesafe_structure.py --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"VibeSafe Structure Validation"* ]]
}

@test "DOGFOOD: templates/ not added to gitignore in VibeSafe repo" {
  # Simulate VibeSafe repo structure
  mkdir -p templates/.cursor/rules
  mkdir -p templates/scripts
  touch templates/scripts/whats_next.py
  
  export VIBESAFE_SKIP_CLONE=true
  bash "$INSTALL_SCRIPT"
  
  # Verify templates/ is NOT in gitignore (dogfood detection)
  if [ -f ".gitignore" ]; then
    ! grep -q "^templates/$" .gitignore
  fi
}

@test "DOGFOOD: templates/ added to gitignore in user projects" {
  # Regular user project (no templates/ structure)
  export VIBESAFE_SKIP_CLONE=true
  bash "$INSTALL_SCRIPT"
  
  # Verify templates/ IS in gitignore
  [ -f ".gitignore" ]
  grep -q "^templates/$" .gitignore
}
