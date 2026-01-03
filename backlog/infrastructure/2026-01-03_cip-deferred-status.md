---
id: "2026-01-03_cip-deferred-status"
title: "Add Deferred Status for CIPs"
status: "Completed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "infrastructure"
related_cips: ["0011"]
owner: "Neil Lawrence"
---

# Task: Add Deferred Status for CIPs

## Description

Update the validation script to allow "Deferred" as a valid CIP status, enabling CIPs to be marked as postponed or blocked by other work.

This extends CIP-0011's YAML standardization to include a status for CIPs that are good ideas but blocked or deprioritized.

## Acceptance Criteria

- [x] Update `scripts/validate_vibesafe_structure.py` to allow "Deferred" in CIP allowed_status list
- [x] Update `templates/scripts/validate_vibesafe_structure.py` (template version) similarly
- [x] Document `blocked_by` field (optional, stores CIP ID that blocks this one)
- [x] Document `superseded_by` field (optional, stores CIP ID that replaces this one)
- [x] Valid CIP statuses: `['Proposed', 'Accepted', 'In Progress', 'Implemented', 'Closed', 'Rejected', 'Deferred']`
- [x] `blocked_by` and `superseded_by` are optional string fields (CIP IDs like "0011")
- [x] Validation passes on test cases
- [x] Update CIP template to mention new status and fields

## Implementation Notes

**Changes needed in validation script:**

```python
'cip': {
    'id_format': 'XXXX (4-digit hex)',
    'required_fields': ['id', 'title', 'status', 'created', 'last_updated'],
    'optional_fields': ['author', 'related_requirements', 'related_cips', 'blocked_by', 'superseded_by', 'tags'],
    'allowed_status': ['Proposed', 'Accepted', 'Implemented', 'Closed', 'Rejected', 'Deferred'],
    'links_to': ['related_requirements'],
    'should_not_have': ['related_backlog'],
},
```

**When to use each status:**
- **Deferred**: Good idea but blocked or deprioritized (use `blocked_by` to reference blocker)
- **Rejected**: Will not be implemented (use `superseded_by` if replaced by another CIP)

## Related

- **CIP**: 0011 (Phase 0 - YAML standardization)
- **Blocker**: None (ready to implement)

## Dependencies

- CIP-0011 (defines the need for this status)

## Progress Updates

### 2026-01-03
Task created as part of CIP-0011 implementation. Currently breaks validation until implemented.

