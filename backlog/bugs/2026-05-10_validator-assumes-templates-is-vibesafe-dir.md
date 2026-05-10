---
category: bugs
created: '2026-05-10'
id: 2026-05-10_validator-assumes-templates-is-vibesafe-dir
last_updated: '2026-05-10'
priority: Medium
related_cips: []
owner: "Neil Lawrence"
status: Proposed
title: "Validator checks for VibeSafe system files under templates/ in user projects"
---

# Bug: Validator checks for VibeSafe system files under templates/ in user projects

## Description

`scripts/validate_vibesafe_structure.py` checks for the existence of VibeSafe system
files at paths under `templates/`:

```
templates/scripts/whats_next.py
templates/scripts/validate_vibesafe_structure.py
templates/backlog/update_index.py
templates/tenets/combine_tenets.py
```

These paths are valid in the VibeSafe source repository, where `templates/` holds
VibeSafe system file templates used during installation. However, when VibeSafe is
installed in a user project that has its own `templates/` directory, the validator
raises false-positive errors for all four files, causing validation to fail even when
the project structure is entirely correct.

**Discovered in**: the Explayner project, where `templates/` contains Explayner user
content (`narration_template.yml`, `scene_timings_template.yml`, `render.py`). Running
the validator produced:

```
❌ ERRORS (4):
  templates/scripts/whats_next.py:
    Missing template system file: templates/scripts/whats_next.py
  templates/scripts/validate_vibesafe_structure.py:
    Missing template system file: templates/scripts/validate_vibesafe_structure.py
  templates/backlog/update_index.py:
    Missing template system file: templates/backlog/update_index.py
  templates/tenets/combine_tenets.py:
    Missing template system file: templates/tenets/combine_tenets.py
```

## Relationship to Related Bug

This is the validator-side manifestation of the same root cause as
`2026-05-10_gitignore-blanket-templates-ignore`: VibeSafe assumes `templates/` is
always its own system directory, both in `.gitignore` generation and in validation.
Both bugs should be fixed together.

## Acceptance Criteria

- [ ] The validator does not check for VibeSafe system files under `templates/` in user
      projects (or only does so when `templates/` is confirmed to be a VibeSafe-managed
      directory)
- [ ] A user project with a `templates/` directory containing user content passes
      validation without errors related to missing VibeSafe template system files
- [ ] The VibeSafe source repo itself continues to validate correctly

## Implementation Notes

Options:
1. **Remove the check entirely** from user-project validation — the presence of
   VibeSafe source templates is only meaningful in the VibeSafe development repo.
2. **Guard with a marker file** — only check for `templates/scripts/whats_next.py` etc.
   if a `.vibesafe-templates` marker exists in `templates/`, written by VibeSafe's own
   install/development setup.
3. **Check `scripts/` directly** — the validator already knows where the actual scripts
   live (`scripts/whats_next.py`, `scripts/validate_vibesafe_structure.py`). Checking
   `templates/scripts/` is redundant for user projects.

Option 1 is simplest and most correct for the user-project use case.

## References

- Related bug: `2026-05-10_gitignore-blanket-templates-ignore` (same root cause, `.gitignore` side)
- Discovered in Explayner project (May 2026)

## Progress Updates

### 2026-05-10
Bug filed. The 4 false-positive errors are currently present in the Explayner project
but do not reflect any real problem. No workaround is needed beyond awareness.
