---
id: "2026-05-14_cip0017-local-sections-hook"
title: "CIP-0017: Extend main() with get_local_sections() before/after hook"
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

# Task: Extend `main()` with `get_local_sections()` before/after hook

## Description

Extend `main()` in `templates/scripts/whats_next.py` to call `get_local_sections(context)`
on the local extension module (if loaded) at two distinct positions in the output:

1. **Before pass** — called with `context["position"] = "before"`. Sections returned
   with `position == "before"` (either via 3-tuple or matched against the passed position)
   are rendered before all built-in VibeSafe sections. Useful for project-wide alerts or
   blockers that must be seen first.

2. **After pass** — called with `context["position"] = "after"`. Sections returned
   with `position == "after"` (or 2-tuples, which default to `"after"`) are rendered
   after all built-in VibeSafe sections.

Each section descriptor returned is either:
- A 2-tuple `(title, lines)` — defaults to `"after"` position
- A 3-tuple `(title, lines, position)` — rendered only when the declared position matches
  the current call's position

Each section is rendered using the existing `print_section()` helper.
All calls are wrapped in `try/except` for graceful degradation.

## Acceptance Criteria

- [ ] `main()` calls `get_local_sections(context)` with `position="before"` before printing any built-in sections
- [ ] `main()` calls `get_local_sections(context)` with `position="after"` after printing all built-in sections
- [ ] 2-tuples `(title, lines)` are rendered in the `"after"` pass
- [ ] 3-tuples `(title, lines, "before")` are rendered in the `"before"` pass only
- [ ] 3-tuples `(title, lines, "after")` are rendered in the `"after"` pass only
- [ ] An exception raised inside `get_local_sections()` is caught, a warning is printed, and the rest of the output is unaffected
- [ ] When `get_local_sections` is not defined on the module, nothing happens
- [ ] When no local module is loaded, output is identical to the current implementation

## Implementation Notes

```python
def _render_local_sections(local_mod, context, position):
    if not local_mod or not hasattr(local_mod, "get_local_sections"):
        return
    ctx = {**context, "position": position}
    try:
        for item in local_mod.get_local_sections(ctx):
            if len(item) == 2:
                title, lines = item
                sec_position = "after"
            else:
                title, lines, sec_position = item
            if sec_position == position:
                print_section(title, lines)
    except Exception as exc:
        print(f"⚠️  Warning: get_local_sections() failed: {exc}")

# In main():
_render_local_sections(local_mod, context, "before")
# ... all built-in sections ...
_render_local_sections(local_mod, context, "after")
```

## Related

- CIP: 0017
- Documentation: cip/cip0017.md

## Progress Updates

### 2026-05-14

Task created as part of CIP-0017 backlog breakdown.
