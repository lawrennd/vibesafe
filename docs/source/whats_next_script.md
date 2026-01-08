# What's Next Script

## Overview

The "What's Next" script is a project status summarizer that helps LLMs and human users quickly understand the current state of the VibeSafe project and identify pending tasks. It provides a comprehensive overview of:

- Git repository status
- CIP (Code Improvement Proposal) status
- Backlog item status
- Recommended next steps
- Files needing YAML frontmatter

## Installation

The script is located in the `scripts` directory of the VibeSafe repository:

```bash
scripts/whats_next.py
```

### Dependencies

The script requires:
- Python 3.6+
- PyYAML library

You can install everything needed using:

1. The installation script (recommended):
   ```bash
   # This creates a virtual environment and sets up a convenient wrapper
   ./install-whats-next.sh
   ```

2. Using the run-python-tests.sh script (for development):
   ```bash
   # This creates a virtual environment for testing
   ./scripts/run-python-tests.sh
   ```

3. Using the pyproject.toml file (if you have Poetry installed):
   ```bash
   # Install Poetry if you don't have it
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry install
   ```

## Usage

After installation using the installation script, run the script using:

```bash
./whats-next
```

If you prefer to run it directly, make sure to activate the virtual environment first:

```bash
source .venv/bin/activate
python scripts/whats_next.py
deactivate  # When finished
```

### Command Line Options

The script supports several command line options:

- `--no-git`: Skip Git status information
- `--no-color`: Disable colored output
- `--cip-only`: Only show CIP information
- `--backlog-only`: Only show backlog information
- `--requirements-only`: Only show requirements information
- `--compression-check`: Show detailed compression candidates (closed CIPs needing compression)
- `--quiet`: Suppress all output except next steps

Examples:

```bash
# Show only the next steps (useful for quick reference)
./whats-next --quiet

# Focus only on CIPs
./whats-next --cip-only

# Focus only on backlog items
./whats-next --backlog-only

# Disable color (useful for non-interactive terminals)
./whats-next --no-color
```

## Output Sections

### Git Status

Shows the current branch, recent commits, modified files, and untracked files.

### CIP Status

Lists all CIPs, categorized by their status (proposed, accepted, implemented, closed), and identifies those missing YAML frontmatter.

### Backlog Status

Lists backlog items, highlighting high-priority items and those in progress, and identifies items missing YAML frontmatter.

### Recommended Next Steps

Provides a prioritized list of recommended actions based on the project's current state.

### Files Needing YAML Frontmatter

Lists specific files that need YAML frontmatter to be added for better project tracking.

### Compression Suggestions (New)

When closed CIPs haven't been compressed into formal documentation, the script automatically detects and suggests compression actions. This helps ensure that knowledge from closed CIPs is systematically transferred to permanent documentation.

## YAML Frontmatter

The script checks for and recommends adding YAML frontmatter to CIPs and backlog items. See [YAML Frontmatter Examples](yaml_frontmatter_examples.md) for the required format.

## Compression Detection

The "What's Next" script automatically detects closed CIPs that haven't been compressed into formal documentation and suggests compression actions.

### What is Compression?

**Documentation compression** is the process of distilling knowledge from closed CIPs (design rationale), completed backlog tasks (implementation details), and finalized code into streamlined formal documentation. This ensures that future users can understand what was built without reading the entire development history.

### --compression-check Flag

Use the `--compression-check` flag to see a detailed view of compression candidates:

```bash
./whats-next --compression-check
```

**Output includes**:
- List of closed CIPs with `compressed: false` (or missing the field)
- Days since CIP closure
- Priority level (High, Medium, Low)
- Batch compression opportunities (3+ CIPs closed within 7 days)

### Compression Suggestions in Main Output

When running `./whats-next` without flags, compression suggestions appear in the "Suggested Next Steps" section if:

1. **Any closed CIPs need compression**: Suggests using the compression template
2. **Batch opportunity detected**: 3+ CIPs closed within 7 days
3. **High-priority CIPs uncompressed**: Older or high-priority CIPs are highlighted

### Compression Workflow

The script suggests:

1. **Use template**: `cp templates/compression_checklist.md cip/cipXXXX-compression.md`
2. **Or run detailed check**: `./whats-next --compression-check`
3. **Follow the guide**: See [Compression Guide](compression-guide.md)

### How the Script Detects Compression Needs

The script scans all closed CIPs and checks:
- **Status**: Is the CIP closed?
- **Compressed field**: Is `compressed: false` or missing?
- **Age**: How many days since `last_updated`?

**Prioritization**:
- High-priority CIPs are flagged first
- Older CIPs are listed before newer ones
- Batch opportunities are highlighted

### Setting compressed: true

After compressing a CIP into formal documentation:

1. Update the CIP's YAML frontmatter: `compressed: true`
2. Commit the changes
3. The CIP will no longer appear in compression suggestions

**Example**:
```yaml
---
id: "0013"
status: "Closed"
compressed: true  # Marks as compressed
---
```

See [Compression Guide](compression-guide.md) for the complete workflow.

## For Developers

### Testing

The script includes unit tests to ensure its functionality. To run the tests:

```bash
# Run all tests (creates a virtual environment automatically)
./scripts/run-python-tests.sh

# Alternatively, run tests manually
source .venv/bin/activate
python -m pytest tests/
deactivate
```

### Project Structure

```
vibesafe/
├── scripts/
│   └── whats_next.py         # The main script
├── docs/
│   ├── whats_next_script.md  # This documentation
│   └── yaml_frontmatter_examples.md  # YAML examples
├── tests/
│   └── test_whats_next.py    # Test cases for the script
├── pyproject.toml            # Dependency and project configuration
├── .venv/                    # Virtual environment (created by install script)
├── whats-next                # Convenience wrapper script (created by install script)
└── install-whats-next.sh     # Installation script
```

### Extending the Script

The script is designed to be modular and extensible. If you want to add new functionality:

1. Add new functions in `scripts/whats_next.py`
2. Update the `generate_next_steps` function to include your new functionality
3. Add tests for your changes in `tests/test_whats_next.py`
4. Update this documentation as needed

## For LLMs

This script is particularly useful for LLMs working on the VibeSafe project, as it provides quick context about the project's current state and priorities. 

When an LLM is asked to work on VibeSafe, it should:

1. Run the "What's Next" script to get current project status
2. Review the recommended next steps
3. Understand the high-priority items
4. Check if there are files missing YAML frontmatter that need updating

This approach ensures that LLMs have the necessary context to make informed decisions about what tasks to prioritize. 