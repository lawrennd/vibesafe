#!/bin/bash
# Installation script for the VibeSafe "What's Next" script
#
# This script sets up the What's Next script by:
# 1. Creating a Python virtual environment
# 2. Installing required dependencies
# 3. Making the script executable
# 4. Creating a convenience wrapper script
#
# Usage:
#   ./install-whats-next.sh
#
# Requirements:
#   - Python 3.6 or higher
#   - python3-venv package (on Ubuntu/Debian)
#
# Exit codes:
#   0 - Success
#   1 - Error creating virtual environment
#   2 - Error installing dependencies
#   3 - Error making script executable
#   4 - Error creating wrapper script

set -e

echo "Installing 'What's Next' Script..."

# Create and activate a virtual environment if it doesn't exist
VENV_DIR=".venv-vibesafe"
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
python3 -m pip install PyYAML python-frontmatter
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 2
fi

# Make the script executable
echo "Making script executable..."
chmod +x scripts/whats_next.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to make script executable."
    exit 3
fi

# Create a convenience wrapper script
echo "Creating convenience wrapper script..."
cat > whats-next << 'EOF'
#!/bin/bash
# Wrapper script for running the What's Next script with the virtual environment
#
# This script ensures the What's Next script runs in the correct virtual environment
# and handles proper activation/deactivation of the environment.
#
# Usage:
#   ./whats-next [options]
#
# Options:
#   --no-git              Skip Git status information
#   --no-color           Disable colored output
#   --cip-only           Show only CIP status
#   --backlog-only       Show only backlog status
#   --requirements-only  Show only requirements status

# Determine directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "${SCRIPT_DIR}/.venv-vibesafe/bin/activate"

# Run the actual script
"${SCRIPT_DIR}/scripts/whats_next.py" "$@"

# Deactivate the virtual environment
deactivate
EOF

# Make the wrapper script executable
chmod +x whats-next
if [ $? -ne 0 ]; then
    echo "Error: Failed to make wrapper script executable."
    exit 4
fi

# Install requirements cursor rule
echo "Installing requirements cursor rule..."
mkdir -p .cursor/rules
if [ -f "templates/cursor_rules/requirements_rule.md" ]; then
    cp templates/cursor_rules/requirements_rule.md .cursor/rules/
    echo "Requirements cursor rule installed."
else
    echo "Warning: Requirements cursor rule template not found."
fi

# Deactivate virtual environment
deactivate

echo ""
echo "Installation complete!"
echo "You can now run the 'What's Next' script using:"
echo "  ./whats-next"
echo ""
echo "Or with options:"
echo "  ./whats-next --no-git --no-color --cip-only --backlog-only --requirements-only"
echo ""
echo "For more information, see:"
echo "  docs/whats_next_script.md" 