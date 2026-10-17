# VibeSafe YAML Frontmatter Schema

This document defines the standard YAML frontmatter schema for all VibeSafe components.

## File Naming Conventions

| Component | File Pattern | ID Pattern | Example File | Example ID |
|-----------|--------------|------------|--------------|------------|
| **Requirement** | `reqXXXX_short-name.md` | `"XXXX"` | `req0001_yaml-standardization.md` | `"0001"` |
| **CIP** | `cipXXXX.md` or `cipXXXX_short-name.md` | `"XXXX"` | `cip0011.md`, `cip0011_component-management.md` | `"0011"` |
| **Backlog** | `YYYY-MM-DD_short-name.md` | `"YYYY-MM-DD_short-name"` | `2026-01-03_yaml-frontmatter.md` | `"2026-01-03_yaml-frontmatter"` |
| **Tenet** | `short-name.md` | `"short-name"` | `simplicity-of-use.md` | `"simplicity-of-use"` |

### Naming Rules

- **Requirements**: 4-digit hexadecimal (0001-FFFF), lowercase, short name required
- **CIPs**: 4-digit hexadecimal (0001-FFFF), lowercase, short name optional
- **Backlog**: Date-based (YYYY-MM-DD), lowercase, short name required
- **Tenets**: Descriptive kebab-case name, lowercase

## YAML Frontmatter Fields

### Common Fields (All Components)

```yaml
id: "unique-identifier"       # Required: Component's unique ID
title: "Human-readable title"  # Required: Descriptive title
status: "Current status"       # Required: Component state
created: "YYYY-MM-DD"          # Required: Creation date
last_updated: "YYYY-MM-DD"     # Required: Last modification date
tags: []                       # Optional: List of tags
```

### Component-Specific Fields

#### Requirements

```yaml
id: "0001"                     # 4-digit hex
title: "Requirement Title"
status: "Proposed"             # Proposed, Refined, Ready, In Progress, Implemented, Validated, Deferred, Rejected
priority: "High"               # High, Medium, Low
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: []             # Bottom-up: Which tenets inform this requirement
stakeholders: []               # Who cares about this requirement
tags: []
```

#### CIPs

```yaml
id: "0011"                     # 4-digit hex
title: "CIP Title"
status: "In Progress"          # Proposed, Accepted, In Progress, Implemented, Closed, Rejected, Deferred
created: "2026-01-03"
last_updated: "2026-01-03"
author: "Author Name"
related_requirements: []       # Bottom-up: Which requirements this implements
related_cips: []               # Optional: Related CIPs
blocked_by: "0012"             # Optional: CIP ID blocking this (use with Deferred)
superseded_by: "0013"          # Optional: CIP ID replacing this (use with Rejected)
tags: []
```

#### Backlog Tasks

```yaml
id: "2026-01-03_task-name"    # Date-based
title: "Task Title"
status: "In Progress"          # Proposed, Ready, In Progress, Completed, Abandoned
priority: "High"               # High, Medium, Low
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"           # features, bugs, documentation, infrastructure
related_cips: []               # Bottom-up: Which CIPs this task implements
owner: "Person Name"           # Optional
dependencies: []               # Optional: Other task IDs
tags: []
```

#### Tenets

```yaml
id: "simplicity-of-use"        # kebab-case
title: "Simplicity at All Levels"
status: "Active"               # Active, Under Review, Archived
created: "2025-05-05"
last_reviewed: "2026-01-03"
review_frequency: "Annual"     # Annual, Quarterly, Monthly
conflicts_with: []             # Optional: Other tenet IDs that conflict
tags: []
```

## Status Workflows

### Requirements

```
Proposed → Refined → Ready → In Progress → Implemented → Validated
         └→ Rejected (won't implement)
         └→ Deferred (postponed)
```

### CIPs

```
Proposed → Accepted → In Progress → Implemented → Closed
         └→ Rejected (won't implement, use superseded_by if replaced)
         └→ Deferred (postponed, use blocked_by to indicate blocker)
```

### Backlog Tasks

```
Proposed → Ready → In Progress → Completed
         └→ Abandoned (won't do, with explanation)
```

### Tenets

```
Active → Under Review → Active (updated)
       └→ Archived (no longer applicable)
```

## Bottom-Up Linking Pattern

VibeSafe uses a bottom-up linking pattern where components reference their immediate upstream context:

```
Tenets (WHY - foundation)
    ↑ related_tenets
Requirements (WHAT) 
    ↑ related_requirements
CIPs (HOW)
    ↑ related_cips
Backlog (DO)
    ↓
Implementation
```

### Linking Rules

- **Requirements** link to `related_tenets` (WHY informs WHAT)
- **CIPs** link to `related_requirements` (WHAT informs HOW)
- **Backlog** links to `related_cips` (HOW informs DO)
- **Tenets** don't link upward (foundation layer)

### What NOT to Do

❌ **Don't link backwards**:
- Requirements should NOT have `related_cips`
- CIPs should NOT have `related_backlog`
- Backlog should NOT have `related_requirements`

✅ **Instead**: Scripts query DOWN to find dependencies:
- "Which CIPs implement this requirement?" → Query CIPs where `related_requirements` contains this requirement ID
- "Which tasks execute this CIP?" → Query backlog where `related_cips` contains this CIP ID

## Validation

The `scripts/validate_vibesafe_structure.py` script enforces:

1. Required fields are present
2. Status values are from allowed lists
3. Dates are in YYYY-MM-DD format
4. File naming matches patterns
5. Bottom-up linking pattern is followed
6. Cross-references point to existing IDs

Run validation:
```bash
./scripts/validate_vibesafe_structure.py
```

## References

- **CIP-0011**: Defines this standardization
- **Validation Script**: `scripts/validate_vibesafe_structure.py`
- **Templates**: Located in component directories and `templates/`

