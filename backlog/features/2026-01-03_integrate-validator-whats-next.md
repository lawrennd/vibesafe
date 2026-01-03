---
id: "2026-01-03_integrate-validator-whats-next"
title: "Phase 0c: Integrate Validator into What's Next Script"
status: "Ready"
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

- [ ] Add validator execution to `scripts/whats_next.py` (after analyzing project)
- [ ] **Run validator silently**:
  - [ ] Execute: `scripts/validate_vibesafe_structure.py` (no auto-fix)
  - [ ] Capture errors, warnings, and summary
  - [ ] Don't show output unless issues found
- [ ] **Include validation in "Next Steps" section**:
  - [ ] If errors: Add high-priority next step: "❌ Fix validation errors: ./scripts/validate_vibesafe_structure.py"
  - [ ] If warnings only: Add medium-priority next step: "⚠️ Address validation warnings: ./scripts/validate_vibesafe_structure.py --strict"
  - [ ] If issues can be auto-fixed: Suggest: "💡 Run with --fix to auto-correct common issues"
- [ ] **Add validation summary to output**:
  - [ ] Show count of errors/warnings
  - [ ] Show most common issue types
  - [ ] Link to validator help: `--help` for options
- [ ] **Add command-line flag**: `--skip-validation`
  - [ ] For users who want faster output
  - [ ] For CI/CD environments
- [ ] **Performance**: Validation should add < 2 seconds to whats-next runtime
- [ ] **Documentation**: Update whats-next docs with validation feature
- [ ] **Testing**: Test with clean repo, repo with errors, repo with warnings

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

### 2026-01-03
Task created. Medium priority for developer workflow integration.

