---
id: "2026-07-16_cip0016-whats-next-integration"
title: "CIP-0016: Integrate CoE status into whats-next output"
status: "Completed"
priority: "Medium"
created: "2026-07-16"
last_updated: "2026-07-16"
category: "features"
related_cips: ["0016"]
owner: "Neil Lawrence"
dependencies:
  - "2026-07-16_cip0016-coe-template"
tags:
  - backlog
  - governance
  - coe
  - whats-next
---

# Task: Integrate CoE status into whats-next output

## Description

Once CoE documents have a defined format and directory, `whats-next` should
surface them alongside CIPs and backlog items.

Specifically:
- Scan the CoE directory for open CoEs (those without all follow-up outputs linked)
- Show open CoEs in the `whats-next` output (similar to how Proposed/Accepted CIPs
  are shown)
- Suggest as a next step any CoE whose follow-up tasks haven't been created yet
- Optionally: flag when a governance incident trigger occurred (governance drift
  warning fired in git) but no CoE exists

This task is dependent on the template/directory being agreed first.

## Acceptance Criteria

- [ ] `whats-next` scans CoE directory (once defined) and reports open CoEs
- [ ] Open CoEs appear in Suggested Next Steps if follow-ups are pending
- [ ] Tests cover the new CoE section

## Related

- CIP: 0016
