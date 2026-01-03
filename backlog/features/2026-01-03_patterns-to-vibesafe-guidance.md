---
id: "2026-01-03_patterns-to-vibesafe-guidance"
title: "Phase 2: Move Patterns to VibeSafe Guidance"
status: "Proposed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_simplify-requirements-framework"]
related_cips: ["0011"]
related_requirements: ["REQ-003"]
---

# Task: Phase 2: Move Patterns to VibeSafe Guidance

## Description

Implement Phase 2 of CIP-0011: Move patterns from ai-requirements/patterns/ to docs/patterns/ as VibeSafe-level guidance documentation. Update cursor rules to reference patterns as optional thinking tools, not required structure.

## Acceptance Criteria

- [ ] Create docs/patterns/ directory structure
- [ ] Move patterns from ai-requirements/patterns/ to docs/patterns/
  - stakeholder-analysis.md
  - goal-decomposition.md
  - (add constraint-mapping.md if needed)
- [ ] Create docs/patterns/README.md explaining patterns as thinking tools
  - Clarify: Patterns are VibeSafe guidance, not user project structure
  - Explain: Consult when stuck, not required process
  - Show: How to apply each pattern to requirements
- [ ] Add examples showing pattern application
- [ ] Update cursor rules to reference patterns as optional resources:
  - Add "Need Help Writing Requirements?" section
  - Link to VibeSafe patterns as reference material
  - Show as thinking tools to consult when stuck
- [ ] Remove patterns from user project templates
- [ ] Update documentation making clear patterns are VibeSafe-level

## Implementation Notes

**Key Message**: Patterns are teaching materials (like a textbook), not project structure (like directories you must create).

**User Experience**:
1. User creating requirements → Works in simple structure
2. User gets stuck → "Not sure how to break down this goal"
3. Cursor suggests → "See docs/patterns/goal-decomposition.md"
4. User reads, applies → Creates their requirements
5. No new directories required

## Related

- CIP: 0011
- Requirement: REQ-003
- Depends on: 2026-01-03_simplify-requirements-framework

## Progress Updates

### 2026-01-03
Task created. Depends on Phase 1 completion.

