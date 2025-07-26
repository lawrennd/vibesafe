---
id: "2025-07-26_clean-installation-implementation"
title: "Implement Clean Installation Philosophy"
status: "Ready"
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

1. **Update Installation Script**
   - [ ] Simplify `scripts/install-minimal.sh` to remove selective installation logic
   - [ ] Implement clear overwrite/preserve rules from CIP-000E
   - [ ] Remove update mode complexity
   - [ ] Always overwrite: templates, system READMEs, cursor rules, scripts
   - [ ] Always preserve: project README, user tasks/CIPs/tenets, .venv

2. **Update Installation Tests**
   - [ ] Remove tests for selective installation (no longer supported)
   - [ ] Add tests verifying system files are always overwritten
   - [ ] Add tests verifying user content is always preserved
   - [ ] Simplify test matrix to focus on preserve/overwrite behavior

3. **Update Documentation**
   - [ ] Update main README with simple installation instructions
   - [ ] Remove complex selective installation documentation
   - [ ] Document clear preserve/overwrite rules for users
   - [ ] Add examples showing what happens on reinstall

4. **Mark Related Items**
   - [ ] Update `2025-05-05_easy-installation-method.md` to reference CIP-000E
   - [ ] Simplify `2025-05-05_installation-testing-plan.md` scope
   - [ ] Evaluate if CIP-000B (update script) is still needed

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

**Always Overwrite:**
- `cip/README.md`, `cip/cip_template.md`
- `backlog/README.md`, `backlog/task_template.md`, `backlog/update_index.py`
- `tenets/README.md`, `tenets/tenet_template.md`
- `.cursor/rules/*`
- `whats-next`, `install-whats-next.sh`
- All `ai-requirements/` templates and system files

**Always Preserve:**
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

**1-2 days** - Simplification should reduce complexity significantly compared to current approach.

## Success Criteria

1. Installation behavior is completely predictable
2. Users know exactly what will be overwritten vs preserved
3. No complex options or modes to choose from
4. All tests pass with simplified test suite
5. Documentation clearly explains the behavior

## Related Items

- **Implements**: CIP-000E (Clean Installation Philosophy)
- **Supersedes**: `2025-05-05_easy-installation-method.md`
- **Updates**: `2025-05-05_installation-testing-plan.md`
- **Evaluates**: CIP-000B (VibeSafe Update Script - may no longer be needed) 