---
id: "0007"
title: "Automatic System Updates on Installation"
status: "Ready"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["clean-installation"]
related_cips: ["000E", "0011"]
related_backlog: []
stakeholders: ["vibesafe-users", "existing-projects"]
tags:
  - installation
  - updates
  - migration
  - backwards-compatibility
---

# Requirement 0007: Automatic System Updates on Installation

## Description

When users install or update VibeSafe, system file changes should automatically propagate to their projects without breaking existing work. Users should get the latest templates, cursor rules, scripts, and documentation while preserving their actual content (requirements, CIPs, backlog tasks, tenets, code).

This follows the Clean Installation Philosophy tenet: "Every installation is a reinstallation. System files updated, user content preserved." The system should be smart enough to:
- Update templates and cursor rules to latest versions
- Migrate deprecated structures (e.g., ai-requirements/ → requirements/)
- Preserve all user-created content
- Provide clear communication about what changed

Users shouldn't need to manually update templates or cursor rules when VibeSafe evolves.

## Acceptance Criteria

- [ ] Running install script updates all VibeSafe system files to latest versions
- [ ] User content is never overwritten or deleted
- [ ] Deprecated structures trigger automatic migration (with user notification)
- [ ] Migration is idempotent (safe to run multiple times)
- [ ] Clear messages explain what was updated and why
- [ ] Rollback is possible if migration fails
- [ ] Migration preserves all metadata and relationships
- [ ] Post-migration validation ensures nothing broken
- [ ] Documentation explains what happens during install/update

## Notes

**Examples from CIP-0011**:

When users update VibeSafe after CIP-0011 implementation:
1. **Templates updated**: requirements, CIP, backlog templates get new YAML fields
2. **Cursor rules updated**: requirements_rule.mdc gets simplified version
3. **Structure migration**: ai-requirements/ content → requirements/ (if present)
4. **New scripts added**: project-summary, validation scripts
5. **User content untouched**: Their actual requirements, CIPs, tasks preserved

**What NOT to migrate automatically**:
- User's actual requirements files (they control format)
- User's specific customizations
- Project-specific configuration

**Philosophy Balance**:
- Aggressive: Update all system files
- Conservative: Preserve all user content
- Smart: Detect and migrate deprecated patterns
- Clear: Communicate what changed

This requirement ensures VibeSafe can evolve without abandoning existing users.

