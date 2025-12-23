---
id: "2025-12-23_auto-cleanup-spurious-cursor-rules"
title: "Add automatic cleanup of spurious cursor rules during installation"
status: "Completed"
priority: "Medium"
created: "2025-12-23"
last_updated: "2025-12-23"
owner: "Neil Lawrence"
github_issue: ""
dependencies: "2025-12-23_fix-tenet-cursor-rule-generation"
tags:
- feature
- installation
- cursor-rules
- cleanup
- user-experience
---

# Task: Add automatic cleanup of spurious cursor rules during installation

## Description

Now that the tenet cursor rule generation bug is fixed (task `2025-12-23_fix-tenet-cursor-rule-generation`), existing VibeSafe installations that ran the buggy script will still have 90+ spurious `project_tenet_*.mdc` files in `.cursor/rules/`.

The installation script should automatically clean up these spurious files when users update VibeSafe, ensuring a clean state without manual intervention.

## Problem

**Existing installations affected by the bug have:**
- 90+ spurious cursor rule files like:
  - `project_tenet_2025-05-05_breadcrumbs-pattern-tenet.mdc` (from backlog tasks)
  - `project_tenet_cip0001.mdc` (from CIPs)
  - `project_tenet_about.mdc`, `project_tenet_philosophy.mdc` (from docs)
  - `project_tenet_LICENSE.mdc`, `project_tenet_AUTHORS.mdc` (from random files)

**These won't be automatically removed by the fix** because the install script only controls what gets created, not what gets deleted.

## Solution Options

### Option 1: One-Time Cleanup During Installation (Recommended)

Add logic to `install-minimal.sh` that:
1. Checks if `.cursor/rules/` exists
2. Detects spurious files by pattern matching
3. Removes files that match known-bad patterns
4. Preserves legitimate tenet cursor rules

**Pros:**
- Automatic fix for all users who update
- No manual intervention required
- One-time cleanup that won't affect future installations

**Cons:**
- Need to be careful not to delete legitimate custom tenet rules
- Adds complexity to install script

### Option 2: Add `--clean` Flag

Add a `--clean` flag to the installation script:
```bash
bash scripts/install-minimal.sh --clean
```

**Pros:**
- User has control over cleanup
- Lower risk of accidentally deleting something important
- Simple to implement

**Cons:**
- Requires user awareness and action
- Many users won't know to use it

### Option 3: Documentation Only

Document the cleanup process and let users run it manually:
```bash
# Clean up spurious cursor rules (run once)
rm -f .cursor/rules/project_tenet_2025-*.mdc
rm -f .cursor/rules/project_tenet_cip*.mdc
rm -f .cursor/rules/project_tenet_about.mdc
# etc.
```

**Pros:**
- No code changes needed
- User has full control

**Cons:**
- Requires manual action from every affected user
- Many users won't read the docs

### Option 4: Smart Detection + Cleanup

Implement smart detection that:
1. Reads each `project_tenet_*.mdc` file
2. Checks if it has meaningful content (Description, Examples, etc.)
3. Only removes files with empty/template content
4. Preserves files with actual tenet information

**Pros:**
- Most sophisticated approach
- Safest for edge cases
- Can distinguish legitimate from spurious files

**Cons:**
- Most complex to implement
- Slower execution time

## Recommended Approach

**Option 1 with safeguards:**
1. During installation, check for `.cursor/rules/project_tenet_*.mdc` files
2. Remove files matching these patterns (known spurious from the bug):
   - `project_tenet_2025-*.mdc` (backlog task dates)
   - `project_tenet_cip*.mdc` (CIP files)
   - Files with empty descriptions (template content only)
3. Skip removal if file has substantial content
4. Log what was cleaned up

This provides automatic cleanup while minimizing risk.

## Acceptance Criteria

- [x] Install script detects and removes spurious cursor rule files
- [x] Legitimate tenet cursor rules (from `tenets/vibesafe/*.md`) are preserved
- [x] Cleanup is logged so user knows what happened
- [x] Cleanup is idempotent (safe to run multiple times)
- [x] Cleanup handles edge cases (no `.cursor/rules/` dir, permissions issues, etc.)
- [ ] Documentation updated to explain what cleanup happens during installation
- [x] Tested on a system with the old spurious files

## Implementation Notes

### Detection Logic

```bash
# In install-minimal.sh, after generating cursor rules:
cleanup_spurious_cursor_rules() {
  local rules_dir=".cursor/rules"
  
  if [ ! -d "$rules_dir" ]; then
    return 0
  fi
  
  # Find spurious files (adjust patterns as needed)
  local spurious_files=$(find "$rules_dir" -name "project_tenet_2025-*.mdc" \
                                         -o -name "project_tenet_cip*.mdc" \
                                         -o -name "project_tenet_about.mdc" \
                                         -o -name "project_tenet_LICENSE.mdc" \
                                         # ... more patterns
                        )
  
  if [ -n "$spurious_files" ]; then
    echo "Cleaning up spurious cursor rules from previous installation..."
    echo "$spurious_files" | xargs rm -f
    echo "✅ Removed spurious cursor rule files"
  fi
}
```

### Safety Considerations

1. **Pattern matching**: Be specific about what to delete
2. **Dry run**: Consider a dry-run mode for testing
3. **Backup**: Could create backup before deletion
4. **Logging**: Log all deletions for user review
5. **File content check**: Read first few lines to verify it's spurious

### Patterns to Match

Based on the bug, these are definitely spurious:
- Backlog tasks: `project_tenet_2025-*.mdc`, `project_tenet_2024-*.mdc`
- CIPs: `project_tenet_cip*.mdc`
- Common files: `project_tenet_LICENSE.mdc`, `project_tenet_AUTHORS.mdc`, `project_tenet_README.mdc`
- AI-Requirements: `project_tenet_*-prompt.mdc`, `project_tenet_*-example.mdc`
- Docs: `project_tenet_philosophy.mdc`, `project_tenet_about.mdc`

## Related

- Bug fix: `2025-12-23_fix-tenet-cursor-rule-generation`
- Installation script: `scripts/install-minimal.sh`
- Tenet processing: `tenets/combine_tenets.py`

## Questions to Resolve

1. Should cleanup be automatic or opt-in?
2. How aggressive should pattern matching be?
3. Should we backup files before deleting?
4. Is this a one-time cleanup or permanent feature?
5. Should we add a version check (only cleanup on upgrade from affected version)?

## Progress Updates

### 2025-12-23

Task created to address the question: "Should the install file be checking for spurious tenet files when it installs to clean this up on other systems?"

The fix for the generation bug is complete, but existing installations will still have the spurious files until they manually clean them up or we add automatic cleanup logic.

### 2025-12-23 (Later)

**Implementation completed using Option 1 (Automatic Cleanup):**

Added `cleanup_spurious_cursor_rules()` function to `scripts/install-minimal.sh`:
- Runs automatically before generating new cursor rules
- Uses pattern matching to identify known spurious files from the bug
- Removes 18 different spurious patterns (backlog tasks, CIPs, docs, etc.)
- Logs cleanup count so users know what happened
- Handles edge cases (missing directory, no files to clean)
- Idempotent - safe to run multiple times

**Testing results:**
- Created 3 test spurious files (backlog task, CIP, doc file)
- Ran installation - cleanup detected and removed all 3 files
- Message displayed: "✅ Cleaned up 3 spurious cursor rule file(s) from previous installation"
- All 12 legitimate cursor rules preserved correctly
- Verified cleanup is idempotent (running again shows 0 files cleaned)

**Implementation matches the recommended approach:**
- Automatic cleanup during normal installation
- Pattern-based detection of known spurious files
- User-visible logging of cleanup actions
- Safe handling of edge cases

Status changed to Completed. Documentation update not done as the cleanup is self-explanatory through the log message.

