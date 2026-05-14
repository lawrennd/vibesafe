---
id: "2026-05-14_cip0017-template-stub"
title: "CIP-0017: Add whats_next_local.py template stub"
status: "Ready"
priority: "Medium"
created: "2026-05-14"
last_updated: "2026-05-14"
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

# Task: Add `whats_next_local.py` template stub

## Description

Create a well-documented template stub at `templates/.vibesafe/whats_next_local.py.example`
that users can copy to `.vibesafe/whats_next_local.py` to start extending `whats-next`.

The stub is **not** installed automatically by `install-minimal.sh` — users opt in by
manually copying or renaming the example file. This keeps the zero-cost-when-absent
guarantee: projects that don't create the file see no change in behaviour.

The stub must document both hooks (`get_local_sections` and `get_local_next_steps`) with:
- Full docstrings describing the signature, arguments, and return format
- Commented-out worked examples covering all tuple variants (2-tuple, 3-tuple for sections;
  plain str, `("high", …)`, `("low", …)` for next steps)
- A data-science project example (dataset freshness / CI failure) similar to the one
  in CIP-0017

## Acceptance Criteria

- [ ] File exists at `templates/.vibesafe/whats_next_local.py.example`
- [ ] Both `get_local_sections` and `get_local_next_steps` are defined (as working stubs returning `[]`)
- [ ] Each function has a complete docstring documenting args and return format
- [ ] Commented-out examples illustrate all supported tuple variants for both hooks
- [ ] The stub is valid, importable Python (no syntax errors)
- [ ] The stub is NOT added to the automatic installation flow in `install-minimal.sh`

## Implementation Notes

The file should start with a module-level docstring explaining the purpose and
how to activate the extension (copy to `.vibesafe/whats_next_local.py`).

Example structure:

```python
"""
whats_next_local.py — Project-specific extension for whats-next.

Copy this file to .vibesafe/whats_next_local.py (remove the .example suffix)
to extend the whats-next output with project-specific sections and next steps.
"""

def get_local_sections(context: dict) -> list:
    """Return additional output sections..."""
    return []

def get_local_next_steps(context: dict) -> list:
    """Return additional next-step suggestions..."""
    return []
```

## Related

- CIP: 0017
- Documentation: cip/cip0017.md

## Progress Updates

### 2026-05-14

Task created as part of CIP-0017 backlog breakdown.
