---
created: '2026-01-03'
id: '0004'
last_updated: '2026-01-03'
priority: Medium
related_backlog: ["2026-01-03_tenets-sustainability-process"]
related_cips: ["0004", "0011"]
related_tenets: []
stakeholders:
- project-teams
- maintainers
status: Ready
tags:
- tenets
- sustainability
- relevance
- maintenance
title: Sustainable and Relevant Tenets
---

# Requirement 0004: Sustainable and Relevant Tenets

## Description

Tenets should remain relevant and aligned with actual project practices throughout the project lifecycle. They should be living documents that evolve with the project, not static rules that drift from reality.

The system should support periodic review to ensure tenets still reflect project values. When projects deviate from a tenet, there should be a way to learn from that (maybe the tenet needs updating, or maybe the decision needs reconsidering). Conflicts between tenets should be identifiable so they can be resolved.

Tenets should have clear review cycles, usage tracking (which tenets actually inform decisions?), and lifecycle management (active, under review, archived).

## Acceptance Criteria

- [ ] Tenets have defined review cycles and last-reviewed dates
- [ ] Process exists for reviewing tenet relevance periodically
- [ ] Tenets can be updated or archived when no longer relevant
- [ ] Conflicts between tenets are detectable
- [ ] Usage tracking shows which tenets inform actual decisions
- [ ] Deviations from tenets can be documented and learned from
- [ ] Tenet lifecycle is clear (active, under review, archived)
- [ ] Review process is lightweight (10-15 minutes per review)

## Notes

**Building on CIP-0004**: This requirement builds on the basic tenet system implemented in CIP-0004. CIP-0004 provided the foundational structure (templates, documentation, VibeSafe's own tenets, combine_tenets.py). This requirement adds lifecycle management and sustainability features.

**Sustainability Principle**: Tenets should evolve with the project, not become stale dogma.

**Review Triggers**:
- Scheduled (quarterly, annual based on frequency)
- Deviation detected (project consistently violates a tenet)
- Conflict detected (two tenets suggest opposite decisions)
- Low usage (tenet never referenced in decisions)

**Learning from Deviations**:
When we violate a tenet, document:
- What decision was made
- Why we deviated
- Was it justified (tenet needs update) or mistake (recommit to tenet)?

This creates feedback loop for tenet improvement.