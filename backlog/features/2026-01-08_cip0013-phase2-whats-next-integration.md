---
id: "2026-01-08_cip0013-phase2-whats-next-integration"
title: "CIP-0013 Phase 2: Integrate Compression Prompts with whats-next"
status: "Ready"
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
- [ ] **Trigger 1**: Detect closed CIPs without `compressed: true` metadata
- [ ] **Trigger 2**: Calculate days since CIP closure, suggest compression after 30 days
- [ ] **Trigger 3**: Verify formal docs reference CIP numbers when `compressed: true`
- [ ] **Trigger 4**: Detect validated requirements without formal doc updates
- [ ] **Trigger 5**: List closed CIPs lacking `compressed: true` in main output
- [ ] **Trigger 6**: Add `--compression-check` flag for focused compression view
- [ ] **Trigger 7**: Detect multiple recent CIP closures, suggest batch compression
- [ ] **Trigger 8**: Auto-generate compression backlog task with checklist when suggested

### Implementation Details
- [ ] Parse CIP YAML frontmatter for `status: "Closed"` and `compressed` field
- [ ] Compare CIP `last_updated` date with current date for age calculation
- [ ] Implement prioritization logic: older CIPs first, high-priority CIPs emphasized
- [ ] Format output: "3 closed CIPs need compression (CIP-0012: 35 days, CIP-0013: 2 days, CIP-0014: 1 day)"
- [ ] Add compression section to "Suggested Next Steps" output
- [ ] Implement `--compression-check` flag with focused view:
  ```bash
  ./whats-next --compression-check
  # Output:
  # Compression Candidates (3):
  #   CIP-0012: 35 days since closure (High priority)
  #   CIP-0013: 2 days since closure (High priority)
  #   CIP-0014: 1 day since closure (Medium priority)
  ```

### Testing
- [ ] Test with closed CIPs having `compressed: false`
- [ ] Test with closed CIPs having `compressed: true` (should not prompt)
- [ ] Test with closed CIPs lacking `compressed` field (treat as false)
- [ ] Test age calculation (0 days, 15 days, 35 days)
- [ ] Test batch detection (3+ CIPs closed within 7 days)
- [ ] Test `--compression-check` flag output

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

