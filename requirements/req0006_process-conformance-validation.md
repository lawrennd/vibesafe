---
id: "0006"
title: "Automated Process Conformance Validation"
status: "Ready"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: ["0011"]
related_backlog: []
stakeholders: ["developers", "maintainers", "vibesafe-itself"]
tags:
  - validation
  - quality
  - automation
  - dogfooding
---

# Requirement 0006: Automated Process Conformance Validation

## Description

VibeSafe should validate that it follows its own processes and principles. Automated scripts should check that components conform to established patterns: proper YAML frontmatter, valid cross-references, requirements focus on outcomes (WHAT), and status consistency across related components.

This validation should run as part of testing/CI to catch process violations early. It should provide helpful feedback when violations occur, not just fail silently. The validation should be fast enough to run frequently without disrupting workflow.

By validating our own conformance, we demonstrate VibeSafe's principles in action and build confidence that the system works as designed.

## Acceptance Criteria

- [ ] Script validates YAML frontmatter in all component types
- [ ] Script validates cross-references (requirements ↔ CIPs ↔ backlog)
- [ ] Script warns if requirements appear to describe implementation (HOW not WHAT)
- [ ] Script checks status consistency across related components
- [ ] Script validates required fields are present
- [ ] Validation errors provide clear, actionable feedback
- [ ] Script runs in < 5 seconds for VibeSafe repository
- [ ] Script can run as pre-commit hook or in CI
- [ ] Documentation explains what each validation checks and why

## Notes

**Validation Types:**

1. **YAML Frontmatter**:
   - All required fields present (id, title, status, created, etc.)
   - Field values are valid (status is one of allowed values)
   - Dates are properly formatted (YYYY-MM-DD)

2. **Cross-References**:
   - CIP references requirements that exist
   - Backlog references CIPs/requirements that exist
   - Requirements referenced by CIPs are marked appropriately

3. **WHAT vs HOW (Heuristic)**:
   - Warn if requirement contains implementation keywords
   - Suggest: "This looks like HOW - consider if it describes WHAT"
   - Not an error (heuristic), but helpful guidance

4. **Status Consistency**:
   - If requirement is "Implemented", at least one CIP should be "Implemented"
   - If all CIPs are "Closed", requirement should be "Validated"
   - Warnings, not hard failures

**False Positives OK**: Better to warn and let humans judge than miss actual issues.

**Dogfooding**: This requirement itself will be validated by the script we build!

