---
id: "2026-10-17_cip001A-phase4-dogfood"
title: "CIP-001A Phase 4: Dogfood GitHub links on VibeSafe artifacts"
status: "Ready"
priority: "Medium"
created: "2026-10-17"
last_updated: "2026-10-17"
category: "features"
related_cips: ["001A"]
owner: "Neil Lawrence"
dependencies:
  - "2026-10-17_cip001A-phase2-whats-next-layer1"
tags:
  - backlog
  - github
  - dogfood
---

# Task: CIP-001A Phase 4 — Dogfood on VibeSafe

## Description

Link a small set of real VibeSafe CIP/backlog (and optionally CoE) artifacts to existing GitHub Issues/PRs/Discussions where useful. Run `./whats-next` with and without auth and with `--no-github` to confirm graceful behaviour. Update CIP-001A / REQ-0011 status when Phases 0–3 are verified.

## Acceptance Criteria

- [ ] At least a few active artifacts carry real `github_*` frontmatter links
- [ ] Manual check: enrichment works when `gh` auth is healthy
- [ ] Manual check: silent skip when auth fails or `--no-github`
- [ ] CIP-001A implementation checklist updated; consider Implemented → Closed after review
- [ ] REQ-0011 acceptance criteria checked off where satisfied

## Implementation Notes

Do not invent Issues just for dogfood. Prefer existing PRs/issues. Auth may need `gh auth login` on the maintainer machine — that is environmental, not a code defect.

## Related

- CIP: 001A

## Progress Updates

### 2026-10-17

Task created at Ready after CIP-001A acceptance.
