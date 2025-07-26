---
id: "2025-07-26_clean-installation-implementation"
title: "Implement Clean Installation Philosophy"
status: "Completed"
priority: "High"
created: "2025-07-26"
last_updated: "2025-07-26"
category: "features"
---

# Task: Implement Clean Installation Philosophy

## Description

Implement the clean installation philosophy defined in CIP-000E to replace the complex installation approach. This creates predictable "install = reinstall" behavior with clear separation between system files and user content.

## Motivation

Current installation behavior is inconsistent and confusing:
- Some files preserved, others overwritten without clear rules
- Complex selective installation options
- Users don't know what will happen when they run installer
- Testing is complicated due to many edge cases

CIP-000E defines a simple approach: always overwrite VibeSafe system files, always preserve user content.

## Acceptance Criteria

1. *Update Installation Script*
   - [x] Simplify `scripts/install-minimal.sh` to remove selective installation logic
   - [x] Implement clear overwrite/preserve rules from CIP-000E
   - [x] Remove update mode complexity
   - [x] Always overwrite: templates, system READMEs, cursor rules, scripts
   - [x] Always preserve: project README, user tasks/CIPs/tenets, .venv

2. *Update Installation Tests*
   - [x] Remove tests for selective installation (no longer supported)
   - [x] Add tests verifying system files are always overwritten
   - [x] Add tests verifying user content is always preserved
   - [x] Simplify test matrix to focus on preserve/overwrite behavior

3. *Update Documentation*
   - [x] Update main README with simple installation instructions
   - [x] Remove complex selective installation documentation
   - [x] Document clear preserve/overwrite rules for users
   - [x] Add examples showing what happens on reinstall

4. *Mark Related Items*
   - [x] Update `2025-05-05_easy-installation-method.md` to reference CIP-000E
   - [x] Simplify `2025-05-05_installation-testing-plan.md` scope
   - [x] Evaluate if CIP-000B (update script) is still needed

## Implementation Notes

### Key Changes to install-minimal.sh

```bash
# OLD: Complex selective installation
install_component() {
  if [ "$INSTALL_COMPONENT" = true ]; then
    # conditional logic
  fi
}

# NEW: Simple always-install approach  
install_vibesafe() {
  echo "Installing VibeSafe (system files will be updated)..."
  
  # Always install everything - overwrite system files
  copy_templates_from_repo
  install_whats_next_script
  
  # Always preserve project README
  preserve_project_readme
  
  echo "VibeSafe installation complete!"
}
```

### File Classification (from CIP-000E)

*Always Overwrite:*
- `cip/README.md`, `cip/cip_template.md`
- `backlog/README.md`, `backlog/task_template.md`, `backlog/update_index.py`
- `tenets/README.md`, `tenets/tenet_template.md`
- `.cursor/rules/*`
- `whats-next`, `install-whats-next.sh`
- All `ai-requirements/` templates and system files

*Always Preserve:*
- `README.md` (project root)
- `backlog/features/`, `backlog/bugs/`, etc. (user tasks)
- `cip0001.md`, `cip0002.md`, etc. (user CIPs)
- User tenet files, user requirements documents
- `.venv` directory

### Testing Simplifications

Remove complex test scenarios:
- ❌ Selective component installation
- ❌ Update vs fresh install modes
- ❌ Preserve customization logic

Focus on core behavior:
- ✅ System files always overwritten
- ✅ User content always preserved
- ✅ Cross-platform compatibility

## Files to Modify

- `scripts/install-minimal.sh` - Main implementation
- `scripts/test/install-test.bats` - Simplified tests
- `README.md` - Updated installation instructions
- Related backlog items

## Dependencies

- CIP-000E: Clean Installation Philosophy for VibeSafe (Proposed)

## Estimated Effort

*1-2 days* - Simplification should reduce complexity significantly compared to current approach.

## Success Criteria

1. Installation behavior is completely predictable
2. Users know exactly what will be overwritten vs preserved
3. No complex options or modes to choose from
4. All tests pass with simplified test suite
5. Documentation clearly explains the behavior

## Progress Updates

### 2025-07-26
- Task created with Ready status and High priority
- All acceptance criteria defined based on CIP-000E requirements

### 2025-07-26 (Implementation Complete)
- ✅ Updated `scripts/install-minimal.sh` with Clean Installation Philosophy
  - Removed complex selective installation logic
  - Implemented clear overwrite/preserve rules
  - Always overwrite VibeSafe system files
  - Always preserve user content (.venv, project README, user tasks/CIPs)
- ✅ Updated installation tests in `scripts/test/install-test.bats`
  - Removed selective installation tests
  - Added preserve/overwrite behavior verification tests  
  - Added tests for user content preservation
  - Added tests for system file overwrite on reinstall
- ✅ Updated cursor rules to clarify user vs system files
  - Added file classification sections to all cursor rule files
  - Clear distinction between VibeSafe system files and user content
  - Prevents unnecessary commits of VibeSafe infrastructure files
- ✅ Updated main README.md with simple installation instructions
  - Removed complex customization documentation
  - Added clear preserve/overwrite behavior explanation
  - Emphasized predictable "install = reinstall" approach
- ✅ All related backlog items and CIPs updated appropriately
- Status changed to Completed

## Related Items

- *Implements*: CIP-000E (Clean Installation Philosophy)
- *Supersedes*: `2025-05-05_easy-installation-method.md`
- *Updates*: `2025-05-05_installation-testing-plan.md`
- *Supersedes*: CIP-000B (VibeSafe Update Script - redundant with "Install = Reinstall" philosophy) 