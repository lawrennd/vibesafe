---
id: "2026-06-13_cip0019-check-function"
title: "CIP-0019: Add check_cip_backlog_coverage() to validate_vibesafe_structure.py"
status: "Completed"
priority: "High"
created: "2026-06-13"
last_updated: "2026-06-13"
category: "features"
related_cips: ["0019"]
owner: "Neil Lawrence"
dependencies: []
tags:
  - backlog
  - validation
  - governance
---

# Task: Add `check_cip_backlog_coverage()` to validate_vibesafe_structure.py

## Description

Add a new cross-component validation function `check_cip_backlog_coverage()` to
`templates/scripts/validate_vibesafe_structure.py`.

The function:
1. Scans all CIP files for those with `status: Accepted` or `status: In Progress`
2. Scans all backlog task files collecting every `related_cips` reference
3. Emits a `result.add_warning()` for each active CIP not covered by any backlog task

Place the function after `check_governance_drift()` to maintain logical grouping.

## Acceptance Criteria

- [ ] Function `check_cip_backlog_coverage(root_dir, result)` exists in the template
- [ ] Emits a warning (not error) for each Accepted/In-Progress CIP with no backlog tasks
- [ ] Does NOT warn for CIPs with status Proposed, Implemented, or Closed
- [ ] Warning message names the CIP id, title, and explains the required action
- [ ] Uses existing helpers: `find_component_files()` and `extract_frontmatter()`
- [ ] Returns early (no warnings) when no active CIPs exist

## Implementation Notes

See the pseudocode in CIP-0019 `Detailed Description` → `Core algorithm` section
for the exact implementation pattern to follow.

## Related

- CIP: 0019
