---
id: "2026-01-03_process-conformance-validation"
title: "Create Process Conformance Validation Scripts"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_yaml-frontmatter-standardization"]
related_cips: ["0011"]
related_requirements: ["REQ-006"]
---

# Task: Create Process Conformance Validation Scripts

## Description

Create scripts that validate VibeSafe follows its own processes: YAML frontmatter validation, cross-reference checking, WHAT vs HOW heuristics, and status consistency. Can run as pre-commit hook or in CI.

This is dogfooding at its finest - validating that we follow our own principles!

## Acceptance Criteria

- [ ] Create scripts/validate_vibesafe.py
- [ ] YAML Frontmatter Validation
  - Check all required fields present for each component type
  - Validate field values (status is valid, dates formatted correctly)
  - Report missing or invalid fields with clear error messages
- [ ] Cross-Reference Validation
  - Check CIP references to requirements are valid
  - Check backlog references to CIPs/requirements are valid
  - Warn on orphaned components (no references)
  - Warn on broken references (reference to non-existent ID)
- [ ] WHAT vs HOW Heuristic (warnings only)
  - Detect implementation keywords in requirements
  - Suggest: "This looks like HOW - consider if it describes WHAT"
  - Keywords: "replace", "migrate", "create directory", "add script", etc.
- [ ] Status Consistency Checks (warnings only)
  - If requirement "Implemented", check if CIP exists and is "Implemented"
  - If all related CIPs "Closed", suggest requirement should be "Validated"
  - Cross-check backlog task status with CIP status
- [ ] Performance: Run in < 5 seconds for VibeSafe repo
- [ ] Can run as pre-commit hook
- [ ] Can run in CI
- [ ] Documentation of what each check does and why
- [ ] Test suite for validation logic

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

