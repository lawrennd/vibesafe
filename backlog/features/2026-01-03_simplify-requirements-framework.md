---
id: "2026-01-03_simplify-requirements-framework"
title: "Phase 1: Requirements Framework Simplification"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_yaml-frontmatter-standardization"]
related_cips: ["0011"]
related_requirements: ["REQ-002"]
---

# Task: Phase 1: Requirements Framework Simplification

## Description

Implement Phase 1 of CIP-0011: Replace complex ai-requirements framework with simple requirements/ directory. Update cursor rules and documentation to reflect new approach with emphasis on WHAT vs HOW distinction.

## Acceptance Criteria

- [ ] requirements/ directory structure complete (already dogfooded!)
- [ ] requirements/README.md documents WHAT vs HOW distinction clearly
  - Explain: Requirements = WHAT (outcomes), CIPs = HOW (design), Backlog = DO (execution)
  - Show flow: Requirement → CIP → Backlog Task → Implementation
  - Provide examples of good requirements vs implementation details
  - Add decision guide: "Am I describing WHAT or HOW?"
- [ ] templates/requirements/requirement_template.md created
- [ ] Migrate existing VibeSafe requirements to new format
  - REQ-001 (vibesafe-core) → new format
  - REQ-002 (ai-requirements-framework) → new format  
  - REQ-003 (integration-requirements) → new format
- [ ] Update cursor rules (templates/.cursor/rules/requirements_rule.mdc):
  - Change glob from ai-requirements to requirements
  - Remove complex framework description
  - Add WHAT vs HOW guidance section
  - Add simple requirements format documentation
  - Keep status sync table
- [ ] Archive ai-requirements framework with deprecation notice
- [ ] Create migration guide for existing projects

## Implementation Notes

**WHAT vs HOW Examples** (from VibeSafe itself):
- ✅ Good: "Requirements framework should be simple" (outcome)
- ❌ Bad: "Replace ai-requirements with requirements/ directory" (implementation)
- CIP-0011 shows HOW to achieve the outcome

**Migration Strategy**:
- Keep old ai-requirements for now (deprecated)
- Add deprecation notice in ai-requirements/README.md
- Update docs to point to new requirements/

## Related

- CIP: 0011
- Requirement: REQ-002
- Depends on: 2026-01-03_yaml-frontmatter-standardization

## Progress Updates

### 2026-01-03
Task created. Depends on Phase 0 completion.

