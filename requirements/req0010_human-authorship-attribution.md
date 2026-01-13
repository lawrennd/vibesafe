---
id: "0010"
title: "Human Authorship Attribution for Accountable Artifacts"
status: "Proposed"
priority: "High"
created: "2026-01-10"
last_updated: "2026-01-10"
related_tenets:
  - "human-authorship"
  - "shared-information-landmarks"
stakeholders:
  - "Maintainers"
  - "Contributors"
  - "Users of AI assistants in VibeSafe-managed repos"
tags:
  - "accountability"
  - "metadata"
  - "governance"
---

# REQ-0010: Human Authorship Attribution for Accountable Artifacts

## Description

VibeSafe must make accountability explicit: whenever an artifact declares responsibility (via metadata fields like `author` or `owner`), that attribution must name a specific human.

AI assistants can draft content and propose changes, but they do not bear social accountability for outcomes. VibeSafe therefore requires that responsibility-bearing artifacts always have a human author/owner, so decisions and follow-through can be traced to someone who can review, decide, and be held accountable.

## Acceptance Criteria

- [ ] Every CIP (`cip/cip*.md`) includes an `author` field in YAML frontmatter.
- [ ] Every backlog task (`backlog/**/YYYY-MM-DD_*.md`) includes an `owner` field in YAML frontmatter.
- [ ] `author`/`owner` values are **single-threaded**: exactly one primary accountable human name per artifact (not multiple names like `"A, B"` or `"A and B"`).
- [ ] `author`/`owner` values are **non-empty human names**, not placeholders (e.g. `"[Your Name]"`), not non-human entities (e.g. `"VibeSafe Team"`), and not AI/tool attributions.
- [ ] The structure validator (`scripts/validate_vibesafe_structure.py`) enforces this requirement.

## Notes (Optional)

This requirement supports the tenet **human-authorship** ("AIs advise; humans decide") by ensuring that decision-making and responsibility are never left anonymous or delegated to tools.


