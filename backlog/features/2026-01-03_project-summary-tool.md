---
id: "2026-01-03_project-summary-tool"
title: "Phase 4: Create Project Summary Tool"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_yaml-frontmatter-standardization", "2026-01-03_simplify-requirements-framework", "2026-01-03_tenets-sustainability-process"]
related_cips: ["0011"]
related_requirements: ["REQ-005", "REQ-006"]
---

# Task: Phase 4: Create Project Summary Tool

## Description

Implement Phase 4 of CIP-0011: Create comprehensive project-summary tool that extends whats-next with requirements and tenets analysis. Includes recommendations engine and cross-reference validation.

This also partially implements REQ-006 (process conformance validation) through cross-reference checking.

## Acceptance Criteria

- [ ] Create scripts/project_summary.py (extends whats_next.py)
- [ ] Add YAML parsing for all component types
  - Requirements parsing and status analysis
  - Tenets parsing and review status
  - CIPs and backlog (extend existing whats-next)
- [ ] Add requirements analysis
  - Count by status
  - Identify oldest unaddressed
  - Check coverage (do all have CIPs?)
- [ ] Add tenets analysis
  - Identify tenets needing review
  - Detect conflicts (from conflicts_with field)
  - Show usage (which tenets referenced in CIPs?)
- [ ] Add cross-reference validation (REQ-006 partial implementation)
  - Validate requirements → CIPs → backlog links
  - Warn on broken references
  - Suggest fixes
- [ ] Add recommendations engine
  - Prioritize based on status, age, relationships
  - Identify blockers
  - Suggest next actions
- [ ] Create wrapper script ./project-summary
- [ ] Add command-line flags: --requirements, --tenets, --status, --quiet
- [ ] Update installation scripts to include tool
- [ ] Write tests for parsing and analysis logic

## Implementation Notes

**Relationship to whats-next**:
- whats-next: Quick check (git + backlog + CIPs)
- project-summary: Deep analysis (all components + recommendations)

Complement each other, both valuable.

## Related

- CIP: 0011
- Requirements: REQ-005, REQ-006 (partial)
- Depends on: Phases 0, 1, 3

## Progress Updates

### 2026-01-03
Task created. Requires Phases 0, 1, 3 completion.

