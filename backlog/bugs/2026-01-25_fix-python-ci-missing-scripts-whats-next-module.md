---
category: bugs
created: "2026-01-25"
id: 2026-01-25_fix-python-ci-missing-scripts-whats-next-module
last_updated: "2026-01-25"
priority: High
related_cips: []
owner: Neil Lawrence
status: Proposed
title: Fix Python CI failure from missing scripts.whats_next runtime module
tags:
  - bug
  - ci
  - python-tests
  - whats-next
  - scripts
---

# Bug: Fix Python CI failure (missing `scripts/whats_next.py` module)

## Description

Python CI is failing because tests patch/import `scripts.whats_next`, but the repository does not contain `scripts/whats_next.py` (only `templates/scripts/whats_next.py` exists). This causes errors like:

- `AttributeError: module 'scripts' has no attribute 'whats_next'`

This is likely a repo layout / template-sync regression where `whats_next.py` moved (or was deleted) without updating the Python test suite and/or packaging expectations.

### What we learned (dogfooding install semantics)

In `scripts/install-minimal.sh`, VibeSafe dogfoods its own install model:

- **Canonical source**: `templates/scripts/whats_next.py`
- **Installed/runtime copy**: `scripts/whats_next.py` (materialized during installation via `cp templates/... → scripts/...`)

The current Python CI workflow (`.github/workflows/python-tests.yml`) runs `pytest` directly and **does not materialize the runtime layer first**, so `scripts.whats_next` is missing at import/patch time.

Also note: **install-whats-next** (the venv/wrapper setup) is about runtime execution environment and generally assumes `scripts/whats_next.py` already exists; it does not replace the materialization step.

## Acceptance Criteria

- [ ] `python -m pytest tests/` passes in CI (including `tests/test_whats_next.py`).
- [ ] `scripts/whats_next.py` exists (or tests are updated to patch the correct import path and the module is available as expected).
- [ ] VibeSafe “installation” continues to ship a working `whats-next` command/wrapper and underlying implementation.
- [ ] If `templates/scripts/whats_next.py` is the canonical source, establish and document the sync rule so repo + templates don’t drift again.

## Implementation Notes

Possible fixes (choose one, avoid split-brain):

1. **CI materialization step (recommended)**: before running pytest, materialize runtime scripts from templates in the workspace (no committed duplication):
   - `mkdir -p scripts`
   - `cp templates/scripts/whats_next.py scripts/whats_next.py`
   - (Optionally also materialize `scripts/validate_vibesafe_structure.py` similarly, to match the installed view)

2. **Run installer (heavier)**: invoke `scripts/install-minimal.sh` in CI before pytest to ensure runtime files exist. This exercises more behavior than needed for unit tests and may have extra side effects (gitignore edits, venv, etc.), so it should be done carefully or via a dedicated “materialize-only” mode.

3. **Test-only workaround (not preferred)**: make the whats-next unit tests conditional on runtime file existence (similar to `tests/test_template_runtime_sync.py`). This reduces coverage of the installed runtime import path.

## Related

- Tests: `tests/test_whats_next.py`
- Templates: `templates/scripts/whats_next.py`
- Potentially relevant: template drift task `backlog/infrastructure/2025-08-15_sync-templates-with-current-files.md`
  - Also relevant CIPs: CIP-0006 (install script env-var configurability), CIP-000A (whats-next script + template copy)

## Progress Updates

### 2026-01-25

Task created after observing recurring CI failures on `tests/test_whats_next.py` due to missing `scripts.whats_next` module.
