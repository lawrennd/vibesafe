---
id: "2026-06-13_cip0019-sync-runtime"
title: "CIP-0019: Sync validate_vibesafe_structure.py template → runtime"
status: "Ready"
priority: "Medium"
created: "2026-06-13"
last_updated: "2026-06-13"
category: "features"
related_cips: ["0019"]
owner: "Neil Lawrence"
dependencies:
  - "2026-06-13_cip0019-wire-main"
tags:
  - backlog
  - validation
  - governance
---

# Task: Sync `validate_vibesafe_structure.py` template → runtime

## Description

After Tasks 1–3 are complete and tests pass, copy the updated template to
the runtime location:

```bash
cp templates/scripts/validate_vibesafe_structure.py scripts/validate_vibesafe_structure.py
```

This mirrors the pattern used for `whats_next.py` (CIP-0017).

## Acceptance Criteria

- [ ] `scripts/validate_vibesafe_structure.py` contains the new function and flag
- [ ] Running `scripts/validate_vibesafe_structure.py` on the VibeSafe repo exits 0
- [ ] Pre-commit hook still passes after the sync

## Related

- CIP: 0019
