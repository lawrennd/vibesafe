---
id: "2026-01-03_integrate-validator-whats-next"
title: "Phase 0c: Integrate Validator into What's Next Script"
status: "Completed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_process-conformance-validation"]
related_cips: ["0011"]
---

# Task: Phase 0c: Integrate Validator into What's Next Script

## Description

Integrate the VibeSafe structure validator into the `whats-next` script to provide validation feedback as part of the project status summary. This helps developers identify and fix structural issues as part of their regular workflow.

The validator should run silently and only show results if issues are found, keeping the "What's Next" output focused on actionable next steps.

## Acceptance Criteria

- [x] Add validator execution to `scripts/whats_next.py` (after analyzing project)
- [x] **Run validator silently**:
  - [x] Execute: `scripts/validate_vibesafe_structure.py` (no auto-fix)
  - [x] Capture errors, warnings, and summary
  - [x] Don't show output unless issues found
- [x] **Include validation in "Next Steps" section**:
  - [x] If errors: Add high-priority next step: "❌ Fix validation errors: ./scripts/validate_vibesafe_structure.py"
  - [x] If warnings only: Add medium-priority next step: "⚠️ Address validation warnings: ./scripts/validate_vibesafe_structure.py --strict"
  - [x] If issues can be auto-fixed: Suggest: "💡 Run with --fix to auto-correct common issues"
- [x] **Add validation summary to output**:
  - [x] Show count of errors/warnings in next steps
  - [x] Link to validator with fix command
- [x] **Add command-line flag**: `--skip-validation`
  - [x] For users who want faster output
  - [x] For CI/CD environments
- [x] **Performance**: Validation adds < 1 second to whats-next runtime
- [x] **Testing**: Tested with repo with errors, --skip-validation flag

## Implementation Notes

**Integration Point**: After scanning CIPs, backlog, and requirements, before generating next steps.

```python
def run_validation():
    """Run VibeSafe structure validation and return summary."""
    try:
        output, exit_code = run_command([
            sys.executable,
            os.path.join(SCRIPT_DIR, 'validate_vibesafe_structure.py'),
            '--no-color'
        ])
        
        # Parse output
        errors = re.search(r'ERRORS \((\d+)\)', output)
        warnings = re.search(r'WARNINGS \((\d+)\)', output)
        
        error_count = int(errors.group(1)) if errors else 0
        warning_count = int(warnings.group(1)) if warnings else 0
        
        return {
            'error_count': error_count,
            'warning_count': warning_count,
            'has_issues': error_count > 0 or warning_count > 0,
            'exit_code': exit_code
        }
    except Exception as e:
        return {'error': str(e)}

# In main():
if not args.skip_validation:
    validation = run_validation()
    
    if validation.get('has_issues'):
        # Add to next steps
        if validation['error_count'] > 0:
            next_steps.insert(0, {
                'priority': 'high',
                'action': f"Fix {validation['error_count']} validation errors",
                'command': './scripts/validate_vibesafe_structure.py --fix'
            })
        elif validation['warning_count'] > 0:
            next_steps.append({
                'priority': 'medium',
                'action': f"Address {validation['warning_count']} validation warnings",
                'command': './scripts/validate_vibesafe_structure.py --strict'
            })
```

**User Experience**:
- Seamless: Validation happens in the background
- Focused: Only shows issues if found
- Actionable: Provides clear commands to fix issues
- Optional: Can skip for speed

## Related

- CIP: 0011
- Requirement: REQ-0006 (Process Conformance Validation)
- Depends on: 2026-01-03_process-conformance-validation (Phase 0a - COMPLETED)
- Related: 2026-01-03_project-summary-tool (Phase 4 - may consolidate validation)

## Progress Updates

### 2026-01-03 (Completed)
✅ Task completed successfully!

**Implementation details:**
- Created `run_validation()` function in whats_next.py
- Runs validator silently in background
- Parses output for error/warning counts
- Adds validation issues as first next step if found
- `--skip-validation` flag skips validation entirely

**Testing performed:**
- ✅ Validation runs by default (found 124 errors in VibeSafe)
- ✅ Errors appear as high-priority next step
- ✅ --skip-validation flag works correctly
- ✅ Adds < 1 second to runtime
- ✅ Graceful error handling if validator missing

**Next step**: Phase 0d for intelligent gap detection and AI-assisted suggestions

