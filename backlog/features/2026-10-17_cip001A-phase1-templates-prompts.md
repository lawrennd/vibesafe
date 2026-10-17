---
id: "2026-10-17_cip001A-phase1-templates-prompts"
title: "CIP-001A Phase 1: Templates and agent prompts for GitHub links"
status: "Ready"
priority: "High"
created: "2026-10-17"
last_updated: "2026-10-17"
category: "features"
related_cips: ["001A"]
owner: "Neil Lawrence"
dependencies:
  - "2026-10-17_cip001A-phase0-normalization"
tags:
  - backlog
  - github
  - templates
  - prompts
---

# Task: CIP-001A Phase 1 — Templates and agent prompts

## Description

Update CIP, backlog, and CoE templates so optional GitHub frontmatter fields are visible at authoring time. Update agent prompt sources so assistants put GitHub IDs in frontmatter (not only body prose).

Canonical sources under `templates/`; keep install/runtime copies consistent with VibeSafe install paths.

## Acceptance Criteria

- [ ] CIP template includes optional `github_issues` / `github_prs` / `github_discussions`
- [ ] Backlog task template includes the same (plus legacy `github_issue` note if kept)
- [ ] CoE template includes the same
- [ ] Agent prompts for cip/backlog/coe/whats_next mention frontmatter linking
- [ ] Body “Related” sections remain optional human mirrors, not the sole source

## Implementation Notes

Update `templates/prompts/context-specific/*` and regenerate or note install path for `.cursor/rules`, `CLAUDE.md`, `AGENTS.md`, Copilot instructions as appropriate for this repo’s prompt pipeline.

## Related

- CIP: 001A

## Progress Updates

### 2026-10-17

Task created at Ready after CIP-001A acceptance.
