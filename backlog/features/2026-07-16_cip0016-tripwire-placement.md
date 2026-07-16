---
id: "2026-07-16_cip0016-tripwire-placement"
title: "CIP-0016: Decide where preventative tripwire warnings live"
status: "Ready"
priority: "Medium"
created: "2026-07-16"
last_updated: "2026-07-16"
category: "features"
related_cips: ["0016"]
owner: "Neil Lawrence"
dependencies:
  - "2026-07-16_cip0016-severity-classes"
tags:
  - backlog
  - governance
  - coe
  - validation
---

# Task: Decide where preventative tripwire warnings live

## Description

CIP-0016 identifies three categories of preventative tripwires (optional
early-detection, not heavyweight gates):

1. Governance drift warnings — implementation changed without CIP/backlog
   updates (already partially implemented via `check_governance_drift()`)
2. Traceability gap warnings — tenet/requirement + implementation changed
   without CIP/backlog update (partially implemented)
3. Template/runtime drift enforcement (already implemented)

And now CIP-0019 adds:
4. CIP→backlog coverage warnings (implemented)

Decide:
- Which of these belong in the **validator** (`validate_vibesafe_structure.py`)
- Which belong in **`whats-next`** output
- Which belong in **CI strict mode** only
- Whether any should become hard errors vs warnings

Document the decision in CIP-0016 and create any resulting implementation
backlog tasks.

## Acceptance Criteria

- [ ] Decision on tripwire placement documented in CIP-0016
- [ ] Any gaps between current implementation and the agreed set identified
- [ ] Implementation tasks created for any missing tripwires

## Related

- CIP: 0016
- CIP: 0019
