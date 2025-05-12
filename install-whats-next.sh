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