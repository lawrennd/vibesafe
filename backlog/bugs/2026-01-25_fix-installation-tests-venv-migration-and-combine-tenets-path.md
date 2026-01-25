---
category: bugs
created: "2026-01-25"
id: 2026-01-25_fix-installation-tests-venv-migration-and-combine-tenets-path
last_updated: "2026-01-25"
priority: High
related_cips: []
owner: Neil Lawrence
status: Proposed
title: Fix installation test failures (venv migration/preservation and combine_tenets path)
tags:
  - bug
  - installation
  - tests
  - venv
  - tenets
---

# Bug: Fix installation test failures (venv migration + combine_tenets.py path)

## Description

The GitHub Actions installation tests (`scripts/test/install-test.bats`) are failing on Ubuntu 24.04. The failures indicate regressions or drift in installation behavior around virtual environment handling and tenet/cursor-rule generation setup.

### Context (dogfooding install model)

VibeSafe’s installer treats `templates/` as the **source of truth** and copies system/runtime files into their installed locations (e.g. `scripts/whats_next.py`). Tests should align with that model: setup may need to materialize runtime files from templates when tests patch/import runtime paths.

### Failing tests

- **#9 VENV: Old VibeSafe `.venv` is migrated to `.venv-vibesafe` on first install**
  - Expectation: legacy VibeSafe `.venv` is migrated and removed.
  - Observed: `.venv` still exists (`[ ! -d ".venv" ]` failed).

- **#10 VENV: Project `.venv` (not VibeSafe) is preserved**
  - Expectation: installer creates `.venv-vibesafe` without disturbing an existing project `.venv`.
  - Observed: `.venv-vibesafe` not created (`[ -d ".venv-vibesafe" ]` failed).

- **#11 VENV: Orphaned `.venv` warns but doesn't delete when `.venv-vibesafe` exists**
  - Expectation: clear warning mentioning orphaned `.venv` and preservation behavior.
  - Observed: warning text not present (output match failed).

- **#17 GENERATE: Cursor rules are created from project tenets**
  - Failure is during test setup: `cp .../tenets/combine_tenets.py` fails because the source path does not exist.
  - Observed: `cp: cannot stat '.../tenets/combine_tenets.py': No such file or directory`

## Acceptance Criteria

- [ ] Installer migrates a legacy VibeSafe-managed `.venv` to `.venv-vibesafe` on first install and removes the legacy directory.
- [ ] Installer preserves an existing user/project `.venv` and still creates/uses `.venv-vibesafe` for VibeSafe tooling.
- [ ] When both `.venv` and `.venv-vibesafe` exist and `.venv` appears unrelated to VibeSafe, installer emits a warning mentioning the orphaned `.venv` and does not delete it.
- [ ] Installation tests no longer reference a non-existent `tenets/combine_tenets.py` path (either restore/provide the expected file location or update the tests to the correct source path).
- [ ] `bats scripts/test/*.bats` passes in CI.

## Implementation Notes

- The `.venv`/`.venv-vibesafe` behavior should preserve the “clean installation” philosophy: update system tooling while not damaging user project environments.
- For test #17, decide on the canonical location of `combine_tenets.py` in this repo (and the installed layout). Then make the tests reflect that canonical layout consistently.
  - If the canonical source is `templates/tenets/combine_tenets.py`, tests should copy/materialize it into the expected runtime location before invoking generation logic.
  - If the canonical runtime location is `tenets/combine_tenets.py`, ensure it exists in the dogfooding repo (or ensure install/materialization creates it before tests reference it).

## Related

- Tests: `scripts/test/install-test.bats`
- Installer: `scripts/install-minimal.sh`

## Progress Updates

### 2026-01-25

Task created after CI failures in installation test suite (VENV handling and tenet/cursor-rule generation setup).
