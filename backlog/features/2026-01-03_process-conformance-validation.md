---
id: "2026-01-03_process-conformance-validation"
title: "Phase 0a: Create Validation Script (DO FIRST)"
status: "Completed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: []
related_cips: ["0011"]
---

# Task: Phase 0a: Create Validation Script (DO FIRST)

## Description

**DO THIS FIRST** - Build the validation tool BEFORE implementing CIP-0011 changes, so we can verify our work as we go.

Create `scripts/validate_vibesafe.py` that validates VibeSafe follows its own specifications from CIP-0011: file naming, YAML frontmatter, cross-references, and bottom-up linking pattern. This is our "gold standard" checker.

This is dogfooding at its finest - the tool validates we follow our own specs!

## Acceptance Criteria

- [x] Create `scripts/validate_vibesafe_structure.py` (standalone validation tool)
- [x] **File Naming Validation**:
  - Requirements: `reqXXXX_short-name.md` (4-digit hex)
  - CIPs: `cipXXXX.md` or `cipXXXX_short-name.md` (4-digit hex)
  - Backlog: `YYYY-MM-DD_short-name.md` (date)
  - Tenets: `short-name.md` (kebab-case)
- [x] **YAML Frontmatter Validation**:
  - Check all required fields present for each component type
  - Validate field values (status in allowed list, dates YYYY-MM-DD format)
  - Report missing or invalid fields with file path and line number
- [x] **Cross-Reference Validation**:
  - Requirements reference valid tenet IDs
  - CIPs reference valid requirement IDs
  - Backlog references valid CIP IDs
  - Warn on broken references with suggestions
- [x] **Bottom-Up Pattern Validation**:
  - Warn if requirements have related_cips or related_backlog
  - Warn if CIPs have related_backlog
  - Warn if backlog has related_requirements
  - Warn if tenets have any related_ fields
- [x] **Output Format**:
  - Color-coded: ✅ success, ⚠️  warnings, ❌ errors
  - Grouped by validation type
  - Shows file paths and specific issues
  - Exit code 0 if no errors, 1 if errors
- [x] **Command-line Options**: `--strict`, `--component`, `--fix`, `--fix-links`, `--dry-run`
- [x] **Auto-fix functionality**: Capitalize status/priority, add missing fields, fix reverse links
- [x] Performance: Run in < 5 seconds for VibeSafe repo
- [x] **Refactored to use python-frontmatter** for simpler, more robust parsing
- [x] **Comprehensive test suite** (32 tests covering all functionality)
- [x] Test on VibeSafe itself (find existing issues!)
- [x] Documentation of what each check does and why

## Implementation Notes

**Philosophy**: Better to warn and let humans judge than miss issues.

**Output Format**:
```
✅ YAML Validation: 45 components checked, 0 errors
⚠️  Cross-References: 3 warnings
  - CIP-0011 references REQ-007 which doesn't exist
  - REQ-002 has no related CIPs (consider creating one?)
✅ WHAT vs HOW: 0 warnings
⚠️  Status Consistency: 1 warning
  - REQ-001 status is "Implemented" but no CIP is "Implemented"
```

**False Positives OK**: Heuristics will have false positives. That's fine - they provide helpful nudges, not hard requirements.

## Related

- CIP: 0011
- Requirement: REQ-006
- Depends on: 2026-01-03_yaml-frontmatter-standardization

## Progress Updates

### 2026-01-03 (Completed)
✅ Task completed successfully!

**What was delivered:**
- Created `validate_vibesafe_structure.py` with comprehensive validation
- Validates file naming, YAML frontmatter, cross-references, bottom-up pattern
- Auto-fix with `--fix` (safe single-file) and `--fix-links` (multi-file)
- Refactored to use python-frontmatter package (cleaner, more robust)
- 32 comprehensive tests (100% passing)
- Follows VibeSafe testing conventions (tests/ for Python, scripts/test/ for BATS)

**Next steps** (see new backlog tasks):
- Integrate into install-minimal.sh (with user prompt for auto-fix)
- Integrate into whats-next script (as validator)

