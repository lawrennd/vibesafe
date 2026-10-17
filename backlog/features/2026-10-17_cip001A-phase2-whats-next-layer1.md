---
id: "2026-10-17_cip001A-phase2-whats-next-layer1"
title: "CIP-001A Phase 2: whats-next Layer 1 GitHub enrichment and --no-github"
status: "Ready"
priority: "High"
created: "2026-10-17"
last_updated: "2026-10-17"
category: "features"
related_cips: ["001A"]
owner: "Neil Lawrence"
dependencies:
  - "2026-10-17_cip001A-phase0-normalization"
  - "2026-10-17_cip001A-phase1-templates-prompts"
tags:
  - backlog
  - github
  - whats-next
---

# Task: CIP-001A Phase 2 — whats-next Layer 1 enrichment

## Description

Implement eligibility probe (`gh` on PATH, GitHub remote, successful `gh auth status`) and Layer 1 linked enrichment in `whats-next`: for CIP/backlog/CoE artifacts with GitHub IDs, resolve title/state via `gh` and display compactly. Add `--no-github`. Fail open when GitHub is unavailable.

## Acceptance Criteria

- [ ] GitHub section/enrichment appears only when eligibility probe passes
- [ ] Linked issues/PRs/discussions show number, title, and state when resolvable
- [ ] Missing `gh` / auth / non-GitHub remote → no error, no GitHub section
- [ ] `--no-github` skips all GitHub calls
- [ ] Tests mock `gh`; CI does not require live GitHub
- [ ] Templates/scripts and installed `scripts/whats_next.py` stay in sync per project convention

## Implementation Notes

Prefer batching/`gh` call caps within a single run. Discussions may need `gh api`. Reuse Phase 0 normalization helpers.

## Related

- CIP: 001A
- Related CIP: 000A, 0017

## Progress Updates

### 2026-10-17

Task created at Ready after CIP-001A acceptance.
