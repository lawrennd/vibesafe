---
category: bugs
created: '2026-05-10'
id: 2026-05-10_gitignore-blanket-templates-ignore
last_updated: '2026-05-10'
priority: Medium
related_cips: []
owner: "Neil Lawrence"
status: Proposed
title: "Auto-generated .gitignore blanket-ignores templates/ and silently swallows user content"
---

# Bug: Auto-generated .gitignore blanket-ignores templates/ and silently swallows user content

## Description

VibeSafe's auto-generated `.gitignore` contains the entry:

```
# VibeSafe templates directory (source files for VibeSafe development)
templates/
```

This is appropriate for the VibeSafe source repository itself, where `templates/` holds
VibeSafe system files (`templates/requirements/`, `templates/tenets/`, etc.). However,
when VibeSafe is installed into a user project, that project may have its own `templates/`
directory containing user content. The blanket ignore silently prevents those files from
being committed.

**Discovered in**: the Explayner project, which uses `templates/` to hold starter YAML
files (`narration_template.yml`, `scene_timings_template.yml`) and a render wrapper
(`render.py`) that users copy when creating new animations. Running `git add templates/`
produced:

```
The following paths are ignored by one of your .gitignore files:
templates
```

The workaround applied in Explayner was to replace `templates/` with the specific
VibeSafe subdirectories:

```gitignore
# VibeSafe templates subdirectories (system files for VibeSafe development)
templates/requirements/
templates/tenets/
```

## Acceptance Criteria

- [ ] The auto-generated `.gitignore` does not ignore `templates/` as a whole
- [ ] Only the specific VibeSafe-managed subdirectories (`templates/requirements/`,
      `templates/tenets/`) are ignored in user project `.gitignore` files
- [ ] A user project with a `templates/` directory containing user content can `git add`
      those files without using `-f`
- [ ] Existing VibeSafe installations are updated by re-running `install.sh`

## Implementation Notes

The fix is in the `.gitignore` generation step within `install.sh` (or whatever script
writes the `.gitignore` block). Replace:

```bash
templates/
```

with:

```bash
templates/requirements/
templates/tenets/
```

Alternatively, if VibeSafe ever adds more system subdirectories under `templates/`, use
a comment-delimited block and list each one explicitly rather than ignoring the entire
directory.

## References

- Discovered while setting up the Explayner project (May 2026)
- Related: the `.venv` → `.venv-vibesafe` rename (2026-01-03_venv-naming-conflict) solved
  a similar class of problem: VibeSafe system names colliding with conventional user
  project names.

## Progress Updates

### 2026-05-10
Bug filed. Workaround applied in Explayner `.gitignore`.
