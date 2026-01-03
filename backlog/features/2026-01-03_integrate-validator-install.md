---
id: "2026-01-03_integrate-validator-install"
title: "Phase 0b: Integrate Validator into Install Script"
status: "Completed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_process-conformance-validation"]
related_cips: ["0011"]
---

# Task: Phase 0b: Integrate Validator into Install Script

## Description

Integrate the VibeSafe structure validator into `install-minimal.sh` to ensure all VibeSafe installations maintain quality standards. The validator should run automatically with a dry-run first, then prompt the user to apply fixes if issues are found.

This ensures every VibeSafe installation is validated against REQ-0001 and REQ-0006 specifications.

## Acceptance Criteria

- [x] Add validator execution to `install-minimal.sh` (after system files deployed)
- [x] **Run validator in dry-run mode first**:
  - [x] Execute: `.venv-vibesafe/bin/python scripts/validate_vibesafe_structure.py --dry-run --fix --fix-links`
  - [x] Show what would be fixed (colored output)
  - [x] Count total fixes that would be applied
- [x] **Prompt user if fixes needed**:
  - [x] "Found X issues that can be auto-fixed. Apply fixes? [y/N]"
  - [x] If yes: Run with `--fix --fix-links` (no dry-run)
  - [x] If no: Continue with warning about validation failures
  - [x] Show summary of what was fixed
- [x] **Handle validation failures gracefully**:
  - [x] If errors remain after fixes: Show error report
  - [x] Provide guidance on manual fixes needed
  - [x] Don't block installation (warn only)
- [x] **Skip validation if requested**:
  - [x] Add `VIBESAFE_SKIP_VALIDATION` environment variable
  - [x] Useful for CI/CD or automated installs
- [x] **Performance**: Validation completes in < 5 seconds
- [x] **Non-interactive mode detection**: Skips prompt in CI/CD
- [x] **Testing**: Tested with issues, skip mode, and non-interactive mode

## Implementation Notes

**Integration Point**: After deploying system files, before final success message.

```bash
# After deploying system files
info "Validating VibeSafe structure..."

# Run validator in dry-run mode
if [ -z "$VIBESAFE_SKIP_VALIDATION" ]; then
  DRY_RUN_OUTPUT=$(.venv-vibesafe/bin/python scripts/validate_vibesafe_structure.py --dry-run --fix --fix-links 2>&1)
  VALIDATION_EXIT=$?
  
  if [ $VALIDATION_EXIT -ne 0 ]; then
    echo "$DRY_RUN_OUTPUT"
    
    # Count fixes
    FIX_COUNT=$(echo "$DRY_RUN_OUTPUT" | grep -oP 'WOULD FIX \(\K\d+' || echo "0")
    
    if [ "$FIX_COUNT" -gt 0 ]; then
      read -p "Found $FIX_COUNT issues that can be auto-fixed. Apply fixes? [y/N] " -n 1 -r
      echo
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        .venv-vibesafe/bin/python scripts/validate_vibesafe_structure.py --fix --fix-links
        success "Applied $FIX_COUNT automatic fixes"
      else
        warn "Skipped automatic fixes. Run manually: ./scripts/validate_vibesafe_structure.py --fix --fix-links"
      fi
    fi
  else
    success "VibeSafe structure validated successfully"
  fi
fi
```

**User Experience**:
- Non-intrusive: Only prompts if issues found
- Transparent: Shows exactly what would be fixed
- Opt-out: Can skip with environment variable
- Educational: Users see validation in action

## Related

- CIP: 0011
- Requirement: REQ-0006 (Process Conformance Validation)
- Depends on: 2026-01-03_process-conformance-validation (Phase 0a - COMPLETED)
- Blocks: Phase 0 (YAML Frontmatter Standardization)

## Progress Updates

### 2026-01-03 (Completed)
✅ Task completed successfully!

**Implementation details:**
- Created `run_vibesafe_validation()` function in install-minimal.sh
- Runs after tenet generation, before cleanup
- Dry-run shows 122 fixable issues in current VibeSafe
- User prompt works in interactive mode
- Non-interactive mode detected and handled gracefully
- VIBESAFE_SKIP_VALIDATION environment variable works
- Validation result shown in success message

**Testing performed:**
- ✅ Dogfood install with validation issues (found 122 fixable items)
- ✅ Non-interactive mode detection (piped input)
- ✅ VIBESAFE_SKIP_VALIDATION environment variable
- ✅ No bash syntax errors
- ✅ Integration with existing install flow

