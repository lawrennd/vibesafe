# VibeSafe Requirements

This directory contains requirements for VibeSafe itself. Requirements define **WHAT** needs to be built.

## Format

Each requirement uses YAML frontmatter for metadata and a simple structure:

```yaml
---
id: "REQ-XXX"
title: "Requirement Title"
status: "Proposed|Ready|In Progress|Implemented|Validated"
priority: "High|Medium|Low"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
related_tenets: ["tenet-id"]  # WHY: Which tenets inform this requirement?
related_cips: ["XXXX"]  # HOW: Which CIPs implement this?
related_backlog: ["YYYY-MM-DD_task-name"]  # DO: Which tasks execute this?
stakeholders: ["group1", "group2"]
tags:
  - tag1
  - tag2
---

# REQ-XXX: Requirement Title

## Description
Brief description of what needs to be built (2-3 paragraphs max)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes (Optional)
Any additional context
```

## Status Values

- **Proposed**: Initial requirement, needs refinement
- **Ready**: Fully defined, ready for implementation
- **In Progress**: Currently being implemented
- **Implemented**: Code complete, needs validation
- **Validated**: Implementation verified against acceptance criteria

## File Naming

Requirements are named: `REQ-XXX_short-description.md`

Examples:
- `REQ-001_yaml-standardization.md`
- `REQ-002_simplify-requirements.md`

## Integration

Requirements connect tenets (WHY) to implementation (HOW/DO):

```
Tenets (WHY) → Requirements (WHAT) → CIP (HOW) → Backlog Task (DO) → Implementation
```

**Linking Structure** (bottom-up):
- Requirements reference `related_tenets` (WHY informs WHAT)
- CIPs reference `related_requirements` (WHAT informs HOW)
- Backlog tasks reference `related_cips` (HOW informs DO)
- Scripts query inverse: "Which requirements relate to this tenet?"

This creates bidirectional traceability while keeping each component focused on its immediate context.

## Need Help?

VibeSafe provides thinking tools for requirements discovery in the main documentation. These are reference materials to consult when stuck, not mandatory process steps.

