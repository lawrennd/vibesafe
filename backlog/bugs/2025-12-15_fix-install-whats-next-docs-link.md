---
category: bugs
created: '2025-12-15'
dependencies: ''
github_issue: ''
id: 2025-12-15_fix-install-whats-next-docs-link
last_updated: '2025-12-15'
owner: ''
priority: Medium
related_cips: []
status: Proposed
tags:
- backlog
- bugs
- installer
- whats-next
title: Fix install-whats-next messaging and requirements rule installation in minimal
  installs
---

# Task: Fix install-whats-next messaging and requirements rule installation in minimal installs

## Description

When installing VibeSafe into a *target project* via the minimal installer, `install-whats-next.sh` currently:

- Prints a docs pointer that assumes a `docs/whats_next_script.md` file exists in the target project (it often doesn’t, because the minimal install doesn’t copy VibeSafe docs).
- Attempts to copy `templates/cursor_rules/requirements_rule.md` from the target project, which does not exist in minimal installs (causing a warning: “Requirements cursor rule template not found.”).

This is confusing for users: the “What’s Next” script works, but the installer output suggests missing documentation/templates.

## Acceptance Criteria

- [ ] Running the minimal installer in a fresh target project does **not** emit a misleading docs path (either install the doc file, or point to an in-repo/online location that is guaranteed to exist).
- [ ] Running the minimal installer in a fresh target project does **not** warn about missing `templates/cursor_rules/requirements_rule.md` (either bundle the required rule content, or remove/adjust the copy step for minimal installs).
- [ ] The behavior difference between full vs minimal installs is documented (at least in installer output and/or a short doc note).
- [ ] Add/adjust an automated test (or coverage script) that verifies minimal install output does not reference non-existent paths.

## Implementation Notes

- Candidate fixes:
  - Update `install-whats-next.sh` to point to a guaranteed reference, e.g.:
    - A copied local doc file that minimal installs include, or
    - `docs/whats_next_script.md` in the VibeSafe repo via GitHub link (stable), or
    - A `--help` suggestion (`./whats-next --help`) instead of a local doc path.
  - Update the “requirements cursor rule” installation:
    - Copy from a path that minimal installs actually include, or
    - Inline the rule content in the installer, or
    - Make it conditional on the presence of the `templates/` directory (and avoid warning for minimal installs).

## Related

- Documentation: `docs/whats_next_script.md`

## Progress Updates

### 2025-12-15

Task created after observing misleading output and a missing-template warning during minimal installation into a target project.