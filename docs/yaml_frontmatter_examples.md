# YAML Frontmatter Examples

This document provides examples of the standardized YAML frontmatter format for CIPs and backlog items.

## CIP Frontmatter Example

```yaml
---
id: "000A"
title: "Project Status Summarizer ('What's Next' Script)"
status: "proposed"
created: "2025-05-11"
last_updated: "2025-05-11"
author: "Neil Lawrence"
tags:
  - "project-management"
  - "automation"
  - "tooling"
---
```

### Required Fields for CIPs

- `id`: The CIP identifier (e.g., "0001", "000A")
- `title`: The title of the CIP
- `status`: One of "proposed", "accepted", "implemented", or "closed"
- `created`: The date the CIP was created (YYYY-MM-DD)
- `last_updated`: The date the CIP was last updated (YYYY-MM-DD)

### Optional Fields for CIPs

- `author`: The name of the CIP author
- `tags`: A list of relevant tags
- `related_cips`: A list of related CIP IDs
- `implementation_date`: The date the CIP was implemented (for implemented CIPs)
- `completion_date`: The date the CIP was closed (for closed CIPs)

## Backlog Item Frontmatter Example

```yaml
---
id: "2025-05-11_feature-x-implementation"
title: "Implement Feature X"
status: "proposed"
priority: "high"
created: "2025-05-11"
last_updated: "2025-05-11"
owner: "Neil Lawrence"
github_issue: 42
dependencies:
  - "2025-05-01_prerequisite-feature"
tags:
  - "feature"
  - "ui"
---
```

### Required Fields for Backlog Items

- `id`: The backlog item identifier (typically date-based: YYYY-MM-DD_short-description)
- `title`: The title of the backlog item
- `status`: One of "proposed", "ready", "in_progress", "completed", or "abandoned"
- `priority`: One of "high", "medium", or "low"
- `created`: The date the item was created (YYYY-MM-DD)
- `last_updated`: The date the item was last updated (YYYY-MM-DD)

### Optional Fields for Backlog Items

- `owner`: The person responsible for the task
- `github_issue`: The related GitHub issue number
- `dependencies`: A list of dependent item IDs
- `tags`: A list of relevant tags
- `completion_date`: The date the item was completed (for completed items)
- `related_cips`: CIP numbers related to this backlog item

## Using YAML Frontmatter

YAML frontmatter should be placed at the very beginning of the markdown file, enclosed between triple-dash lines (`---`). For example:

```markdown
---
id: "000A"
title: "Project Status Summarizer"
status: "proposed"
created: "2025-05-11"
last_updated: "2025-05-11"
---

# CIP-000A: Project Status Summarizer

## Status

- [x] Proposed: [2025-05-11]
- [ ] Accepted
- [ ] Implemented
- [ ] Closed

... rest of the CIP document ...
```

The frontmatter provides structured metadata that can be programmatically parsed, while the rest of the document maintains its readability and follows the established format.

## Migration Script

The "what's next" script will automatically detect files without proper YAML frontmatter and list them as action items. A migration script will be provided to help add frontmatter to existing CIPs and backlog items. 