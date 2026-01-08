---
id: "2026-01-08_cip0013-phase4-workflow-integration"
title: "CIP-0013 Phase 4: Integrate Compression into VibeSafe Workflow"
status: "Ready"
priority: "Medium"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: ""
dependencies: ["2026-01-08_cip0013-phase1-compression-checklist"]
tags: ["documentation", "compression", "workflow"]
---

# Task: CIP-0013 Phase 4: Integrate Compression into VibeSafe Workflow

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 4 of CIP-0013 (Documentation Compression Stage).

## Description

Integrate the compression stage into VibeSafe's core workflow documentation and AI assistant prompts. Ensure AI assistants understand compression as a natural breakpoint and guide users through it.

**Why this matters**: Compression is a new stage in the WHY→WHAT→HOW→DO→DOCUMENT flow. Documentation and AI prompts must reflect this to guide users effectively.

## Acceptance Criteria

- [ ] Update CIP workflow documentation to include compression step
- [ ] Add compression as natural breakpoint in `templates/.cursor/rules/cip.mdc`:
  ```
  6. ✋ After CIP closure (status: Closed)
     → Pause: Compression opportunity - update formal docs?
  ```
- [ ] Update VibeSafe General Development Guidelines (Section 7: Documentation Lifecycle):
  - [ ] Add "Phase 4: Compression" to the three-phase model
  - [ ] Update workflow diagram to show compression stage
- [ ] Create example compression commits for reference:
  - [ ] Example 1: Infrastructure CIP compression
  - [ ] Example 2: Feature CIP compression
  - [ ] Example 3: Process CIP compression
- [ ] Update README.md to mention compression stage in workflow overview
- [ ] Document compression in "Why the Process?" section of README

## Implementation Notes

**Workflow Diagram Update**:
```
WHY (Tenets)
  ↓ informs
WHAT (Requirements) 
  ↓ guides
HOW (CIPs)
  ↓ breaks into
DO (Backlog)
  ↓ produces
CODE (Implementation)
  ↓ validates & compresses into
DOCUMENT (Formal Docs)  ← NEW STAGE
  ↓ feedback loop
WHY (validates alignment with tenets)
```

**Natural Breakpoint Addition** (for AI assistants):
```markdown
### 9. Natural Breakpoints for AI Assistants

5. ✋ After validation (status: Implemented → Closed)
   → Done: CIP complete, commit and celebrate!

6. ✋ After CIP closure (status: Closed) ← NEW
   → Pause: Ask user about compression
   → Suggest: "CIP-XXXX is closed. Compress into formal docs now or defer?"
   → Options: Compress now, create compression task, defer
```

**Example Compression Commit Messages**:
```bash
# Good compression commit
git commit -m "Compress CIP-0012 into formal documentation

Added to README:
- Multi-platform AI assistant support overview

Added to docs/architecture.md:
- Platform-agnostic prompt generation architecture
- Design rationale: single source of truth approach

Marked CIP-0012 compressed: true"

# Another example
git commit -m "Compress CIP-0013: Documentation compression stage

Updated README: Added compression to workflow diagram
Updated docs/: Created compression-guide.md
Marked CIP-0013 compressed: true

Closes compression of CIP-0013"
```

**AI Prompt Integration**:
Update AI assistant context files to recognize compression as a workflow stage and prompt appropriately.

## Related

- CIP: 0013 (Phase 4)
- Requirement: 000E (Documentation Synchronization)
- Previous Phase: Phase 1 (Compression Checklist)
- Next Phase: Phase 5 (Periodic Review)

## Progress Updates

### 2026-01-08
Task created with "Ready" status. Depends on Phase 1 for example checklists.

