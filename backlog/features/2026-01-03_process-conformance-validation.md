---
id: "2026-01-03_process-conformance-validation"
title: "Phase 0a: Create Validation Script (DO FIRST)"
status: "Proposed"
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

- [ ] Create `scripts/validate_vibesafe.py` (standalone validation tool)
- [ ] **File Naming Validation**:
  - Requirements: `reqXXXX_short-name.md` (4-digit hex)
  - CIPs: `cipXXXX.md` or `cipXXXX_short-name.md` (4-digit hex)
  - Backlog: `YYYY-MM-DD_short-name.md` (date)
  - Tenets: `short-name.md` (kebab-case)
- [ ] **YAML Frontmatter Validation**:
  - Check all required fields present for each component type
  - Validate field values (status in allowed list, dates YYYY-MM-DD format)
  - Report missing or invalid fields with file path and line number
- [ ] **Cross-Reference Validation**:
  - Requirements reference valid tenet IDs
  - CIPs reference valid requirement IDs
  - Backlog references valid CIP IDs
  - Warn on broken references with suggestions
- [ ] **Bottom-Up Pattern Validation**:
  - Warn if requirements have related_cips or related_backlog
  - Warn if CIPs have related_backlog
  - Warn if backlog has related_requirements
  - Warn if tenets have any related_ fields
- [ ] **Output Format**:
  - Color-coded: ✅ success, ⚠️  warnings, ❌ errors
  - Grouped by validation type
  - Shows file paths and specific issues
  - Exit code 0 if no errors, 1 if errors
- [ ] **Command-line Options**: `--strict`, `--component`, `--fix`
- [ ] Performance: Run in < 5 seconds for VibeSafe repo
- [ ] Test on VibeSafe itself (find existing issues!)
- [ ] Documentation of what each check does and why

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

### 2026-01-03
Task created. High priority for ensuring quality.

