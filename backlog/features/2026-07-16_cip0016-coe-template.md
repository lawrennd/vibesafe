---
id: "2026-07-16_cip0016-coe-template"
title: "CIP-0016: Define CoE document format and template"
status: "Completed"
priority: "High"
created: "2026-07-16"
last_updated: "2026-07-16"
category: "features"
related_cips: ["0016"]
owner: "Neil Lawrence"
dependencies: []
tags:
  - backlog
  - governance
  - coe
  - process
---

# Task: Define CoE document format and template

## Description

Create the actual CoE document template and decide where CoE artifacts live.

Decisions to make and document:

1. **Directory structure**: Where do CoE documents go? Options:
   - `coe/` top-level directory (analogous to `cip/`, `backlog/`)
   - `cip/coe/` subdirectory
   - A special naming convention within `cip/` (e.g. `cip0016-coe-001.md`)

2. **Naming/numbering scheme**: CIPs use hex IDs, backlogs use dates. CoEs need their own scheme. Consider date-prefixed IDs (`coe-2026-07-16-001`) to reflect when the incident was identified.

3. **Template fields** — the CoE write-up should capture at minimum:
   - Severity class (0, 1, 2+)
   - Single-threaded owner
   - What happened (impact summary)
   - Proximate failure (what broke)
   - Root cause(s) (why it happened)
   - Contributing factors (process/tooling/assumptions)
   - Missing/incorrect traceability artifacts
   - Follow-up outputs (links to resulting backlog tasks, CIPs, requirements, tripwires)

4. **YAML frontmatter** for `whats-next` to pick up CoE status.

## Acceptance Criteria

- [ ] Directory/location decision documented in CIP-0016
- [ ] Naming/numbering scheme defined
- [ ] Template file created at agreed location
- [ ] YAML frontmatter fields defined

## Related

- CIP: 0016
