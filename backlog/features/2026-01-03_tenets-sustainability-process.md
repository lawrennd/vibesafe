---
id: "2026-01-03_tenets-sustainability-process"
title: "Phase 3: Tenets Sustainability Process"
status: "Proposed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_yaml-frontmatter-standardization"]
related_cips: ["0004", "0011"]
---

# Task: Phase 3: Tenets Sustainability Process

## Description

Implement Phase 3 of CIP-0011: Add sustainability and review process to tenets. This builds on the basic tenet system implemented in CIP-0004 by adding lifecycle management features: YAML frontmatter, review metadata, review process documentation, and conflict detection in combine_tenets.py.

## Acceptance Criteria

- [ ] Update tenet template with YAML frontmatter
  - Add: status, last_reviewed, review_frequency, related_cips, conflicts_with
  - Include sections: Description, Quote, Examples, Counter-examples, Conflicts
- [ ] Add review metadata fields to existing VibeSafe tenets
  - Add last_reviewed dates (set to today for initial review)
  - Add review_frequency (Annual for most)
  - Add status (Active for current tenets)
- [ ] **Create VibeSafe Principles script and cursor rule**:
  - Create `scripts/generate_vibesafe_principles.py` (separate from combine_tenets.py)
  - Generates `templates/.cursor/rules/vibesafe-principles.mdc` (single comprehensive cursor rule)
  - Content includes:
    - All VibeSafe Principles (validation-led, simplicity, user-autonomy, etc.)
    - WHY/WHAT/HOW/DO hierarchy (Tenets → Requirements → CIPs → Backlog)
    - Bottom-up linking pattern explanation
    - Component naming conventions (reqXXXX, cipXXXX, YYYY-MM-DD)
    - Core VibeSafe concepts ("What is VibeSafe?")
  - Gets automatically deployed to user projects via install-minimal.sh
  - May consolidate/replace parts of existing cursor rules to avoid duplication
  - Distinction: "VibeSafe Principles" = framework guidance, "Project Tenets" = user-specific (via combine_tenets.py)
  - Keep combine_tenets.py focused on user's project tenets only
- [ ] Create tenet review checklist in tenets/README.md
- [ ] Document tenet review process in tenets/README.md
  - When to review (quarterly, on deviation, on conflict)
  - What to check (still relevant? conflicts? usage?)
  - How to update (status changes, content updates)
- [ ] Add tenet conflict detection to combine_tenets.py
  - Parse conflicts_with field
  - Report conflicts when found
  - Suggest resolution when possible
- [ ] Examples showing tenet lifecycle (Active → Under Review → Updated/Archived)

## Implementation Notes

**Terminology Clarity**:
- **VibeSafe Principles**: Framework-level guidance (in `tenets/vibesafe/`)
  - Examples: validation-led-development, simplicity-of-use, documentation-as-code
  - Deployed to all user projects via `vibesafe-principles.mdc`
- **Project Tenets**: User-specific values (in `tenets/projectname/`)
  - User creates their own tenets for their project
  - Deployed via CIP-0010's individual `project_tenet_*.mdc` files

**Review Process** (Lightweight - 10-15 minutes):
1. Scan active tenets/principles
2. Check if any violations documented recently
3. Check if any conflicts detected
4. Update last_reviewed date

**Learning from Deviations**:
When we violate a principle/tenet, document:
- What decision was made
- Why we deviated  
- Justified (needs update) or mistake (recommit)?

## Related

- CIP: 0004, 0011 (CIP-0004 provides foundation, CIP-0011 adds sustainability features)
- Depends on: 2026-01-03_yaml-frontmatter-standardization

**Note**: REQ-0004 (Sustainable and Relevant Tenets) is linked via CIP-0011, following VibeSafe's bottom-up linking pattern (Backlog → CIP → Requirement).

## Progress Updates

### 2026-01-03
Task created. Can proceed in parallel with Phase 1/2.

