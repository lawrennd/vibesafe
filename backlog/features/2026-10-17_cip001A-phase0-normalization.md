---
id: "2026-10-17_cip001A-phase0-normalization"
title: "CIP-001A Phase 0: GitHub frontmatter normalization and validator support"
status: "Completed"
priority: "High"
created: "2026-10-17"
last_updated: "2026-10-17"
category: "features"
related_cips: ["001A"]
owner: "Neil Lawrence"
dependencies: []
tags:
  - backlog
  - github
  - validation
  - frontmatter
---

# Task: CIP-001A Phase 0 — Normalization and validator support

> Backlog tasks execute CIP HOW. Linked via `related_cips`.

## Description

Validation-led foundation for optional GitHub links. Add helpers (or extend the structure validator) that:

- Accept `github_issues`, `github_prs`, `github_discussions` as int or list of ints
- Treat legacy `github_issue` as an alias for a single-element `github_issues` list
- Treat empty string / null / `N/A` as absent
- Warn (not hard-fail) on non-integer optional GitHub fields
- Document fields in `docs/source/yaml_frontmatter_examples.md`

No live `gh` calls in this phase.

## Acceptance Criteria

- [x] Normalization helper covers int, list, legacy `github_issue`, and empty/`N/A`
- [x] Validator accepts optional GitHub fields without requiring them
- [x] Unit tests cover normalization (no network)
- [x] YAML frontmatter examples document the new fields and legacy alias

## Implementation Notes

See CIP-001A Detailed Description → Frontmatter Schema and Phase 0 plan.
Prefer small pure functions testable without mocking `gh`.

## Related

- CIP: 001A
- Requirement: REQ-0011 (via CIP)

## Progress Updates

### 2026-10-17

Task created at Ready after CIP-001A acceptance.

Implemented: `normalize_github_id_list` / `normalize_github_refs` / `validate_github_refs` in
`templates/scripts/validate_vibesafe_structure.py` (synced to `scripts/`); optional fields on
CIP/backlog specs; docs in `docs/source/yaml_frontmatter_examples.md`; tests in
`TestGitHubRefNormalization`. Status → Completed.
