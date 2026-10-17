---
id: "2026-10-17_cip001A-phase3-next-steps-glance"
title: "CIP-001A Phase 3: Soft next-steps and optional GitHub repo glance"
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
  - whats-next
---

# Task: CIP-001A Phase 3 — Soft next-steps and Layer 2 glance

## Description

Add soft Suggested Next Steps from link/state mismatches (hints only — never auto-change VibeSafe or GitHub status). Add optional Layer 2 repo glance: compact open PRs; optionally open issues with a conventional label if present. Keep glance small; do not dump the full tracker.

## Acceptance Criteria

- [ ] Soft hints for useful mismatches (e.g. In Progress CIP with open PR; Completed backlog with still-open linked issue)
- [ ] Layer 2 glance is compact and skippable with `--no-github`
- [ ] No bidirectional status sync
- [ ] Tests cover hint generation with mocked GitHub state
- [ ] Performance budget documented (enrichment may exceed local-only 2s target)

## Implementation Notes

Label convention for optional issue glance (e.g. `vibesafe`) should be documented as optional, not required.

## Related

- CIP: 001A

## Progress Updates

### 2026-10-17

Task created at Ready after CIP-001A acceptance.
