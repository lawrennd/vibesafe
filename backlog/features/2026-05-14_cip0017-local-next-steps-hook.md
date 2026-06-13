---
id: "2026-05-14_cip0017-local-next-steps-hook"
title: "CIP-0017: Extend generate_next_steps() with get_local_next_steps() hook"
status: "Completed"
priority: "High"
created: "2026-05-14"
last_updated: "2026-06-13"
category: "features"
related_cips: ["0017"]
owner: "Neil Lawrence"
dependencies:
- "2026-05-14_cip0017-load-local-module"
- "2026-05-14_cip0017-build-context-dict"
tags:
- backlog
- whats-next
- extensibility
---

# Task: Extend `generate_next_steps()` with `get_local_next_steps()` hook

## Description

Extend `generate_next_steps()` in `templates/scripts/whats_next.py` to call
`get_local_next_steps(context)` on the local extension module (if loaded) and merge
the returned items into the overall next-steps list with the correct priority ordering.

Items returned by the local hook can be:
- A plain `str` — treated as low priority; appended after all VibeSafe suggestions
- A 2-tuple `("high", str)` — prepended before all VibeSafe suggestions
- A 2-tuple `("low", str)` — appended after all VibeSafe suggestions

The call must be wrapped in `try/except` so a buggy local hook never crashes the script.

## Acceptance Criteria

- [ ] `generate_next_steps()` calls `local_mod.get_local_next_steps(context)` when the attribute exists on the loaded module
- [ ] `"high"` items appear before all VibeSafe-generated suggestions in the output
- [ ] Plain `str` and `"low"` items appear after all VibeSafe-generated suggestions
- [ ] An exception raised inside `get_local_next_steps()` is caught, a warning is printed, and the rest of the output is unaffected
- [ ] When `get_local_next_steps` is not defined on the module, nothing happens (no error)
- [ ] When no local module is loaded, behaviour is identical to the current implementation

## Implementation Notes

```python
# Inside generate_next_steps(context, local_mod=None):
high_local, low_local = [], []
if local_mod and hasattr(local_mod, "get_local_next_steps"):
    try:
        for item in local_mod.get_local_next_steps(context):
            if isinstance(item, tuple) and item[0] == "high":
                high_local.append(item[1])
            elif isinstance(item, tuple) and item[0] == "low":
                low_local.append(item[1])
            else:
                low_local.append(str(item))
    except Exception as exc:
        print(f"⚠️  Warning: get_local_next_steps() failed: {exc}")

steps = high_local + vibesafe_steps + low_local
```

## Related

- CIP: 0017
- Documentation: cip/cip0017.md

## Progress Updates

### 2026-05-14

Task created as part of CIP-0017 backlog breakdown.
