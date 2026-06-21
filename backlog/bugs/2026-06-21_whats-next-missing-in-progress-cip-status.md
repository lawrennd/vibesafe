---
category: bugs
created: '2026-06-21'
dependencies: ''
github_issue: ''
id: 2026-06-21_whats-next-missing-in-progress-cip-status
last_updated: '2026-06-21'
owner: 'Neil Lawrence'
priority: High
related_cips: []
status: Proposed
tags:
- backlog
- bugs
- whats-next
- cip-status
title: 'Inconsistency between CIP status checklist and official status values'
---

# Task: Inconsistency between CIP status checklist and official status values

## Description

The CIP template body (`cip_template.md`) includes five status checkboxes:

```
- [ ] Proposed
- [ ] Accepted
- [ ] In Progress
- [ ] Implemented
- [ ] Closed
```

But the cursor rule guidance (`cip.mdc`, "Status Tracking" section) lists only
four valid frontmatter status values:

```
Proposed → Accepted → Implemented → Closed
```

"In Progress" appears in the template body but not in the authoritative
guidance. This creates two downstream problems:

1. **User confusion**: the template body implies "In Progress" is a valid
   frontmatter `status:` value, leading users (and AI assistants) to set
   `status: "In Progress"` in frontmatter.

2. **Dead code in whats-next**: `scripts/whats_next.py` already references
   `cips_info['by_status']['in_progress']` in the suggestions section
   (line ~1413), but `scan_cips()` never populates that key — it only handles
   `proposed`, `accepted`, `implemented`, `closed`. If "In Progress" is not
   a valid frontmatter status this is dead code; if it is valid, it is a bug.

## Decision Required

Before implementing a fix, decide whether "In Progress" should be:

**Option A — Remove it**: Drop the checkbox from the template body and remove
the dead `in_progress` reference from the script. The four-status model
(`Proposed → Accepted → Implemented → Closed`) is the intended workflow.
`Accepted` covers the period when implementation is actively underway.

**Option B — Adopt it**: Make "In Progress" an official fifth frontmatter
status, add it to the cursor rule, and fix `scan_cips()` to handle it.

## Acceptance Criteria

*(After the decision above is made)*

**If Option A:**
- [ ] Remove "In Progress" checkbox from `cip_template.md` status section
- [ ] Remove `in_progress` dead-code reference from `scripts/whats_next.py`
- [ ] Cursor rule remains unchanged (already correct)

**If Option B:**
- [ ] Add "In Progress" to `cip.mdc` Status Tracking section
- [ ] `scan_cips()` initialises `by_status` with an `in_progress` key
- [ ] CIP status strings normalised with `normalize_status()` (not `.lower()`)
      so "In Progress" → `in_progress` correctly
- [ ] Display and suggestions sections handle `in_progress` CIPs
- [ ] Fallback (no-frontmatter) parsing path updated consistently

## Related

- Template: `cip/cip_template.md`
- Rule: `.cursor/rules/cip.mdc`
- Script: `scripts/whats_next.py` (line ~463 for parsing, ~1413 for suggestions)
- Reported via tax-tools project where `status: "In Progress"` was set on a
  CIP frontmatter and the CIP disappeared from `whats-next` output

## Progress Updates

### 2026-06-21

Discovered while using the tax-tools project. A CIP with `status: "In Progress"`
in frontmatter disappeared from `whats-next` output. Investigation revealed the
template body and cursor rule guidance are inconsistent, and the script has dead
code referencing `in_progress`. The correct fix depends on a design decision
about whether the five-status or four-status model is intended.
