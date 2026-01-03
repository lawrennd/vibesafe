---
id: "REQ-003"
title: "Accessible Guidance Without Prescriptive Structure"
status: "Ready"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["user-autonomy", "simplicity-of-use"]
related_cips: ["0011"]
related_backlog: []
stakeholders: ["developers", "vibesafe-users"]
tags:
  - guidance
  - documentation
  - user-autonomy
  - pedagogy
---

# REQ-003: Accessible Guidance Without Prescriptive Structure

## Description

VibeSafe should provide helpful guidance and thinking tools for requirements discovery without forcing that guidance into user project structure. Users should be able to access help when stuck, but shouldn't be required to adopt complex frameworks or processes.

Guidance should be available as reference material—like a textbook or handbook—that users consult when needed. It should not appear as mandatory subdirectories, templates, or process steps in user projects. This respects user autonomy while providing support when requested.

The guidance should cover common challenges: identifying stakeholders, decomposing goals, mapping constraints, and other requirements thinking tools.

## Acceptance Criteria

- [ ] Guidance materials are accessible and well-documented
- [ ] Users can find help when stuck on requirements
- [ ] Guidance is separate from user project structure
- [ ] AI assistants can reference guidance when appropriate
- [ ] Guidance doesn't create mandatory process or structure
- [ ] Examples show how to apply thinking tools to real requirements
- [ ] Users can ignore guidance without breaking their workflow

## Notes

**Design Principle**: Provide tools, not prescription.

**User Experience**:
- User creating requirements → Works in simple structure
- User gets stuck → "Not sure how to identify stakeholders"
- Cursor/AI → "Here's a thinking tool that might help: [link to guidance]"
- User reads guidance → Applies to their context
- User continues in simple structure (no new directories required)

**Guidance vs Structure**:
- **Good**: Reference documentation users consult
- **Bad**: Subdirectories users must populate
- **Good**: Optional thinking tools
- **Bad**: Mandatory process steps

