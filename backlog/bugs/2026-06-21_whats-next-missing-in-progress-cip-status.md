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
title: whats-next silently drops CIPs with status "In Progress"
---

# Task: whats-next silently drops CIPs with status "In Progress"

## Description

`scripts/whats_next.py` does not handle `in_progress` as a valid CIP status.
The `scan_cips()` function initialises `by_status` with only four keys
(`proposed`, `accepted`, `implemented`, `closed`) and the subsequent if/elif
chain has no `in_progress` branch. As a result, any CIP whose YAML frontmatter
contains `status: "In Progress"` is silently dropped — it appears in no
category in the output, and the suggestion engine never references it.

The bug manifests in two ways:

1. **Wrong normalisation**: `status` is extracted with `.lower()` (line ~463),
   which converts `"In Progress"` to `"in progress"` (with a space). The
   comparison checks for `'in_progress'` (with an underscore), so the match
   always fails even if a branch existed.

2. **Missing branch and bucket**: Even if normalisation were correct, there is
   no `'in_progress'` entry in the `by_status` dict and no `elif` branch to
   populate it — unlike backlog items, which do handle `in_progress`.

The display and suggestions sections already reference
`cips_info['by_status']['in_progress']` (line ~1413), but since the key is
never populated, nothing is ever shown.

## Acceptance Criteria

- [ ] `scan_cips()` initialises `by_status` with an `in_progress` key
- [ ] CIP status strings are normalised consistently (spaces → underscores,
      lowercase) before comparison — ideally using the existing
      `normalize_status()` helper, which already handles this correctly
- [ ] CIPs with `status: "In Progress"` are collected into `by_status['in_progress']`
      and displayed under an **In Progress** heading in the output
- [ ] The fallback (no-frontmatter) parsing path receives the same fix
- [ ] `whats-next` output and suggestions correctly reference in-progress CIPs
- [ ] Existing behaviour for `proposed`, `accepted`, `implemented`, and
      `closed` CIPs is unchanged
- [ ] Test or manual verification: a CIP with `status: "In Progress"` in
      frontmatter appears in the `whats-next` output

## Implementation Notes

In `scan_cips()`:

```python
# 1. Add in_progress bucket
'by_status': {
    'proposed': [],
    'accepted': [],
    'in_progress': [],   # add this
    'implemented': [],
    'closed': []
}

# 2. Use normalize_status() instead of .lower()
status = normalize_status(frontmatter.get('status', 'unknown'))

# 3. Add branch
elif status == 'in_progress':
    cips_info['by_status']['in_progress'].append({
        'id': file_id,
        'title': frontmatter.get('title', 'Untitled')
    })
```

Apply the same three changes to the fallback (no-frontmatter) code path.

In the display section, add an **In Progress** line between Accepted and
Implemented (consistent with backlog display order).

## Related

- Script: `scripts/whats_next.py`
- Reported while using tax-tools project (CIP-000A and CIP-000E both have
  `status: "In Progress"` and both disappear from output)

## Progress Updates

### 2026-06-21

Bug observed in tax-tools project. Two CIPs with `status: "In Progress"` in
frontmatter were not appearing in `whats-next` output, causing the suggestion
engine to keep recommending already-completed workflow steps.
