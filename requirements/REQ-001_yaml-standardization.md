---
id: "REQ-001"
title: "Standardize YAML Frontmatter Across VibeSafe Components"
status: "Ready"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: ["0011"]
related_backlog: []
stakeholders: ["developers", "ai-assistants"]
tags:
  - standardization
  - yaml
  - metadata
  - tooling
---

# REQ-001: Standardized Component Metadata

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

**Component-Specific Extensions**:
- **CIP**: `author`, `related_cips`, `related_backlog`
- **Backlog**: `priority`, `category`, `owner`, `dependencies`
- **Requirements**: `priority`, `related_cips`, `related_backlog`, `stakeholders`
- **Tenets**: `last_reviewed`, `review_frequency`, `related_cips`, `conflicts_with`

Validation should be soft (warnings, not errors) to maintain flexibility.

