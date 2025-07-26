#!/bin/bash
# VibeSafe Clean Installation Script
# Implements the Clean Installation Philosophy from CIP-000E
# 
# PHILOSOPHY: Install = Reinstall
# - Always overwrite VibeSafe system files (templates, system READMEs, cursor rules, scripts)
# - Always preserve user content (project README, user tasks/CIPs/tenets, .venv)

# ANSI color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default configuration (can be overridden via environment variables)
: "${VIBESAFE_REPO_URL:=https://github.com/lawrennd/vibesafe.git}"
: "${VIBESAFE_SKIP_CLONE:=false}"
: "${VIBESAFE_TEMPLATES_DIR:=}"
: "${VIBESAFE_DEBUG:=false}"
: "${VIBESAFE_INSTALL_WHATS_NEXT:=true}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function for debug output
debug() {
  if [ "$VIBESAFE_DEBUG" = "true" ]; then
    echo "[DEBUG] $1"
  fi
}

# Function to print banner
print_banner() {
  echo -e "${GREEN}"
  echo "██╗   ██╗██╗██████╗ ███████╗███████╗ █████╗ ███████╗███████╗"
  echo "██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝"
  echo "██║   ██║██║██████╔╝█████╗  ███████╗███████║█████╗  █████╗  "
  echo "╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║██╔══██║██╔══╝  ██╔══╝  "
  echo " ╚████╔╝ ██║██████╔╝███████╗███████║██║  ██║██║     ███████╗"
  echo "  ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝"
  echo -e "${NC}"
  echo "Clean Installation Script"
  echo "-------------------------"
  echo "System files will be updated, user content will be preserved"
  echo ""
}

# Function to create system template files (always overwrite)
create_system_template() {
  local dir="$1"
  local file="$2"
  local content="$3"
  
  # Make sure the directory exists
  mkdir -p "$dir"
  
  echo "$content" > "$dir/$file"
  debug "Created/updated system template: $dir/$file"
}

# Function to preserve user content while updating system files
install_system_files() {
  local templates_dir="$1"
  
  echo "Installing VibeSafe system files..."
  
  # ALWAYS OVERWRITE: VibeSafe system files
  if [ -d "$templates_dir/templates" ]; then
    debug "Installing from repository templates"
    
    # Install system template files (always overwrite)
    system_templates=(
      "backlog/README.md"
      "backlog/task_template.md"
      "backlog/update_index.py"
      "cip/README.md"
      "cip/cip_template.md"
      "tenets/README.md"
      "tenets/tenet_template.md"
      "tenets/combine_tenets.py"
    )
    
    for template in "${system_templates[@]}"; do
      if [ -f "$templates_dir/templates/$template" ]; then
        target_dir=$(dirname "$template")
        mkdir -p "$target_dir"
        cp -f "$templates_dir/templates/$template" "$template"
        debug "Installed system file: $template"
      fi
    done
    
    # Install AI-Requirements framework (always overwrite system files)
    if [ -d "$templates_dir/templates/ai-requirements" ]; then
      debug "Installing AI-Requirements framework"
      
      # Create structure and copy all system files
      find "$templates_dir/templates/ai-requirements" -type d | while read -r dir; do
        target_dir="${dir#$templates_dir/templates/}"
        debug "Creating directory: $target_dir"
        mkdir -p "$target_dir"
      done
      
      find "$templates_dir/templates/ai-requirements" -type f | while read -r file; do
        target_file="${file#$templates_dir/templates/}"
        debug "Installing AI-Requirements file: $target_file"
        cp -f "$file" "$target_file"
      done
    fi
    
    # Install cursor rules (always overwrite)
    if [ -d "$templates_dir/templates/.cursor" ]; then
      debug "Installing cursor rules"
      mkdir -p .cursor/rules
      cp -f "$templates_dir/templates/.cursor/rules/"* .cursor/rules/ 2>/dev/null || true
    fi
    
  else
    debug "No templates directory found, creating minimal system files"
    install_minimal_system_files
  fi
  
  echo "✅ VibeSafe system files installed"
}

# Function to install minimal system files when no repo is available
install_minimal_system_files() {
  debug "Installing minimal system files"
  
  # Create directory structure
  mkdir -p backlog/{documentation,features,infrastructure,bugs}
  mkdir -p cip
  mkdir -p tenets
  mkdir -p ai-requirements/{patterns,prompts/{discovery,refinement,validation,testing},integrations,examples,guidance}
  
  # Backlog system files
  create_system_template "backlog" "README.md" "# Backlog System
This directory contains tasks for the project.

## Structure
- features/: New feature tasks
- bugs/: Bug fix tasks  
- documentation/: Documentation tasks
- infrastructure/: Infrastructure tasks

Use task_template.md to create new tasks."

  create_system_template "backlog" "task_template.md" "---
id: \"YYYY-MM-DD_short-name\"
title: \"Task Title\"
status: \"Proposed\"
priority: \"Medium\"
created: \"YYYY-MM-DD\"
last_updated: \"YYYY-MM-DD\"
category: \"features\"
---

# Task: Task Title

## Description

Brief description of what needs to be done.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Implementation Notes

Any technical notes or considerations.

## Progress Updates

### YYYY-MM-DD
Task created."
  
  # CIP system files
  create_system_template "cip" "README.md" "# Code Improvement Proposals (CIPs)
This directory contains Code Improvement Proposals for the project.

## Overview
CIPs document planned improvements to the codebase.

Use cip_template.md to create new CIPs."

  create_system_template "cip" "cip_template.md" "---
id: \"XXXX\"
title: \"CIP Title\"
status: \"Proposed\"
created: \"YYYY-MM-DD\"
last_updated: \"YYYY-MM-DD\"
author: \"Author Name\"
---

# CIP-XXXX: CIP Title

## Status
- [ ] Proposed
- [ ] Accepted
- [ ] Implemented
- [ ] Closed

## Description
Brief overview of the proposed improvement.

## Motivation
Why this change is needed.

## Implementation
How the change will be implemented."

  # Tenets system files
  create_system_template "tenets" "README.md" "# Tenets
This directory contains the guiding principles for the project.

Use tenet_template.md to create new tenets."

  create_system_template "tenets" "tenet_template.md" "## Tenet: [id]

**Title**: [Concise Title]

**Description**: [Description of the tenet]

**Rationale**: [Why this tenet is important]

**Examples**: [Examples of how this tenet applies]"

  # Basic AI-Requirements files
  create_system_template "ai-requirements" "README.md" "# AI-Assisted Requirements Framework

This directory contains the framework for AI-assisted requirements gathering and management."
}

# Function to preserve project README if it exists, create if missing
preserve_project_readme() {
  echo "Checking project README.md..."
  
  if [ ! -f "README.md" ]; then
    echo "Creating project README.md..."
    cat > README.md << 'EOL'
# Project Name

This project uses [VibeSafe](https://github.com/lawrennd/vibesafe) for project management.

## Project Structure

- **tenets/**: Project tenets and guiding principles
- **backlog/**: Task tracking system
- **cip/**: Code Improvement Plans
- **ai-requirements/**: AI-Assisted Requirements Framework

## Getting Started

1. Define your project tenets in the `tenets/` directory
2. Use the `backlog/` to track tasks and issues
3. Document code improvements using CIPs in the `cip/` directory
4. Use the AI-Requirements framework for structured requirements gathering

For more information, visit: https://github.com/lawrennd/vibesafe
EOL
    debug "Created project README.md"
    echo "✅ Created project README.md"
  else
    echo "✅ Existing README.md preserved"
    debug "Preserved existing project README.md"
  fi
}

# Function to setup the "What's Next" script
setup_whats_next() {
  echo "Setting up 'What's Next' script..."
  
  # Check if Python 3 is available
  if ! command_exists python3; then
    echo -e "${YELLOW}Warning: Python 3 is required for the 'What's Next' script but not found.${NC}"
    echo "The script will not be installed. You can install it later with ./install-whats-next.sh"
    return 1
  fi
  
  # Try to find and install the What's Next script
  local whats_next_source=""
  
  if [ -n "$VIBESAFE_TEMPLATES_DIR" ] && [ -f "$VIBESAFE_TEMPLATES_DIR/scripts/whats_next.py" ]; then
    whats_next_source="$VIBESAFE_TEMPLATES_DIR/scripts/whats_next.py"
  elif [ -f "scripts/whats_next.py" ]; then
    whats_next_source="scripts/whats_next.py"
  fi
  
  if [ -n "$whats_next_source" ]; then
    # Copy the script if it's not already in place
    if [ "$whats_next_source" != "scripts/whats_next.py" ]; then
      mkdir -p scripts
      cp "$whats_next_source" "scripts/whats_next.py"
    fi
    
    # Run the installation script for What's Next
    if [ -f "./install-whats-next.sh" ]; then
      debug "Running existing install-whats-next.sh"
      ./install-whats-next.sh
    else
      echo "Creating basic What's Next setup..."
      
      # Create virtual environment if it doesn't exist (preserve if exists)
      if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        debug "Created virtual environment"
      else
        debug "Preserved existing virtual environment"
      fi
      
      # Install dependencies
      .venv/bin/pip install -q PyYAML
      
      # Create wrapper script (always overwrite - it's a system file)
      cat > whats-next << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
.venv/bin/python scripts/whats_next.py "$@"
EOF
      chmod +x whats-next
      debug "Created whats-next wrapper script"
    fi
    
    echo "✅ What's Next script installed"
  else
    echo -e "${YELLOW}Warning: Could not find whats_next.py script${NC}"
  fi
}

# Main installation function implementing Clean Installation Philosophy
install_vibesafe() {
  print_banner
  
  echo "Installing VibeSafe with Clean Installation Philosophy..."
  echo "📁 System files will be updated"
  echo "🛡️  User content will be preserved"
  echo ""
  
  local temp_dir=""
  
  # Determine source of templates
  if [ -n "$VIBESAFE_TEMPLATES_DIR" ]; then
    debug "Using provided templates directory: $VIBESAFE_TEMPLATES_DIR"
    install_system_files "$VIBESAFE_TEMPLATES_DIR"
  elif [ "$VIBESAFE_SKIP_CLONE" = "true" ]; then
    debug "Skipping repository clone, using minimal system files"
    install_minimal_system_files
  else
    # Clone the repository
    temp_dir=$(mktemp -d)
    debug "Created temporary directory: $temp_dir"
    echo "Cloning VibeSafe repository..."
    
    if git clone --quiet "$VIBESAFE_REPO_URL" "$temp_dir"; then
      debug "Successfully cloned repository from $VIBESAFE_REPO_URL"
      install_system_files "$temp_dir"
      
      # Copy What's Next script if it exists (system file)
      if [ -f "$temp_dir/scripts/whats_next.py" ]; then
        debug "Found What's Next script in repository"
        mkdir -p scripts
        cp "$temp_dir/scripts/whats_next.py" "scripts/whats_next.py"
        
        # Copy installation script (system file)
        if [ -f "$temp_dir/install-whats-next.sh" ]; then
          cp "$temp_dir/install-whats-next.sh" "install-whats-next.sh"
        fi
      fi
    else
      debug "Failed to clone repository, using minimal system files"
      echo "Warning: Failed to clone repository, using minimal templates instead."
      install_minimal_system_files
    fi
  fi
  
  # ALWAYS PRESERVE: User content
  preserve_project_readme
  
  # Setup What's Next script if requested (system file installation)
  if [ "$VIBESAFE_INSTALL_WHATS_NEXT" = "true" ]; then
    setup_whats_next
  fi
  
  # Clean up temporary directory if we created one
  if [ -n "$temp_dir" ]; then
    rm -rf "$temp_dir"
    debug "Removed temporary directory"
  fi
  
  echo ""
  echo -e "${GREEN}🎉 VibeSafe has been successfully installed!${NC}"
  echo ""
  echo "Clean Installation Philosophy applied:"
  echo "✅ VibeSafe system files updated to latest version"
  echo "✅ User content preserved"
  echo ""
  echo -e "${YELLOW}Next steps:${NC}"
  echo "1. Define your project tenets in the tenets/ directory"
  echo "2. Use the backlog to track tasks"
  echo "3. Document code improvements using CIPs"
  if [ "$VIBESAFE_INSTALL_WHATS_NEXT" = "true" ] && [ -f "whats-next" ]; then
    echo "4. Run the 'What's Next' script to see project status: ./whats-next"
  fi
  echo ""
  echo "For more information, visit: https://github.com/lawrennd/vibesafe"
  echo ""
  
  return 0
}

# Run the installation
install_vibesafe 