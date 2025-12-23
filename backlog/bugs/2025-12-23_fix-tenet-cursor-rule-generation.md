---
id: "2025-12-23_fix-tenet-cursor-rule-generation"
title: "Fix overly broad tenet-to-cursor-rule generation in installation script"
status: "Proposed"
priority: "High"
created: "2025-12-23"
last_updated: "2025-12-23"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ""
tags:
- bug
- installation
- cursor-rules
- tenets
- system-files
---

# Task: Fix overly broad tenet-to-cursor-rule generation in installation script

## Description

The installation script (`scripts/install-minimal.sh`) is generating cursor rules from **every file in the project** instead of just actual tenets. This creates 90+ spurious `project_tenet_*.mdc` files in `.cursor/rules/` that include:

- Backlog tasks (e.g., `project_tenet_2025-05-05_breadcrumbs-pattern-tenet.mdc`)
- CIP files (e.g., `project_tenet_cip0001.mdc`)
- Documentation files (e.g., `project_tenet_about.mdc`, `project_tenet_philosophy.mdc`)
- AI-requirements files
- Random project files (e.g., `project_tenet_LICENSE.mdc`, `project_tenet_AUTHORS.mdc`)

These are not actual tenets and should not be converted to cursor rules.

## Root Cause

In `scripts/install-minimal.sh` line 442, the script calls:

```bash
.venv/bin/python tenets/combine_tenets.py --generate-cursor-rules --tenets-dir . --output-dir .cursor/rules
```

The problem is `--tenets-dir .` which treats the **entire project directory** as the tenets directory, causing `combine_tenets.py` to process all markdown files in the project.

It should be:

```bash
.venv/bin/python tenets/combine_tenets.py --generate-cursor-rules --tenets-dir tenets --output-dir .cursor/rules
```

## Impact

- **Cursor IDE clutter**: 90+ irrelevant cursor rules that pollute the rules system
- **Performance**: Extra files for Cursor to load and process
- **Confusion**: Rules like "Project Tenet: 2025-05-05_breadcrumbs-pattern-tenet" with no content
- **Misleading**: These appear to be tenets but are actually backlog tasks, CIPs, etc.

## Expected Cursor Rules

The `.cursor/rules/` directory should only contain:

**VibeSafe System Rules:**
- `backlog.mdc`
- `cip.mdc`
- `requirements_rule.mdc`
- `vibesafe_general.mdc`
- `whats_next.mdc`

**Actual Project Tenets (if any):**
- Generated from files in `tenets/vibesafe/*.md` only
- Example: `project_tenet_user-autonomy.mdc`, `project_tenet_simplicity-of-use.mdc`, etc.

## Acceptance Criteria

- [ ] Fix `scripts/install-minimal.sh` to use `--tenets-dir tenets` instead of `--tenets-dir .`
- [ ] Clean up all spurious `project_tenet_*.mdc` files from `.cursor/rules/`
- [ ] Verify that only actual tenets from `tenets/vibesafe/*.md` generate cursor rules
- [ ] Test that reinstallation doesn't recreate the spurious files
- [ ] Update templates/scripts/install-minimal.sh with the same fix
- [ ] Document what cursor rules should be present in VibeSafe projects

## Implementation Notes

### Fix Steps

1. **Update install-minimal.sh (both locations)**
   - Line 442 in `scripts/install-minimal.sh`
   - Same line in `templates/scripts/install-minimal.sh` (if exists)
   - Change: `--tenets-dir .` → `--tenets-dir tenets`

2. **Clean up spurious files**
   ```bash
   # Remove all project_tenet_* files except actual tenets
   cd .cursor/rules
   # Keep only legitimate tenet cursor rules from tenets/vibesafe/
   # Delete everything else starting with project_tenet_
   ```

3. **Verify combine_tenets.py behavior**
   - Ensure it only processes files in the specified tenets directory
   - Check if it has any hardcoded assumptions about project structure

4. **Test the fix**
   ```bash
   # Clean install
   rm -rf .cursor/rules/project_tenet_*
   bash scripts/install-minimal.sh
   # Verify only legitimate files are created
   ls .cursor/rules/
   ```

### Investigation Needed

- [ ] What files should `combine_tenets.py` process?
- [ ] Should it process subdirectories of `tenets/`?
- [ ] How does it distinguish between actual tenets and other markdown files?
- [ ] Are there supposed to be project_tenet files for actual tenets?
- [ ] Should VibeSafe's own tenets generate cursor rules?

## Related

- Installation script: `scripts/install-minimal.sh`
- Tenet processing: `tenets/combine_tenets.py`
- Cursor rules documentation: `.cursor/rules/`
- CIP-000E: Clean Installation Philosophy

## Progress Updates

### 2025-12-23

Task created after discovering 90+ spurious cursor rule files in `.cursor/rules/` directory during documentation update work. The installation script is processing the entire project directory instead of just the `tenets/` directory when generating cursor rules.

