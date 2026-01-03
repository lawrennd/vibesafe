---
id: "0005"
title: "Clear Understanding of Project Status"
status: "Ready"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: ["0011"]
related_backlog: []
stakeholders: ["developers", "project-managers", "ai-assistants"]
tags:
  - visibility
  - status
  - understanding
  - context
---

# Requirement 0005: Clear Understanding of Project Status

## Description

Users and LLMs should be able to quickly understand the current state of a project across all VibeSafe components: requirements, tenets, CIPs, and backlog. This understanding should be accessible in a single view without manually checking multiple directories.

The system should provide both quick status checks (what's happening now?) and deeper analysis (what should I do next?). Status should include not just current work, but also the health of requirements (any unaddressed?), tenets (any need review?), and relationships (are requirements linked to implementation?).

Intelligent recommendations based on project state would help users prioritize work and identify issues before they become problems.

## Acceptance Criteria

- [ ] Single command provides comprehensive project status
- [ ] Status covers all components (requirements, tenets, CIPs, backlog, git)
- [ ] Requirements status is visible (count by status, age, coverage)
- [ ] Tenet health is visible (review status, conflicts, usage)
- [ ] Relationships are validated (requirements → CIPs → backlog)
- [ ] Recommendations suggest next actions based on project state
- [ ] Quick status available without detailed analysis
- [ ] Tool is fast (< 2 seconds for typical project)
- [ ] Output is readable by both humans and AI assistants

## Notes

**User Experience Goal**:
- "What should I work on next?" → Run one command → See prioritized recommendations
- "Are all requirements addressed?" → See at a glance
- "Do any tenets need review?" → Visible in summary
- "What's blocking progress?" → Identified automatically

**Status Dimensions**:
- **Requirements**: How many? What status? Any stalled?
- **Tenets**: How many? Need review? Conflicts detected?
- **CIPs**: Current status of designs
- **Backlog**: Active work items
- **Relationships**: Are requirements connected to implementation?

**Quick vs Deep**:
- Quick: Current work (what's next?)
- Deep: Full analysis (where are we? what's next? any issues?)

