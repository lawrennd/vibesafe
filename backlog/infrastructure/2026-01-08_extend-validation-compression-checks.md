---
id: "2026-01-08_extend-validation-compression-checks"
title: "Extend Validation Script with Compression Checks"
status: "Proposed"
priority: "Medium"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "infrastructure"
related_cips: ["0011", "0013"]
owner: "Neil Lawrence"
dependencies: []
tags: ["validation", "compression", "documentation", "quality"]
---

# Task: Extend Validation Script with Compression Checks

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task extends CIP-0011's validation script to detect compression issues from CIP-0013.

## Description

Extend `scripts/validate_vibesafe_structure.py` to validate documentation compression compliance. Currently, the validation script checks VibeSafe structure (requirements, CIPs, backlog, tenets) but doesn't validate that closed CIPs have been compressed into formal documentation.

**Why this matters**: Compression (CIP-0013) is now part of VibeSafe's workflow, but there's no automated check that it's being followed. The validation script should detect uncompressed closed CIPs and verify compression completeness.

**Discovered**: During CIP-0013 compression, we noticed `./whats-next --compression-check` detects issues but the validation script doesn't.

## Acceptance Criteria

### Basic Compression Validation
- [ ] Check that closed CIPs have `compressed` field in YAML frontmatter
- [ ] Warn if closed CIP has `compressed: false` (or missing field)
- [ ] Detect closed CIPs older than 30 days without compression
- [ ] Count and report total uncompressed closed CIPs

### Compression Quality Checks
- [ ] Verify `compressed: true` CIPs have traceability in documentation
  - [ ] Search `docs/` for references to the CIP ID
  - [ ] Check README.md for high-level references
  - [ ] Warn if compressed CIP has no documentation references
- [ ] Flag CIPs with invalid `compressed` values (not true/false)
- [ ] Optional: Check that compression guide exists (`docs/source/compression-guide.md`)

### Validation Output
- [ ] Add "Compression Status" section to validation output
- [ ] Show count of compressed vs. uncompressed closed CIPs
- [ ] List oldest uncompressed CIP (if >30 days)
- [ ] Warning (not error) level for compression issues
- [ ] Link to compression guide in warnings

### Command Line Options
- [ ] Add `--compression-only` flag to check only compression
- [ ] Add `--skip-compression` flag to skip compression checks
- [ ] Include compression in default validation run

## Implementation Notes

### Detection Logic

**Pseudo-code**:
```python
def validate_compression(cips_info):
    closed_cips = [cip for cip in cips_info if cip['status'] == 'Closed']
    
    for cip in closed_cips:
        # Check 1: Has compressed field?
        if 'compressed' not in cip:
            warn(f"CIP-{cip['id']} closed but missing 'compressed' field")
        
        # Check 2: Is it false?
        elif cip['compressed'] == False:
            days_closed = calculate_days_since(cip['last_updated'])
            if days_closed > 30:
                warn(f"CIP-{cip['id']} closed {days_closed} days ago, not compressed")
        
        # Check 3: If true, has docs references?
        elif cip['compressed'] == True:
            if not find_cip_references_in_docs(cip['id']):
                warn(f"CIP-{cip['id']} marked compressed but no docs references found")
```

### Documentation Search

Search for CIP references in:
- `docs/**/*.md` files
- `docs/**/*.rst` files (if Sphinx)
- `README.md`

**Search patterns**:
- `CIP-{id}` (e.g., "CIP-0013")
- `cip{id}.md` (e.g., "cip0013.md")
- `cip/{id}` (in links)

### Output Format

```
Compression Status:
  ✅ 1 closed CIP compressed (7%)
  ⚠️  13 closed CIPs need compression (93%)
  
  Oldest uncompressed: CIP-0006 (248 days)
  
  ⚠️  WARNING: High compression backlog (>10 CIPs)
  → Run: ./whats-next --compression-check
  → Guide: docs/source/compression-guide.md
```

### Integration with whats-next

**Division of responsibility**:
- `whats-next`: Proactive suggestions during development
- `validate_vibesafe_structure.py`: Conformance checking (CI/CD, pre-commit)

Both tools should detect the same issues but serve different purposes:
- `whats-next`: "You should compress CIP-0013"
- `validate`: "13 closed CIPs violate compression policy"

## Testing Strategy

### Unit Tests

Add to `tests/test_validate_vibesafe_structure.py`:

```python
def test_compression_validation_closed_without_field():
    # CIP closed, no compressed field → warning
    
def test_compression_validation_closed_false():
    # CIP closed, compressed: false → warning
    
def test_compression_validation_old_uncompressed():
    # CIP closed >30 days, uncompressed → high priority warning
    
def test_compression_validation_compressed_true_with_docs():
    # CIP compressed: true, found in docs → pass
    
def test_compression_validation_compressed_true_no_docs():
    # CIP compressed: true, NOT in docs → warning
```

### Integration Tests

```bash
# Test with real VibeSafe structure
python scripts/validate_vibesafe_structure.py --compression-only

# Should show:
# - CIP-0013: compressed: true, found in docs/source/compression-guide.md ✅
# - CIP-000F: compressed: false, 5 days old ⚠️
# - CIP-0006: compressed: false, 248 days old ⚠️⚠️
```

## Related

- **CIP-0011**: VibeSafe Structure Validator (the script we're extending)
- **CIP-0013**: Documentation Compression Stage (the workflow we're validating)
- **REQ-000E**: Documentation Synchronization with Implementation
- **Tool**: `scripts/validate_vibesafe_structure.py`
- **Tool**: `scripts/whats_next.py` (compression detection already implemented)

## Progress Updates

### 2026-01-08
Task created with "Proposed" status. 

**Context**: During CIP-0013 compression, we realized the validation script doesn't check compression compliance. `whats-next` detects issues but validation should too for CI/CD and conformance checking.

**Why Now**: Compression is now part of VibeSafe's workflow (CIP-0013 closed). Need validation to ensure it's followed.

**Priority**: Medium (not blocking, but important for workflow enforcement)

## Benefits

- **Automated detection**: CI/CD catches uncompressed CIPs early
- **Quality enforcement**: Prevents compression backlog from growing
- **Conformance**: Validates CIP-0013 workflow is being followed
- **Traceability**: Ensures compressed CIPs have documentation references
- **Metrics**: Track compression compliance over time

