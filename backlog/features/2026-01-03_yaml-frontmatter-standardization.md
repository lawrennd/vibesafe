---
id: "2026-01-03_yaml-frontmatter-standardization"
title: "Phase 0: YAML Frontmatter Standardization"
status: "Completed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_process-conformance-validation"]
related_cips: ["0011"]
---

# Task: Phase 0: YAML Frontmatter Standardization

## Description

Implement Phase 0 of CIP-0011: Standardize YAML frontmatter across all VibeSafe component types (CIPs, backlog, requirements, tenets). This provides the foundation for automated tooling and cross-referencing.

This is the first phase because all other phases depend on consistent metadata structure.

## Acceptance Criteria

- [ ] Audit all existing templates (CIP, backlog, requirements, tenets)
- [ ] Define standard YAML fields for each component type
- [ ] Update all templates with consistent YAML frontmatter
- [ ] Update CIP template to reference source requirements
  - Add `related_requirements` field to YAML frontmatter
  - Add note: "CIPs describe HOW to achieve requirements (WHAT)"
  - Add prompt: "Which requirements does this CIP address?"
- [ ] Update backlog template to reference requirements and CIPs
  - Ensure `related_cips` and `related_requirements` fields exist
  - Add note: "Backlog tasks are DOING the work defined in requirements/CIPs"
- [ ] Add YAML validation to parsing scripts (soft validation - warnings)
- [ ] Document YAML schema for each component type
- [ ] Test: Existing components can be parsed with new schema
- [ ] **Run validation script**: `scripts/validate_vibesafe.py` should pass with no errors

## Implementation Notes

**Common Fields** (all components):
- `id`, `title`, `status`, `created`, `last_updated`, `tags`

**Component-Specific**:
- CIP: `author`, `related_requirements`, `related_cips`, `related_backlog`
- Backlog: `priority`, `category`, `owner`, `dependencies`, `related_cips`, `related_requirements`
- Requirements: `priority`, `stakeholders`, `related_cips`, `related_backlog`
- Tenets: `last_reviewed`, `review_frequency`, `related_cips`, `conflicts_with`

## Related

- CIP: 0011
- Requirement: REQ-001

## Progress Updates

### 2026-01-03
Task created. Proposed status.

