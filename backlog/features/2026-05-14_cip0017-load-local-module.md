---
id: "2026-05-14_cip0017-load-local-module"
title: "CIP-0017: Add _load_local_module() helper to whats_next.py"
status: "Completed"
priority: "High"
created: "2026-05-14"
last_updated: "2026-06-13"
category: "features"
related_cips: ["0017"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- whats-next
- extensibility
---

# Task: Add `_load_local_module()` helper to whats_next.py

## Description

Add a `_load_local_module()` helper function to `templates/scripts/whats_next.py` that
discovers and loads the optional local extension module at `.vibesafe/whats_next_local.py`.

This is the foundation of the CIP-0017 hook system. All other hook-related tasks depend on
this function being in place.

The function must:
- Check whether `.vibesafe/whats_next_local.py` exists; if not, return `None` silently
- Load the module using `importlib.util.spec_from_file_location` so it runs in isolation
- Catch any `Exception` raised during import and print a warning to stdout (never raise)
- Return the loaded module object on success, `None` on any failure

## Acceptance Criteria

- [ ] `_load_local_module()` is defined in `templates/scripts/whats_next.py`
- [ ] Returns `None` (no output, no error) when `.vibesafe/whats_next_local.py` does not exist
- [ ] Returns the loaded module object when the file exists and is valid Python
- [ ] Prints a warning line (prefixed with `⚠️  Warning:`) and returns `None` when the file exists but raises on import
- [ ] Does not introduce any new package dependencies

## Implementation Notes

```python
import importlib.util, sys, traceback

def _load_local_module(path=".vibesafe/whats_next_local.py"):
    if not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location("whats_next_local", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as exc:
        print(f"⚠️  Warning: could not load {path}: {exc}")
        return None
```

`importlib.util` is part of the Python standard library — no new dependencies.

## Related

- CIP: 0017
- Documentation: cip/cip0017.md

## Progress Updates

### 2026-05-14

Task created as part of CIP-0017 backlog breakdown.
