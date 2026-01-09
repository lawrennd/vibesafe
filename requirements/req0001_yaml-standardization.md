---
created: '2026-01-03'
id: '0001'
last_updated: '2026-01-09'
priority: High
related_tenets:
  - effortless-context-restoration
  - simplicity-of-use
stakeholders:
- developers
- ai-assistants
status: Ready
tags:
- standardization
- yaml
- metadata
- tooling
title: Standardize YAML Frontmatter Across VibeSafe Components
---

# Requirement 0001: Standardized Component Metadata

## Description

VibeSafe components (CIPs, backlog tasks, requirements, tenets) should have consistent, machine-readable metadata that enables automated parsing, cross-referencing, and status tracking.

The metadata should be human-readable while supporting tooling. Components should share common fields (id, title, status, dates, tags) while allowing component-specific extensions. Cross-references between components should work bidirectionally.

This standardization is foundational for building unified tools, generating summaries, validating relationships, and understanding project state across all VibeSafe components.

## Acceptance Criteria

- [ ] All component types have consistent metadata structure
- [ ] Metadata is machine-parseable and human-readable
- [ ] Cross-references between components are bidirectional and validated
- [ ] Tools can automatically discover relationships between components
- [ ] Metadata schema is documented and examples provided
- [ ] Existing VibeSafe components use the standard metadata format

## Notes

**Common Fields** (all components):
- `id`: Unique identifier
- `title`: Human-readable title
- `status`: Current status
- `created`: Creation date (YYYY-MM-DD)
- `last_updated`: Last modification date (YYYY-MM-DD)
- `tags`: Array of categorization tags

**Component-Specific Extensions** (links bottom-up):
- **Requirements**: `priority`, `stakeholders`, `related_tenets`
- **CIP**: `author`, `related_requirements`, `related_cips`, `blocked_by`, `superseded_by`
- **Backlog**: `priority`, `category`, `owner`, `dependencies`, `related_cips`
- **Tenets**: `last_reviewed`, `review_frequency`, `conflicts_with`

**Linking Structure**: Each component references "up" the chain:
- Requirements → Tenets (WHY informs WHAT)
- CIPs → Requirements (WHAT informs HOW)
- Backlog → CIPs (HOW informs DO)
- Scripts query for inverse: "Which requirements relate to tenet X?"

Validation should be soft (warnings, not errors) to maintain flexibility.