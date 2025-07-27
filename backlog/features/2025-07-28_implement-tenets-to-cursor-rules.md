---
id: "2025-07-28_implement-tenets-to-cursor-rules"
title: "Implement Automatic Tenets-to-Cursor-Rules Generation"
status: "Ready"
priority: "High"
created: "2025-07-28"
last_updated: "2025-07-28"
category: "features"
---

# Task: Implement Automatic Tenets-to-Cursor-Rules Generation

## Description

Implement the automatic generation of Cursor AI rules from project tenets during VibeSafe installation, as specified in CIP-0010. This feature will scan for existing project tenets and automatically create corresponding cursor rules to ensure AI assistance aligns with project-specific guiding principles.

## Acceptance Criteria

- [ ] Extend `tenets/combine_tenets.py` to support cursor rule generation
- [ ] Create tenet-to-cursor-rule template system with proper `.mdc` format
- [ ] Add tenet discovery functionality to find project-specific tenets (not just VibeSafe tenets)
- [ ] Integrate tenet processing into `scripts/install-minimal.sh` installation flow
- [ ] Implement rule naming convention (`project_tenet_[tenet-id].mdc`) to avoid conflicts
- [ ] Add preservation logic to never overwrite existing project-specific cursor rules
- [ ] Handle malformed tenet files gracefully with appropriate error messages
- [ ] Add comprehensive test coverage for all tenet discovery and rule generation scenarios
- [ ] Update installation tests to verify tenet-to-rule generation works correctly
- [ ] Update documentation to explain the new automatic rule generation feature

## Implementation Notes

### Key Technical Requirements:

1. *Tenet Discovery*: Look for tenets in `tenets/` directory structure, not just `tenets/vibesafe/`
2. *Metadata Extraction*: Use existing `combine_tenets.py` logic to parse tenet files
3. *Rule Generation*: Create valid `.mdc` files with proper YAML frontmatter
4. *Conflict Resolution*: Ensure generated rules don't conflict with VibeSafe system rules
5. *Installation Integration*: Add to `install_vibesafe()` function in installation script

### Testing Scenarios:

- Installation with existing project tenets
- Installation with no tenets
- Installation with malformed tenet files
- Reinstallation with new tenets added
- Conflict resolution with existing cursor rules
- Preservation of user-modified generated rules

### Dependencies:

- CIP-0010: Automatic Tenets-to-Cursor-Rules Generation (Proposed)
- Existing `tenets/combine_tenets.py` functionality
- `scripts/install-minimal.sh` installation script

## Related

- CIP: 0010 