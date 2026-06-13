---
id: "2026-05-14_cip0017-build-context-dict"
title: "CIP-0017: Build context dict in main() for hook calls"
status: "Completed"
priority: "High"
created: "2026-05-14"
last_updated: "2026-06-13"
category: "features"
related_cips: ["0017"]
owner: "Neil Lawrence"
dependencies:
- "2026-05-14_cip0017-load-local-module"
tags:
- backlog
- whats-next
- extensibility
---

# Task: Build context dict in `main()` for hook calls

## Description

Assemble the `context` dict in `main()` of `templates/scripts/whats_next.py` from the
already-computed scan results. This dict is the stable interface passed to both
`get_local_sections()` and `get_local_next_steps()` in the local extension module.

This task is a prerequisite for Tasks 3 and 4, which wire up the two hooks.

The context dict must contain:

| Key | Source |
|-----|--------|
| `git_info` | return value of `get_git_status()` |
| `cips_info` | return value of `scan_cips()` |
| `backlog_info` | return value of `scan_backlog()` |
| `requirements_info` | return value of `scan_requirements()` |
| `args` | `argparse.Namespace` from CLI argument parsing |

The dict is constructed after all scans have run and before any hook calls are made.
Local modules must treat it as read-only; mutations have no effect on the core script.

## Acceptance Criteria

- [ ] `context` dict is built in `main()` after all scan functions have been called
- [ ] Contains all five keys: `git_info`, `cips_info`, `backlog_info`, `requirements_info`, `args`
- [ ] The dict is constructed once and reused for both `get_local_sections()` and `get_local_next_steps()` calls
- [ ] Local module mutating the dict does not affect core script behaviour

## Implementation Notes

```python
context = {
    "git_info": git_info,
    "cips_info": cips_info,
    "backlog_info": backlog_info,
    "requirements_info": requirements_info,
    "args": args,
}
```

The `position` key (`"before"` / `"after"`) is added per-call when invoking
`get_local_sections()`, not stored permanently in the base context dict.

## Related

- CIP: 0017
- Documentation: cip/cip0017.md

## Progress Updates

### 2026-05-14

Task created as part of CIP-0017 backlog breakdown.
