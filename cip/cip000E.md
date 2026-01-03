---
author: VibeSafe Team
created: '2025-07-26'
id: 000E
last_updated: '2025-07-26'
related_requirements:
- '0007'
status: Proposed
supersedes:
- CIP-0002
- CIP-000B
title: Clean Installation Philosophy for VibeSafe
---

# CIP-000E: Clean Installation Philosophy for VibeSafe

## Status

- [x] Proposed: 2025-07-26
- [x] Accepted: 2025-07-26
- [x] Implemented: 2025-07-26
- [x] Closed: 2025-07-28 (Fully implemented and tested)

## Description

This CIP establishes a simple, predictable installation philosophy for VibeSafe that treats every installation as a "reinstall" with clear separation between system files and user content.

## Motivation

The current installation approach (CIP-0002) has several problems:

1. *Inconsistent preservation logic* - Some files preserved, others overwritten
2. *Complex selective installation* - Users must choose components
3. *Confusing update behavior* - Unclear what gets updated vs preserved
4. *Maintenance burden* - Complex logic is hard to test and maintain

This creates confusion and makes VibeSafe installations unpredictable. Users don't know what will happen when they run the installer.

## Proposed Solution

### Core Philosophy: "Install = Reinstall"

Every VibeSafe installation should be treated as a complete reinstall of the VibeSafe system, with clear rules:

*✅ ALWAYS OVERWRITE (VibeSafe System Files):*
- Templates: `cip_template.md`, `task_template.md`, `tenet_template.md`
- System READMEs: `cip/README.md`, `backlog/README.md`, `tenets/README.md`
- Cursor rules: `.cursor/rules/*` 
- Installation scripts: `install-whats-next.sh`, `whats-next` wrapper
- AI-Requirements framework: All template and system files
- Index scripts: `update_index.py`, helper scripts

*✅ ALWAYS PRESERVE (User Content):*
- Project README: `README.md` (root level)
- User tasks: Files in `backlog/features/`, `backlog/bugs/`, etc.
- User CIPs: `cip0001.md`, `cip0002.md`, etc.
- User tenets: Actual project tenet files
- User virtual environment: `.venv` (user's project dependencies)
- User content in `ai-requirements/` (actual requirements documents)

*🔧 ALWAYS UPDATE (VibeSafe System):*
- VibeSafe virtual environment: `.venv-vibesafe` (VibeSafe's dependencies like PyYAML)

### Benefits

1. *Predictable* - Users know exactly what will happen
2. *Simple* - No complex detection or selective logic
3. *Always up-to-date* - System files always match latest VibeSafe
4. *Safe* - User content is never touched
5. *Easy to test* - Clear, simple behavior to verify

### Installation Behavior

```bash
# Simple installation - no options needed
./install-vibesafe.sh

# Always does the same thing:
# 1. Overwrites all VibeSafe system files  
# 2. Preserves all user content
# 3. Updates templates and tools to latest version
```

### File Classification

| File Type | Action | Example |
|-----------|--------|---------|
| *System Templates* | Overwrite | `task_template.md`, `cip_template.md` |
| *System Documentation* | Overwrite | `backlog/README.md`, `cip/README.md` |
| *Tool Configuration* | Overwrite | `.cursor/rules/*`, `update_index.py` |
| *Installation Scripts* | Overwrite | `whats-next`, `install-whats-next.sh` |
| *Project Documentation* | Preserve | `README.md` (root) |
| *User Content* | Preserve | `cip0001.md`, `backlog/features/task1.md` |

## Implementation

### 1. Update Installation Script

Simplify `scripts/install-minimal.sh`:

```bash
# Remove all selective installation logic
# Remove update/preserve detection 
# Clear rules: templates=overwrite, content=preserve

install_vibesafe() {
  echo "Installing VibeSafe (system files will be updated)..."
  
  # Always overwrite system files
  copy_system_templates
  copy_system_documentation  
  copy_cursor_rules
  install_whats_next_script
  
  # Preserve project README if it exists
  preserve_project_readme
  
  echo "VibeSafe installation complete!"
}
```

### 2. Update Documentation

- Update main README with simple installation instructions
- Remove complex selective installation documentation
- Document the clear preserve/overwrite rules

### 3. Simplify Testing

- Remove tests for selective installation
- Focus on preserve/overwrite behavior verification
- Test that user content is never touched

## Migration from CIP-0002

### Superseded Features

- *Selective installation* - Removed (install everything)
- *Update mode* - Removed (install = reinstall) 
- *Preserve customizations* - Clarified (only user content)

### Maintained Features

- *Cross-platform support* - Keep
- *Minimal dependencies* - Keep
- *Error handling* - Keep and simplify

## Implementation Status

- [x] Update `scripts/install-minimal.sh` with new philosophy
- [x] Simplify installation tests  
- [x] Update documentation
- [x] Mark CIP-0002 as superseded
- [x] Mark CIP-000B as superseded (update script no longer needed)
- [x] Update related backlog items

## References

- CIP-0002: VibeSafe Local Installation Method (superseded)
- CIP-000B: VibeSafe Update Script (superseded - redundant with Install = Reinstall)
- Current `scripts/install-minimal.sh` implementation

## Author and Date

- Author: VibeSafe Team
- Date: 2025-07-26