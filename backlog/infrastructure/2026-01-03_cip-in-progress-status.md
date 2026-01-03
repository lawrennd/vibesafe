---
id: "2026-01-03_cip-in-progress-status"
title: "Add In Progress Status for CIPs"
status: "Proposed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "infrastructure"
related_cips: ["0011"]
owner: "Neil Lawrence"
---

# Task: Add In Progress Status for CIPs

## Description

Update the validation script to allow "In Progress" as a valid CIP status, enabling clearer tracking of CIPs that are actively being implemented.

This extends CIP-0011's YAML standardization to include a status for CIPs that have moved beyond acceptance and are actively being worked on.

## Acceptance Criteria

- [ ] Update `scripts/validate_vibesafe_structure.py` to allow "In Progress" in CIP allowed_status list
- [ ] Update `templates/scripts/validate_vibesafe_structure.py` (template version) similarly
- [ ] Valid CIP statuses: `['Proposed', 'Accepted', 'In Progress', 'Implemented', 'Closed', 'Rejected', 'Deferred']`
- [ ] "In Progress" indicates active implementation work
- [ ] Validation passes on test cases
- [ ] Update CIP template to mention new status

## Implementation Notes

**Changes needed in validation script:**

```python
'cip': {
    'id_format': 'XXXX (4-digit hex)',
    'required_fields': ['id', 'title', 'status', 'created', 'last_updated'],
    'optional_fields': ['author', 'related_requirements', 'related_cips', 'blocked_by', 'superseded_by', 'tags'],
    'allowed_status': ['Proposed', 'Accepted', 'In Progress', 'Implemented', 'Closed', 'Rejected', 'Deferred'],
    'links_to': ['related_requirements'],
    'should_not_have': ['related_backlog'],
},
```

**When to use each status:**
- **Proposed**: Initial idea
- **Accepted**: Approved, ready to start
- **In Progress**: Actively being implemented
- **Implemented**: Work complete (awaiting verification)
- **Closed**: Verified and complete
- **Rejected**: Will not be implemented
- **Deferred**: Good idea but blocked or deprioritized

## Related

- **CIP**: 0011 (Phase 0 - YAML standardization)
- **Also**: 2026-01-03_cip-deferred-status (adding Deferred status)

## Dependencies

- CIP-0011 (defines the need for this status)

## Progress Updates

### 2026-01-03
Task created as part of CIP-0011 implementation. CIP-0011 itself is now using "In Progress" status.

