---
title: "Ensure combine_tenets.py Includes Cursor Rules Generation Functionality"
id: "2025-07-28_vibesafe-combine-tenets-cursor-rules"
status: "proposed"
priority: "medium"
created: "2025-07-28"
updated: "2025-07-28"
owner: "Neil"
dependencies: ["2025-07-28_vibesafe-combine-tenets-project-detection"]
category: "infrastructure"
---

# Task: Ensure combine_tenets.py Includes Cursor Rules Generation Functionality

## Description

The `install-minimal.sh` script expects `combine_tenets.py` to support the `--generate-cursor-rules` flag for generating cursor rules from project tenets, but the current version in some projects doesn't have this functionality. This creates a mismatch between what the installation script expects and what's actually provided.

## Current Issue

The `install-minimal.sh` script includes a function `generate_tenet_cursor_rules()` that attempts to use `combine_tenets.py` with cursor rules generation:

```bash
# Run tenet processing with Python
.venv/bin/python tenets/combine_tenets.py --generate-cursor-rules --tenets-dir . --output-dir .cursor/rules
```

However, the `combine_tenets.py` script in some projects (like The Inaccessible Game) doesn't include this functionality, causing:
- Silent failures during installation
- Missing cursor rules generation
- Incomplete VibeSafe setup

## Acceptance Criteria

### 1. Cursor Rules Generation Support
- [ ] Script supports `--generate-cursor-rules` flag
- [ ] Script accepts `--tenets-dir` and `--output-dir` parameters
- [ ] Generates `.mdc` files in `.cursor/rules/` directory

### 2. Tenet Metadata Extraction
- [ ] Extracts tenet metadata from YAML frontmatter
- [ ] Handles both old and new tenet formats
- [ ] Robust parsing with error handling

### 3. Cursor Rule Template
- [ ] Generates properly formatted cursor rules
- [ ] Includes tenet title, description, and examples
- [ ] Follows VibeSafe's cursor rule format

### 4. Integration with Installation Script
- [ ] Works seamlessly with `install-minimal.sh`
- [ ] Handles virtual environment activation
- [ ] Provides clear error messages on failure

## Implementation Notes

### Required Functionality
The script should include these functions from VibeSafe's advanced version:

```python
def extract_tenet_metadata_for_cursor_rules(content):
    """Extract metadata from tenet content for cursor rules."""
    # Parse YAML frontmatter
    # Extract title, description, examples, etc.
    pass

def generate_cursor_rule_content(metadata):
    """Generate cursor rule content from tenet metadata."""
    # Format as cursor rule
    # Include tenet information
    pass

def generate_cursor_rules_from_tenets(tenets_directory, output_directory):
    """Generate cursor rules from project tenets."""
    # Find all tenet files
    # Extract metadata
    # Generate cursor rules
    pass
```

### Command Line Interface
```python
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-cursor-rules', action='store_true',
                       help='Generate cursor rules from tenets')
    parser.add_argument('--tenets-dir', default='.',
                       help='Directory containing tenets')
    parser.add_argument('--output-dir', default='.cursor/rules',
                       help='Output directory for cursor rules')
    
    args = parser.parse_args()
    
    if args.generate_cursor_rules:
        generate_cursor_rules_from_tenets(args.tenets_dir, args.output_dir)
    else:
        # Original tenet combination behavior
        pass
```

### Error Handling
- Graceful handling of missing tenet files
- Clear error messages for parsing failures
- Fallback behavior when cursor rules generation fails

## Related Work

- **VibeSafe Repository**: https://github.com/lawrennd/vibesafe
- **Advanced Script Location**: `$HOME/lawrennd/vibesafe/tenets/combine_tenets.py`
- **Installation Script**: `scripts/install-minimal.sh`
- **Related Task**: "Make combine_tenets.py Project-Agnostic Instead of Hardcoded for 'vibesafe'"

## Testing Requirements

### Test Scenarios
- [ ] Test with VibeSafe's own tenets (should work as before)
- [ ] Test with The Inaccessible Game tenets (new format)
- [ ] Test with missing tenet files (error handling)
- [ ] Test with malformed tenet files (robust parsing)

### Expected Output
- [ ] Cursor rules generated in `.cursor/rules/` directory
- [ ] Files named `project_tenet_{tenet_id}.mdc`
- [ ] Proper formatting for Cursor AI consumption

## Impact

### Benefits
- **Complete VibeSafe Setup**: Installation script works as expected
- **AI Integration**: Cursor rules enable AI assistance with project tenets
- **Consistent Experience**: All VibeSafe projects get cursor rule generation

### Risks
- **Complexity**: Adds significant functionality to a simple script
- **Dependencies**: Requires YAML parsing and file system operations
- **Maintenance**: More complex script requires more testing

## Success Metrics

- [ ] `install-minimal.sh` successfully generates cursor rules
- [ ] Cursor rules are properly formatted and functional
- [ ] No errors during VibeSafe installation process
- [ ] Backward compatibility maintained with existing tenet formats

## Implementation Priority

This task should be implemented **after** the project detection task, as both improvements should be made together to ensure a complete solution. 