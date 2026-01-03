---
id: "2026-01-03_cip0011-documentation"
title: "Phase 5: CIP-0011 Documentation and Testing"
status: "Proposed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_simplify-requirements-framework", "2026-01-03_patterns-to-vibesafe-guidance", "2026-01-03_tenets-sustainability-process", "2026-01-03_project-summary-tool"]
related_cips: ["0011"]
related_requirements: ["REQ-001", "REQ-002", "REQ-003", "REQ-004", "REQ-005"]
---

# Task: Phase 5: CIP-0011 Documentation and Testing

## Description

Implement Phase 5 of CIP-0011: Update main documentation with simplified approach, integrate WHAT vs HOW distinction throughout, create migration guide, write tests, and create visual diagrams.

This is the final phase that ties everything together and ensures the new system is well-documented.

## Acceptance Criteria

- [ ] Update main README with new simplified approach
- [ ] Add WHAT vs HOW distinction to main documentation
  - Create dedicated section explaining the distinction
  - Show flow visually: WHAT → HOW → DO  
  - Provide examples from VibeSafe itself (dogfooding)
  - Link from all component READMEs back to core concept
- [ ] Document YAML frontmatter schema for all components
  - Common fields table
  - Component-specific extensions table
  - Examples for each component type
- [ ] Add examples using new format
  - Requirements examples (REQ-001 through REQ-006 already exist!)
  - Pattern examples in docs/patterns/
  - Tenet examples with review metadata
- [ ] Create migration guide for existing projects
  - How to migrate from ai-requirements to requirements/
  - How to add YAML frontmatter to existing components
  - How to establish tenet review process
- [ ] Write tests for project_summary.py
- [ ] Update cursor rules with WHAT vs HOW guidance
  - Add to vibesafe_general.mdc
  - Include decision tree for AI assistants
  - Examples: "User asks for feature" → "Create requirement (WHAT) first"
- [ ] Create visual diagram showing component relationships
  - WHAT (Requirements) → HOW (CIPs) → DO (Backlog) flow
  - Tenets (WHY) informing all decisions
  - Patterns as optional guidance layer

## Implementation Notes

**Documentation Goals**:
1. Make WHAT vs HOW distinction obvious and pervasive
2. Show VibeSafe using VibeSafe (dogfooding examples)
3. Provide clear migration path for existing users
4. Ensure AI assistants understand the principles

**Visual Diagram Ideas**:
- Flow diagram: Requirement → CIP → Backlog → Implementation
- Layer diagram: Tenets (foundation) → Components (structure) → Patterns (guidance)
- Decision tree: "Creating something?" → WHAT/HOW/DO decision points

## Related

- CIP: 0011
- Requirements: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005
- Depends on: All other phases

## Progress Updates

### 2026-01-03
Task created. Final phase - integrates everything.

