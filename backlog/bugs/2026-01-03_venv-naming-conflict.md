---
id: "2026-01-03_venv-naming-conflict"
title: "VibeSafe .venv conflicts with user project virtual environments"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "bugs"
---

# Bug: VibeSafe .venv conflicts with user project virtual environments

## Description

VibeSafe currently creates a `.venv` directory to install its own dependencies (PyYAML for the `whats-next` script). However, many projects also use `.venv` as their standard virtual environment name for project dependencies. This creates ambiguity and confusion about which environment is active:

- **Current behavior**: VibeSafe installation creates `.venv` with PyYAML
- **Problem**: User projects often use `.venv` for their own dependencies
- **Impact**: Confusion about which environment is active, potential dependency conflicts, unclear separation of concerns

### Example Scenarios

1. **Scenario 1**: User has existing `.venv` for their project → VibeSafe installation overwrites/modifies it
2. **Scenario 2**: User creates `.venv` after VibeSafe installation → User's venv replaces VibeSafe's venv, breaking `whats-next` script
3. **Scenario 3**: Multiple shell sessions → Unclear which venv should be activated for which purpose

## Acceptance Criteria

- [ ] VibeSafe virtual environment has a distinct name that doesn't conflict with user projects
- [ ] Installation scripts updated to use new venv name
- [ ] Wrapper scripts (`whats-next`) updated to reference new venv
- [ ] `.gitignore` updated to ignore the new venv directory
- [ ] Documentation updated to reflect the change
- [ ] Tests updated to use new venv name
- [ ] Solution maintains "clean installation" philosophy

## Implementation Options

### Option 1: Use VibeSafe-specific virtual environment name ✅ **Recommended**

**Change**: Rename `.venv` → `.venv-vibesafe`

**Files to modify**:
- `install-whats-next.sh` (line 29: `VENV_DIR=".venv-vibesafe"`)
- `scripts/install-minimal.sh` (line 307-308, 315, 321: use `.venv-vibesafe`)
- `whats-next` wrapper (line 21, 85: reference `.venv-vibesafe`)
- `.gitignore` VibeSafe section (add `.venv-vibesafe`)
- `tests/test_whats_next.py` (update test fixtures if needed)

**Pros**:
- Clear separation between VibeSafe tools and user project
- Minimal disruption to existing structure
- Easy to identify which venv is which
- Simple find-and-replace implementation
- Maintains flat project structure

**Cons**:
- Two venv directories at project root (minor visual clutter)
- Users with existing installations need to run update script

**Implementation complexity**: Low (simple rename across files)

### Option 2: Put VibeSafe infrastructure in subdirectory

**Change**: Create `.vibesafe/` directory structure:
```
.vibesafe/
├── .venv/          # VibeSafe's Python environment
├── scripts/        # Move whats_next.py here
└── config/         # Future: VibeSafe configuration
```

**Files to modify**:
- All installation scripts (major path updates)
- `whats-next` wrapper (update paths)
- `.gitignore` (update to ignore `.vibesafe/`)
- Documentation (update all references to script locations)
- Tests (update path references)

**Pros**:
- Clean project root (all VibeSafe infrastructure contained)
- Clear organizational boundary
- Future-proof for additional VibeSafe tools
- Scalable if VibeSafe grows

**Cons**:
- More disruptive change to existing installations
- Requires migration strategy for existing users
- More files to update
- Changes user-facing paths (`./whats-next` might move)

**Implementation complexity**: Medium-High (significant restructuring)

### Option 3: No virtual environment (assume system dependencies)

**Change**: Remove virtual environment, rely on system Python and PyYAML

**Pros**:
- Simplest possible approach
- No venv naming conflicts
- Faster installation (no venv creation)

**Cons**:
- **Violates "clean installation" philosophy** (requires user to manage dependencies)
- Breaks on systems without PyYAML installed
- Version conflicts possible with system packages
- Less isolated and reproducible

**Implementation complexity**: Low (remove venv logic)
**Recommendation**: ❌ **Reject** - violates core VibeSafe principles

### Option 4: Dynamic venv detection and creation

**Change**: Check if `.venv` exists and belongs to VibeSafe, otherwise use `.venv-vibesafe`

**Pros**:
- Backwards compatible with existing installations
- Smart adaptation to environment

**Cons**:
- Complex logic to determine "ownership" of `.venv`
- Fragile detection mechanism
- Still doesn't solve the fundamental ambiguity problem
- More code to maintain and test

**Implementation complexity**: High (detection logic, edge cases)
**Recommendation**: ❌ **Reject** - adds complexity without solving root cause

## Recommended Solution

**Option 1: Rename to `.venv-vibesafe`**

This is the cleanest solution that:
1. Solves the naming conflict completely
2. Requires minimal code changes
3. Maintains the clean installation philosophy
4. Is immediately obvious which venv is for what purpose
5. Easy to test and verify

## Implementation Notes

### Migration Strategy

For existing installations, the update process should:
1. Detect if `.venv` exists and appears to be VibeSafe-managed (contains only PyYAML)
2. Rename `.venv` → `.venv-vibesafe`
3. Or: Simply create `.venv-vibesafe` fresh (if `.venv` has other packages, likely user's)

### Testing Strategy

- Test fresh installation creates `.venv-vibesafe`
- Test update from `.venv` to `.venv-vibesafe`
- Test `whats-next` wrapper works with new venv
- Test installation when user already has `.venv` for their project

## Related

- Installation scripts: `install-whats-next.sh`, `scripts/install-minimal.sh`
- VibeSafe Update Guide: `.cursor/rules/vibesafe_update.md`
- Clean Installation Philosophy: `cip/cip000E.md` (if exists)

## Progress Updates

### 2026-01-03
Bug identified and documented with implementation options.

