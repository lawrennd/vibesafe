---
title: "Make combine_tenets.py Project-Agnostic Instead of Hardcoded for 'vibesafe'"
id: "2025-07-28_vibesafe-combine-tenets-project-detection"
status: "proposed"
priority: "medium"
created: "2025-07-28"
updated: "2025-07-28"
owner: "Neil"
dependencies: []
category: "infrastructure"
---

# Task: Make combine_tenets.py Project-Agnostic Instead of Hardcoded for 'vibesafe'

## Description

The `combine_tenets.py` script in VibeSafe is currently hardcoded to work with the `'vibesafe'` directory, but it should be project-agnostic. When installed via `install-minimal.sh` in other projects, it should automatically detect the current project and work with that project's tenets.

## Current Issue

The script contains hardcoded references to the 'vibesafe' project:

```python
# Combine VibeSafe tenets
combine_tenets(
    'vibesafe',  # ← Hardcoded project name
    'vibesafe-tenets.md',
    'vibesafe-tenets.yaml'
)
```

When installed in other projects (like The Inaccessible Game), this fails because:
- There's no `tenets/vibesafe/` directory in other projects
- The script expects VibeSafe's specific directory structure
- Other projects have their own tenet directories (e.g., `tenets/inaccessible-game/`)

## Acceptance Criteria

### 1. Auto-Detect Project Name
- [ ] Script automatically detects current project name from:
  - Git remote URL (e.g., `github.com/lawrennd/the-inaccessible-game` → `inaccessible-game`)
  - Current directory name as fallback
  - Environment variable override option

### 2. Project-Agnostic Directory Structure
- [ ] Script works with any project's tenet directory structure
- [ ] Supports both single-project and multi-project modes
- [ ] Maintains backward compatibility with VibeSafe's own usage

### 3. Flexible Output Naming
- [ ] Generated files use detected project name:
  - `{project}-tenets.md` instead of `vibesafe-tenets.md`
  - `{project}-tenets.yaml` instead of `vibesafe-tenets.yaml`

### 4. Error Handling
- [ ] Graceful handling when no tenet directory exists
- [ ] Clear error messages for missing dependencies
- [ ] Fallback to minimal functionality when auto-detection fails

## Implementation Notes

### Detection Strategy
```python
def detect_project_name():
    # Try git remote first
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extract project name from URL
            project = extract_project_from_url(url)
            if project:
                return project
    except:
        pass
    
    # Fallback to directory name
    return os.path.basename(os.getcwd())
```

### Backward Compatibility
- Keep existing hardcoded behavior as fallback
- Add `--project` flag for explicit project specification
- Support `VIBESAFE_PROJECT` environment variable

### Testing Requirements
- Test with VibeSafe's own repository (should still work)
- Test with The Inaccessible Game repository
- Test with repositories without git remotes
- Test with custom project names via environment variables

## Related Work

- **VibeSafe Repository**: https://github.com/lawrennd/vibesafe
- **Current Script Location**: `tenets/combine_tenets.py`
- **Installation Script**: `scripts/install-minimal.sh` (expects this functionality)
- **Related Task**: "Ensure combine_tenets.py includes cursor rules generation functionality"

## Impact

### Benefits
- **Universal Compatibility**: Works with any project using VibeSafe
- **Better User Experience**: No manual configuration required
- **Consistent Behavior**: Same script works across all VibeSafe projects

### Risks
- **Breaking Changes**: Could affect existing VibeSafe workflows
- **Complexity**: Adds detection logic that could fail in edge cases

## Success Metrics

- [ ] Script works correctly in The Inaccessible Game project
- [ ] Script still works correctly in VibeSafe's own repository
- [ ] No manual configuration required for new projects
- [ ] Clear error messages when auto-detection fails 