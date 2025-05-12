#!/bin/bash
# VibeSafe Minimal Installation Script
# This script installs the basic VibeSafe templates in the current directory.

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
  echo "Minimal Installation Script"
  echo "----------------------------"
}

# Function to create default template file
create_default_template() {
  local dir="$1"
  local file="$2"
  local content="$3"
  
  # Make sure the directory exists
  mkdir -p "$dir"
  
  echo "$content" > "$dir/$file"
  debug "Created default template: $dir/$file"
}

# Function to create the default directory structure
# Only used when we can't get the structure from the repo
create_default_directory_structure() {
  debug "Creating default directory structure"
  mkdir -p cip backlog/documentation backlog/features backlog/infrastructure backlog/bugs tenets
}

# Function to create default backlog files
create_default_backlog_files() {
  create_default_template "backlog" "README.md" "# Backlog System\nThis directory contains tasks for the project."
  
  create_default_template "backlog" "task_template.md" "# Task: [Title]\n\n- **ID**: [YYYY-MM-DD_short-name]\n- **Status**: Proposed\n- **Priority**: [High/Medium/Low]\n\n## Description\n\n## Acceptance Criteria"
  
  # Create backlog subdirectories
  mkdir -p backlog/documentation backlog/features backlog/infrastructure backlog/bugs
}

# Function to create default CIP files
create_default_cip_files() {
  create_default_template "cip" "README.md" "# Code Improvement Proposals (CIPs)\nThis directory contains Code Improvement Proposals for the project."
  
  create_default_template "cip" "cip_template.md" "# CIP-XXXX: [Title]\n\n## Summary\nA brief summary of the proposed improvement."
}

# Function to create default tenet files
create_default_tenet_files() {
  create_default_template "tenets" "README.md" "# Tenets\nThis directory contains the guiding principles for the project."
  
  create_default_template "tenets" "tenet_template.md" "## Tenet: [id]\n\n**Title**: [Concise Title]\n\n**Description**: [Description of the tenet]"
}

# Function to create default README.md
create_default_readme() {
  if [ ! -f "README.md" ]; then
    echo "Creating project README.md..."
    cat > README.md << 'EOL'
# Project Name

This project uses [VibeSafe](https://github.com/lawrennd/vibesafe) for project management.

## Project Structure

```
project/
├── README.md                 # This file
├── tenets/                   # Project tenets
│   ├── README.md             # Overview of the tenet system
│   └── tenet_template.md     # Template for creating new tenets
├── backlog/                  # Task tracking system
│   ├── README.md             # Overview of the backlog system
│   └── task_template.md      # Template for creating new tasks
└── cip/                      # Code Improvement Plans
    ├── README.md             # Overview of the CIP process
    └── cip_template.md       # Template for creating new CIPs
```

## Getting Started

1. Define your project tenets in the `tenets/` directory
2. Use the backlog to track tasks
3. Document code improvements using CIPs
EOL
    debug "Created default README.md"
  else
    echo "Existing README.md found, skipping creation."
    debug "Preserved existing README.md"
  fi
}

# Function to copy the directory structure and templates from the repository
copy_templates_from_repo() {
  local templates_dir="$1"
  
  debug "Copying directory structure and templates from repository"
  
  # First, check if templates directory exists
  if [ -d "$templates_dir/templates" ]; then
    # Copy entire directory structure as-is, preserving structure
    debug "Found templates directory, copying directory structure"
    
    # Create base directories first (in case the structure is partial)
    mkdir -p cip backlog tenets
    
    # Copy backlog directory structure if it exists
    if [ -d "$templates_dir/templates/backlog" ]; then
      debug "Copying backlog directory structure"
      
      # First create the directory structure
      find "$templates_dir/templates/backlog" -type d | while read -r dir; do
        # Create the equivalent directory in the target
        target_dir="${dir#$templates_dir/templates/}"
        debug "Creating directory: $target_dir"
        mkdir -p "$target_dir"
      done
      
      # Then copy the files
      find "$templates_dir/templates/backlog" -type f | while read -r file; do
        # Determine the target file path
        target_file="${file#$templates_dir/templates/}"
        debug "Copying file: $file to $target_file"
        cp -f "$file" "$target_file"
      done
    else
      debug "No backlog directory structure found, creating defaults"
      create_default_backlog_files
    fi
    
    # Copy CIP directory structure if it exists
    if [ -d "$templates_dir/templates/cip" ]; then
      debug "Copying CIP directory structure"
      
      # First create the directory structure
      find "$templates_dir/templates/cip" -type d | while read -r dir; do
        # Create the equivalent directory in the target
        target_dir="${dir#$templates_dir/templates/}"
        debug "Creating directory: $target_dir"
        mkdir -p "$target_dir"
      done
      
      # Then copy the files
      find "$templates_dir/templates/cip" -type f | while read -r file; do
        # Determine the target file path
        target_file="${file#$templates_dir/templates/}"
        debug "Copying file: $file to $target_file"
        cp -f "$file" "$target_file"
      done
    else
      debug "No CIP directory structure found, creating defaults"
      create_default_cip_files
    fi
    
    # Copy tenets directory structure if it exists
    if [ -d "$templates_dir/templates/tenets" ]; then
      debug "Copying tenets directory structure"
      
      # First create the directory structure
      find "$templates_dir/templates/tenets" -type d | while read -r dir; do
        # Create the equivalent directory in the target
        target_dir="${dir#$templates_dir/templates/}"
        debug "Creating directory: $target_dir"
        mkdir -p "$target_dir"
      done
      
      # Then copy the files
      find "$templates_dir/templates/tenets" -type f | while read -r file; do
        # Determine the target file path
        target_file="${file#$templates_dir/templates/}"
        debug "Copying file: $file to $target_file"
        cp -f "$file" "$target_file"
      done
    else
      debug "No tenets directory structure found, creating defaults"
      create_default_tenet_files
    fi
    
    # Copy any cursor rules if they exist
    if [ -d "$templates_dir/templates/.cursor" ]; then
      debug "Found cursor templates in repository"
      mkdir -p .cursor/rules
      cp "$templates_dir/templates/.cursor/rules/"* .cursor/rules/ 2>/dev/null || echo "Warning: Could not copy Cursor rules"
    fi
  else
    debug "No templates directory found in repository, creating default structure"
    create_default_directory_structure
    create_default_backlog_files
    create_default_cip_files
    create_default_tenet_files
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
  
  # Check if the whats_next.py script exists
  if [ ! -f "scripts/whats_next.py" ]; then
    echo -e "${YELLOW}Warning: scripts/whats_next.py not found. Skipping 'What's Next' setup.${NC}"
    return 1
  fi
  
  # Create and activate a virtual environment
  local VENV_DIR=".venv"
  echo "Creating Python virtual environment..."
  
  if ! python3 -m venv "$VENV_DIR"; then
    echo -e "${YELLOW}Warning: Failed to create virtual environment. 'What's Next' script will not be installed.${NC}"
    echo "You can try again later with ./install-whats-next.sh"
    return 1
  fi
  
  # Create the installation script for future use
  if [ ! -f "install-whats-next.sh" ]; then
    echo "Creating 'What's Next' installation script..."
    cat > install-whats-next.sh << 'EOL'
#!/bin/bash
# Installation script for the VibeSafe "What's Next" script

set -e

echo "Installing 'What's Next' Script..."

# Create and activate a virtual environment if it doesn't exist
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        echo "Make sure python3-venv is installed on your system."
        echo "  - Ubuntu/Debian: apt-get install python3-venv"
        echo "  - macOS: Python 3 should include venv by default"
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install PyYAML

# Make the script executable
echo "Making script executable..."
chmod +x scripts/whats_next.py

# Create a convenience wrapper script
echo "Creating convenience wrapper script..."
cat > whats-next << 'EOF'
#!/bin/bash
# Wrapper script for running the What's Next script with the virtual environment

# Determine directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "${SCRIPT_DIR}/.venv/bin/activate"

# Run the actual script
"${SCRIPT_DIR}/scripts/whats_next.py" "$@"

# Deactivate the virtual environment
deactivate
EOF

# Make the wrapper script executable
chmod +x whats-next

# Deactivate virtual environment
deactivate

echo ""
echo "Installation complete!"
echo "You can now run the 'What's Next' script using:"
echo "  ./whats-next"
echo ""
echo "Or with options:"
echo "  ./whats-next --no-git --no-color --cip-only --backlog-only --quiet"
echo ""
echo "For more information, see:"
echo "  docs/whats_next_script.md"
EOL
    chmod +x install-whats-next.sh
  fi
  
  # Execute the installation script we just created
  echo "Installing 'What's Next' dependencies..."
  
  # Activate the virtual environment
  source "$VENV_DIR/bin/activate"
  
  # Install dependencies
  python3 -m pip install PyYAML
  
  # Make the script executable
  chmod +x scripts/whats_next.py
  
  # Create a convenience wrapper script
  echo "Creating convenience wrapper script..."
  cat > whats-next << 'EOL'
#!/bin/bash
# Wrapper script for running the What's Next script with the virtual environment

# Determine directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "${SCRIPT_DIR}/.venv/bin/activate"

# Run the actual script
"${SCRIPT_DIR}/scripts/whats_next.py" "$@"

# Deactivate the virtual environment
deactivate
EOL

  # Make the wrapper script executable
  chmod +x whats-next
  
  # Deactivate virtual environment
  deactivate
  
  echo -e "${GREEN}Successfully installed 'What's Next' script!${NC}"
  echo "You can run it with ./whats-next"
  
  return 0
}

# Main installation function
install_vibesafe() {
  local temp_dir=""
  
  print_banner
  
  # Check prerequisites
  echo "Checking prerequisites..."
  if ! command_exists git && [ "$VIBESAFE_SKIP_CLONE" = "false" ]; then
    echo -e "${RED}Error: git is required but not installed.${NC}"
    echo "Please install git and try again."
    return 1
  fi
  
  # Use provided templates directory or clone repository
  if [ -n "$VIBESAFE_TEMPLATES_DIR" ]; then
    debug "Using provided templates directory: $VIBESAFE_TEMPLATES_DIR"
    copy_templates_from_repo "$VIBESAFE_TEMPLATES_DIR"
  elif [ "$VIBESAFE_SKIP_CLONE" = "true" ]; then
    debug "Skipping repository clone, using default templates"
    create_default_directory_structure
    create_default_backlog_files
    create_default_cip_files
    create_default_tenet_files
  else
    # Clone the repository
    temp_dir=$(mktemp -d)
    debug "Created temporary directory: $temp_dir"
    echo "Cloning VibeSafe repository..."
    
    if git clone --quiet "$VIBESAFE_REPO_URL" "$temp_dir"; then
      debug "Successfully cloned repository from $VIBESAFE_REPO_URL"
      echo "Copying VibeSafe templates..."
      copy_templates_from_repo "$temp_dir"
      
      # Copy What's Next script if it exists
      if [ -f "$temp_dir/scripts/whats_next.py" ]; then
        debug "Found What's Next script in repository"
        mkdir -p scripts
        cp "$temp_dir/scripts/whats_next.py" "scripts/whats_next.py"
        # Copy docs if they exist
        if [ -f "$temp_dir/docs/whats_next_script.md" ]; then
          mkdir -p docs
          cp "$temp_dir/docs/whats_next_script.md" "docs/whats_next_script.md"
        fi
        if [ -f "$temp_dir/docs/yaml_frontmatter_examples.md" ]; then
          mkdir -p docs
          cp "$temp_dir/docs/yaml_frontmatter_examples.md" "docs/yaml_frontmatter_examples.md"
        fi
      fi
    else
      debug "Failed to clone repository, using default templates"
      echo "Warning: Failed to clone repository, using minimal templates instead."
      create_default_directory_structure
      create_default_backlog_files
      create_default_cip_files
      create_default_tenet_files
    fi
  fi
  
  # Create or preserve README
  echo "Checking for existing README.md..."
  create_default_readme
  
  # Setup What's Next script if requested
  if [ "$VIBESAFE_INSTALL_WHATS_NEXT" = "true" ]; then
    setup_whats_next
  fi
  
  # Clean up temporary directory if we created one
  if [ -n "$temp_dir" ]; then
    rm -rf "$temp_dir"
    debug "Removed temporary directory"
  fi
  
  echo -e "${GREEN}VibeSafe has been successfully installed!${NC}"
  echo "The basic project structure has been created."
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