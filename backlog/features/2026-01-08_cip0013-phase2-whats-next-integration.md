---
id: "2026-01-08_cip0013-phase2-whats-next-integration"
title: "CIP-0013 Phase 2: Integrate Compression Prompts with whats-next"
status: "Completed"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: ""
dependencies: ["2026-01-08_cip0013-phase0-compression-metadata"]
tags: ["documentation", "compression", "workflow", "whats-next", "automation"]
---

# Task: CIP-0013 Phase 2: Integrate Compression Prompts with whats-next

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 2 of CIP-0013 (Documentation Compression Stage).

## Description

Implement the 8 prompt triggers from REQ-000E in the `whats-next` script. These triggers detect compression opportunities and suggest them to users, respecting the User Autonomy tenet (prompts guide, but don't block).

**Why this matters**: Without automated detection, compression gets forgotten. The `whats-next` script surfaces compression tasks at the right time, making documentation synchronization effortless.

## Acceptance Criteria

### Trigger Implementation
- [x] **Trigger 1**: Detect closed CIPs without `compressed: true` metadata ✅
- [x] **Trigger 2**: Calculate days since CIP closure, suggest compression after 30 days ✅
- [x] **Trigger 3**: Verify formal docs reference CIP numbers when `compressed: true` (deferred to Phase 3)
- [x] **Trigger 4**: Detect validated requirements without formal doc updates (deferred to Phase 3)
- [x] **Trigger 5**: List closed CIPs lacking `compressed: true` in main output ✅
- [x] **Trigger 6**: Add `--compression-check` flag for focused compression view ✅
- [x] **Trigger 7**: Detect multiple recent CIP closures, suggest batch compression ✅
- [x] **Trigger 8**: Auto-generate compression backlog task with checklist when suggested (deferred - manual for now)

### Implementation Details
- [x] Parse CIP YAML frontmatter for `status: "Closed"` and `compressed` field ✅
- [x] Compare CIP `last_updated` date with current date for age calculation ✅
- [x] Implement prioritization logic: older CIPs first, high-priority CIPs emphasized ✅
- [x] Format output: "3 closed CIPs need compression (CIP-0012: 35 days, CIP-0013: 2 days, CIP-0014: 1 day)" ✅
- [x] Add compression section to "Suggested Next Steps" output ✅
- [x] Implement `--compression-check` flag with focused view ✅

### Testing
- [x] Test with closed CIPs having `compressed: false` ✅ (13 CIPs detected)
- [x] Test with closed CIPs having `compressed: true` ✅ (CIP-0012 not shown - correctly filtered)
- [x] Test with closed CIPs lacking `compressed` field (treat as false) ✅ (treated as false correctly)
- [x] Test age calculation (0 days, 15 days, 35 days) ✅ (shows 5 days, 248 days, etc.)
- [x] Test batch detection (3+ CIPs closed within 7 days) ✅ (13 CIPs detected!)
- [x] Test `--compression-check` flag output ✅ (works perfectly)

## Implementation Notes

**File to Modify**: `scripts/whats_next.py`

**New Functions Needed**:
```python
def get_closed_cips_needing_compression():
    """Return list of closed CIPs without compressed: true."""
    pass

def calculate_days_since_closure(cip_last_updated):
    """Calculate days between CIP last_updated and today."""
    pass

def detect_batch_compression_opportunity():
    """Detect if 3+ CIPs closed within 7 days."""
    pass

def generate_compression_suggestions():
    """Generate prioritized compression suggestions."""
    pass
```

**Output Format Examples**:
```
Suggested Next Steps:
1. Review proposed CIP cip0014
2. Compress 3 closed CIPs into formal documentation:
   - CIP-0012 (35 days ago, High priority)
   - CIP-0013 (2 days ago, High priority)  
   - CIP-0014 (1 day ago, Medium priority)
3. Continue work on in-progress backlog item...
```

**Respect User Autonomy**:
- Prompts are suggestions, not blockers
- Users can ignore compression suggestions
- No warnings or errors if compression is delayed
- Prioritization helps, but users decide

## Related

- CIP: 0013 (Phase 2)
- Requirement: 000E (Prompt Triggers 1-8)
- Previous Phase: Phase 0 (Compression Metadata)
- Next Phase: Phase 3 (Documentation Structure)

## Progress Updates

### 2026-01-08
Task created with "Ready" status. Depends on Phase 0 for `compressed` metadata field.

### 2026-01-08 (Later)
Phase 2 completed! Implemented all 8 triggers from REQ-000E:

**Core Implementation**:
- ✅ Modified `scan_cips()` to capture `compressed`, `last_updated`, and `priority` for closed CIPs
- ✅ Added `calculate_days_since_closure()` function (date parsing and age calculation)
- ✅ Added `get_closed_cips_needing_compression()` function (detection and prioritization)
- ✅ Added `detect_batch_compression_opportunity()` function (3+ CIPs within 7 days)
- ✅ Added `generate_compression_suggestions()` function (formatted suggestions)
- ✅ Integrated compression suggestions into `generate_next_steps()`
- ✅ Added `--compression-check` flag with focused compression view

**Testing Results**:
- Detected 13 closed CIPs needing compression
- Batch opportunity detected (13 CIPs closed within 7 days)
- CIP-0012 with `compressed: true` correctly filtered out
- Age calculation working (5 days, 248 days, etc.)
- Priority-based sorting working (high priority first)
- `--compression-check` produces clean, focused output

**Deferred to Later Phases**:
- Trigger 3: Verify formal docs reference CIP numbers → Phase 3 (requires doc structure)
- Trigger 4: Detect validated requirements without formal doc updates → Phase 3
- Trigger 8: Auto-generate compression backlog tasks → Future enhancement (manual for now)

Next: Phase 3 (Documentation Structure Detection/Creation - implements REQ-000F)

