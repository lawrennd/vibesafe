---
id: "2026-01-03_document-status-workflow-whats-next"
title: "Document Status Workflow and What's Next Script Logic"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "documentation"
related_cips: ["0011"]
---

# Task: Document Status Workflow and What's Next Script Logic

## Description

Create comprehensive documentation explaining how statuses work across all VibeSafe components (CIPs, Requirements, Backlog, Tenets) and how the `whats-next` script uses these statuses to generate actionable suggestions.

This documentation should serve as the authoritative reference for:
- Valid status values for each component type
- Status workflow (transitions)
- How `whats-next` interprets statuses to suggest next actions
- When to use which status

## Acceptance Criteria

- [ ] Document created explaining all status workflows
- [ ] Cover all component types: CIPs, Requirements, Backlog, Tenets
- [ ] Explain status transitions (workflow diagrams)
- [ ] Document how `whats-next` uses each status
- [ ] Provide examples of when to use each status
- [ ] Cross-reference with validation script allowed values
- [ ] Include decision trees for status selection
- [ ] Document the relationship between component statuses (e.g., Requirement → CIP → Backlog)

## Implementation Notes

**Location:** Create `docs/status_workflows.md`

**Content Structure:**

### 1. Component Status Reference

**CIPs:**
```
Valid Statuses: Proposed, Accepted, In Progress, Implemented, Closed, Rejected, Deferred
Workflow: Proposed → Accepted → In Progress → Implemented → Closed
          └→ Rejected (won't implement)
          └→ Deferred (postponed, use blocked_by field)

What's Next Logic:
- Proposed: "Review proposed CIP - should it be accepted or is it a requirement?"
- Accepted: "Break down into actionable backlog tasks"
- In Progress: "Continue implementing CIP backlog tasks"
- Implemented: "Verify implementation; consider closing"
- Closed: No action (complete)
- Rejected: No action
- Deferred: No action (revisit when blocker resolved)
```

**Requirements:**
```
Valid Statuses: Proposed, Refined, Ready, In Progress, Implemented, Validated, Deferred, Rejected
Workflow: Proposed → Refined → Ready → In Progress → Implemented → Validated
          └→ Rejected (won't implement)
          └→ Deferred (postponed)

What's Next Logic:
- Proposed/Refined: "Refine requirement X with acceptance criteria"
- Ready: "Create CIP to implement requirement X"
- In Progress: "Continue requirement implementation"
- Implemented: "Validate requirement X against acceptance criteria"
- Validated: No action (complete)
```

**Backlog:**
```
Valid Statuses: Proposed, Ready, In Progress, Completed, Abandoned
Workflow: Proposed → Ready → In Progress → Completed
          └→ Abandoned (won't do, with explanation)

What's Next Logic:
- Proposed: Listed in proposed section
- Ready: Listed in ready section, suggested for high-priority
- In Progress: "Continue work on in-progress item X"
- Completed: No action (filtered out)
- Abandoned: No action (filtered out)
```

**Tenets:**
```
Valid Statuses: Active, Under Review, Archived
Workflow: Active → Under Review → Active (updated)
          └→ Archived (no longer applicable)

What's Next Logic:
- Active: Check last_reviewed date, suggest review if overdue
- Under Review: "Complete tenet review for X"
- Archived: No action
```

### 2. Status Transition Decision Trees

**When to move CIP from Accepted → In Progress:**
- Backlog tasks have been created
- Work has actively begun
- At least one backlog task is "In Progress"

**When to move CIP from In Progress → Implemented:**
- All backlog tasks are "Completed"
- Code changes are complete
- Tests are passing
- Ready for verification

**When to move CIP from Implemented → Closed:**
- Implementation has been verified
- All acceptance criteria met
- Documentation updated
- No outstanding issues

### 3. Cross-Component Status Relationships

**Example Flow:**
```
Tenet: "simplicity-of-use" (Active)
   ↓ informs
Requirement: REQ-000A "Minimal Footprint" (Ready)
   ↓ implemented by
CIP: CIP-000F "Auto-Gitignore" (In Progress)
   ↓ broken into
Backlog: "Phase 1: Core Protection" (Completed)
Backlog: "Phase 2: Documentation" (In Progress)
```

**Status Synchronization:**
- When all CIP backlog tasks → Completed: CIP → Implemented
- When CIP → Closed: Requirement → Implemented
- When all requirement CIPs → Closed: Requirement → Validated

### 4. What's Next Suggestion Priority

**Priority Order:**
1. Validation errors (highest priority)
2. Proposed CIPs needing review (WHAT vs HOW check)
3. Accepted CIPs without backlog tasks
4. In-progress CIPs with backlog tasks
5. In-progress backlog items
6. High-priority backlog items
7. Git uncommitted changes

## Related

- **CIP**: 0011 (defines YAML frontmatter and status fields)
- **Script**: `scripts/whats_next.py` (implements the logic)
- **Validator**: `scripts/validate_vibesafe_structure.py` (enforces allowed values)

## Dependencies

- CIP-0011 Phase 0 (YAML standardization)
- Backlog tasks: 2026-01-03_cip-in-progress-status, 2026-01-03_cip-deferred-status

## Progress Updates

### 2026-01-03
Task created to document the status workflow system and how `whats-next` interprets it.

