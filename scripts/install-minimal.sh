#!/bin/bash
# VibeSafe Minimal Installation Script
# This script installs the basic VibeSafe templates in the current directory.

# ANSI color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
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

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."
if ! command_exists git; then
  echo -e "${RED}Error: git is required but not installed.${NC}"
  echo "Please install git and try again."
  exit 1
fi

# Set the repository URL
REPO_URL="https://github.com/lawrennd/vibesafe.git"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Clone the repository into the temp directory
echo "Cloning VibeSafe repository..."
if ! git clone --quiet "$REPO_URL" "$TEMP_DIR"; then
  echo -e "${RED}Error: Failed to clone repository.${NC}"
  rm -rf "$TEMP_DIR"
  exit 1
fi

# Copy the templates into the current directory
echo "Copying VibeSafe templates..."

# Create the directory structure
mkdir -p cip backlog/documentation backlog/features backlog/infrastructure backlog/bugs tenets

# Copy template files
cp "$TEMP_DIR/templates/backlog/README.md" backlog/
cp "$TEMP_DIR/templates/backlog/task_template.md" backlog/
cp "$TEMP_DIR/templates/backlog/update_index.py" backlog/

cp "$TEMP_DIR/templates/cip/README.md" cip/
cp "$TEMP_DIR/templates/cip/cip_template.md" cip/

cp "$TEMP_DIR/templates/tenets/README.md" tenets/
cp "$TEMP_DIR/templates/tenets/tenet_template.md" tenets/
cp "$TEMP_DIR/templates/tenets/combine_tenets.py" tenets/

# Copy any cursor rules if they exist
if [ -d "$TEMP_DIR/templates/.cursor" ]; then
  mkdir -p .cursor/rules
  cp "$TEMP_DIR/templates/.cursor/rules/"* .cursor/rules/ 2>/dev/null || :
fi

# Create a basic README.md in the current directory
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

# Clean up
rm -rf "$TEMP_DIR"

echo -e "${GREEN}VibeSafe has been successfully installed!${NC}"
echo "The basic project structure has been created."
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Define your project tenets in the tenets/ directory"
echo "2. Use the backlog to track tasks"
echo "3. Document code improvements using CIPs"
echo ""
echo "For more information, visit: https://github.com/lawrennd/vibesafe"
echo "" 