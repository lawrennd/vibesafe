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

Make sure the script is executable:

```bash
chmod +x scripts/whats_next.py
```

## Requirements

- Python 3.6+
- PyYAML library (`pip install pyyaml`)

## Usage

Run the script from the root directory of the VibeSafe repository:

```bash
python scripts/whats_next.py
```

### Command Line Options

The script supports several command line options:

- `--no-git`: Skip Git status information
- `--no-color`: Disable colored output
- `--cip-only`: Only show CIP information
- `--backlog-only`: Only show backlog information
- `--quiet`: Suppress all output except next steps

Examples:

```bash
# Show only the next steps (useful for quick reference)
python scripts/whats_next.py --quiet

# Focus only on CIPs
python scripts/whats_next.py --cip-only

# Focus only on backlog items
python scripts/whats_next.py --backlog-only

# Disable color (useful for non-interactive terminals)
python scripts/whats_next.py --no-color
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

## YAML Frontmatter

The script checks for and recommends adding YAML frontmatter to CIPs and backlog items. See [YAML Frontmatter Examples](yaml_frontmatter_examples.md) for the required format.

## For LLMs

This script is particularly useful for LLMs working on the VibeSafe project, as it provides quick context about the project's current state and priorities. 

When an LLM is asked to work on VibeSafe, it should:

1. Run the "What's Next" script to get current project status
2. Review the recommended next steps
3. Understand the high-priority items
4. Check if there are files missing YAML frontmatter that need updating

This approach ensures that LLMs have the necessary context to make informed decisions about what tasks to prioritize. 