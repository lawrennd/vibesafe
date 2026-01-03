# What's Next Script

The What's Next script is a tool in the VibeSafe framework that helps teams understand their project's current status and identify pending tasks. It provides a comprehensive overview of:

- Git repository status
- CIP (Change Implementation Proposal) status
- Backlog item status
- Requirements status

## Philosophy

The What's Next script embodies several key principles from the VibeSafe framework:

1. **Progressive Disclosure**: Information is presented in layers, from high-level status to detailed implementation tasks
2. **Contextual Awareness**: The script maintains awareness of the project's current state and suggests relevant next steps
3. **Requirements-Driven Development**: Integration with the AI-Requirements framework ensures alignment with project goals
4. **Continuous Improvement**: Regular status checks help identify areas for improvement and maintain project momentum

## Installation

The script can be installed using the provided installation script:

```bash
./install-whats-next.sh
```

This will:
1. Create a Python virtual environment (if it doesn't exist)
2. Install required dependencies
3. Make the script executable
4. Create a convenience wrapper script

## Usage

The script can be run in several ways:

```bash
# Basic usage
./whats-next

# With options
./whats-next --no-git        # Skip Git status
./whats-next --no-color      # Disable colored output
./whats-next --cip-only      # Show only CIP status
./whats-next --backlog-only  # Show only backlog status
./whats-next --requirements-only  # Show only requirements status
```

## Example Use Case

Here's a typical workflow using the What's Next script:

1. **Daily Status Check**
   ```bash
   ./whats-next
   ```
   This provides a quick overview of:
   - Current Git branch and recent commits
   - Active CIPs and their status
   - High-priority backlog items
   - Requirements framework status

2. **Requirements-Focused Planning**
   ```bash
   ./whats-next --requirements-only
   ```
   Use this when:
   - Starting a new feature
   - Reviewing requirements for an existing feature
   - Checking requirements coverage

3. **CIP Review**
   ```bash
   ./whats-next --cip-only
   ```
   Use this when:
   - Planning sprint work
   - Reviewing proposed changes
   - Tracking implementation progress

4. **Backlog Management**
   ```bash
   ./whats-next --backlog-only
   ```
   Use this when:
   - Prioritizing work
   - Planning team capacity
   - Reviewing task status

## Features

### Git Status
- Current branch
- Recent commits (last 5)
- Modified files
- Untracked files

### CIP Status
- Total number of CIPs
- CIPs by status (proposed, accepted, implemented, closed)
- CIPs with/without frontmatter
- CIP details including title and dates

### Backlog Status
- Total number of backlog items
- Items by priority (high, medium, low)
- Items by status (proposed, ready, in progress, completed, abandoned)
- Items with/without frontmatter

### Requirements Status
- Total number of requirements
- Requirements by status
- Requirements with/without frontmatter

## Implementation Details

### Python Script (`scripts/whats_next.py`)

The main script is implemented in Python and provides the core functionality:

```python
def get_git_status() -> Dict[str, Any]:
    """Get Git repository status information."""
    # Implementation details...

def scan_cips() -> Dict[str, Any]:
    """Scan all CIP files and collect their status."""
    # Implementation details...

def scan_backlog() -> Dict[str, Any]:
    """Scan all backlog items and collect their status."""
    # Implementation details...

def scan_requirements() -> Dict[str, Any]:
    """Scan all requirements and collect their status."""
    # Implementation details...
```

### Shell Script (`install-whats-next.sh`)

The installation script handles the setup process:

```bash
# Create and activate virtual environment
python3 -m venv .venv-vibesafe
source .venv-vibesafe/bin/activate

# Install dependencies
pip install PyYAML

# Make script executable
chmod +x scripts/whats_next.py
```

## Integration with AI-Requirements Framework

The What's Next script integrates with the AI-Requirements framework to provide:

1. **Pattern-Based Analysis**
   - Identifies missing requirements patterns
   - Suggests appropriate patterns for new features
   - Tracks pattern implementation status

2. **Prompt Integration**
   - Links to relevant discovery prompts
   - Suggests refinement prompts for existing requirements
   - Provides validation prompts for implementation

3. **Requirements Tracking**
   - Monitors requirements coverage
   - Identifies gaps in requirements documentation
   - Suggests next steps for requirements gathering

## Dependencies

- Python 3.6 or higher
- PyYAML package
- Git (for Git status features)

## Contributing

To contribute to the What's Next script:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. **Virtual Environment Issues**
   - Ensure Python 3 is installed
   - On Ubuntu/Debian: `apt-get install python3-venv`

2. **Permission Issues**
   - Make sure the script is executable: `chmod +x whats-next`

3. **Dependency Issues**
   - Activate the virtual environment: `source .venv-vibesafe/bin/activate`
   - Install dependencies: `pip install PyYAML` 