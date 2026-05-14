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

## Extending whats-next with Local Hooks

Projects can extend `whats-next` output with project-specific sections and
next-step suggestions without modifying any VibeSafe system files (CIP-0017).

### Activation

Create `.vibesafe/whats_next_local.py` in your project root. VibeSafe
discovers and loads it automatically on every `./whats-next` run. No
installation step is required. A documented template stub is provided at:

```
templates/.vibesafe/whats_next_local.py.example
```

Copy and rename it to get started:

```bash
cp templates/.vibesafe/whats_next_local.py.example .vibesafe/whats_next_local.py
```

### Hook functions

The local module may define either or both of the following functions.
Both are optional — omitting them is equivalent to returning an empty list.

#### `get_local_sections(context) -> list`

Called twice per run to inject custom output sections at controlled positions:

- **First call** with `context["position"] = "before"` — sections are rendered
  *before* all VibeSafe built-in sections. Use for urgent project-wide alerts
  or blockers that must be seen first.
- **Second call** with `context["position"] = "after"` — sections are rendered
  *after* all VibeSafe sections. Use for supplementary project information.

Each returned item is either:

| Format | Position |
|--------|----------|
| `(title, lines)` | "after" (default) |
| `(title, lines, "before")` | before built-in sections |
| `(title, lines, "after")` | after built-in sections |

where `title` is a `str` and `lines` is a `list[str]` of content lines.

#### `get_local_next_steps(context) -> list`

Called once per run to inject additional items into the "Suggested Next Steps"
list.

| Format | Position in output |
|--------|--------------------|
| `str` | appended after VibeSafe suggestions |
| `("low", str)` | appended after VibeSafe suggestions |
| `("high", str)` | prepended *before* VibeSafe suggestions |

Use `"high"` for urgent, project-specific concerns (e.g. "pipeline failed",
"deadline today") that must be seen before VibeSafe housekeeping items.

### Context dictionary

Both hooks receive the same `context` dict:

| Key | Type | Description |
|-----|------|-------------|
| `git_info` | `dict` | Output of `get_git_status()` |
| `cips_info` | `dict` | Output of `scan_cips()` |
| `backlog_info` | `dict` | Output of `scan_backlog()` |
| `requirements_info` | `dict` | Output of `scan_requirements()` |
| `args` | `argparse.Namespace` | CLI arguments (e.g. `args.quiet`) |

`get_local_sections()` additionally receives `context["position"]` set to
`"before"` or `"after"` for the current call. The dict is read-only from the
hook's perspective; mutations have no effect on the core script.

### Error handling

Errors in the local module are caught and reported as warnings — they never
crash `whats-next`. Import errors are caught at load time; runtime errors inside
each hook are caught per-call. The rest of the output is always produced.

### Example (data science project)

```python
# .vibesafe/whats_next_local.py
from pathlib import Path
from datetime import datetime, timedelta

def get_local_sections(context):
    sections = []
    position = context.get("position", "after")

    if position == "before":
        if Path(".ci-failing").exists():
            sections.append(("CI FAILING", ["  Fix CI before merging."], "before"))

    if position == "after":
        data_dir = Path("data/processed")
        if data_dir.exists():
            stale = [
                f for f in data_dir.glob("*.parquet")
                if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime))
                   > timedelta(days=7)
            ]
            lines = [f"  - {f.name}" for f in stale] or ["  All datasets are fresh."]
            sections.append(("Data Freshness", lines))
    return sections

def get_local_next_steps(context):
    steps = []
    if not Path("results/latest_run.json").exists():
        steps.append(("high", "Run the pipeline: make run"))
    if Path("tmp/").exists():
        steps.append("Clean up tmp/: rm -rf tmp/")
    return steps
```

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