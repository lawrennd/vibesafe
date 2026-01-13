---
category: features
created: '2025-07-26'
id: 2025-07-26_whats-next-status-normalization
last_updated: '2025-07-26'
priority: Medium
related_cips: []
owner: "Neil Lawrence"
status: Completed
title: What's Next Script Status Normalization Enhancement
---

# Task: What's Next Script Status Normalization Enhancement

## Description

Apply the same status normalization improvements to the `whats_next.py` script that were implemented in `update_index.py`. This will ensure consistent status handling across both scripts when processing backlog items with different status formatting conventions.

## Motivation

The `whats_next.py` script currently has similar status handling logic to the old `update_index.py` but doesn't benefit from the status normalization improvements. This could lead to:
- Inconsistent behavior between the two scripts
- Tasks being incorrectly categorized or missed in the what's next analysis
- Confusion when using different status formats across task files

## Acceptance Criteria

1. **Status Normalization Function**
   - [x] Add `normalize_status()` function matching the implementation in `update_index.py`
   - [x] Handle conversion of spaces to underscores and hyphens to underscores
   - [x] Return None for empty/invalid status values

2. **Backlog Status Processing**
   - [x] Apply `normalize_status()` when extracting status from YAML frontmatter in `scan_backlog()`
   - [x] Apply normalization when extracting status from old format parsing
   - [x] Update status checking logic to use normalized values

3. **Constants Consistency**
   - [x] Ensure status constants in `scan_backlog()` match the normalized format: `['proposed', 'ready', 'in_progress', 'completed', 'abandoned']`

4. **Documentation Enhancement**
   - [x] Update module docstring to mention multi-format status support
   - [x] Add comments explaining status normalization behavior

5. **Output Consistency**
   - [x] Maintain existing display format for status names in output
   - [x] Ensure backward compatibility with current output format

6. **Testing Compatibility**
   - [x] Verify that both scripts handle the same task files consistently
   - [x] Test with mixed status formats to ensure both scripts agree

## Implementation Notes

### Key Changes Required

1. **Add normalize_status function** (same as update_index.py):
   ```python
   def normalize_status(status):
       """Normalize status to lowercase with underscores."""
       if not status:
           return None
       # Convert to lowercase and replace spaces with underscores
       return status.lower().replace(' ', '_').replace('-', '_')
   ```

2. **Update scan_backlog() function**:
   - Apply normalization: `status = normalize_status(frontmatter.get('status', 'unknown'))`
   - Apply normalization in old format parsing: `status = normalize_status(status_match.group(1)) if status_match else "unknown"`

3. **Ensure consistency with update_index.py**:
   - Use the same status constants
   - Apply the same normalization logic
   - Handle edge cases similarly

### Files to Modify

- `scripts/whats_next.py` - Main implementation

### Areas of Focus

1. **scan_backlog() function** (lines ~351-434):
   - Line ~365: `status = frontmatter.get('status', 'unknown').lower()`
   - Line ~406: `status = status_match.group(1).lower() if status_match else "unknown"`
   - Status checking logic throughout the function

2. **Status constants in backlog_info structure** (lines ~354-361):
   - Ensure consistency with normalized format

## Testing Requirements

1. **Cross-script consistency**:
   - Run both `update_index.py` and `whats_next.py` on the same backlog
   - Verify they categorize tasks consistently
   - Test with various status formats

2. **Status format compatibility**:
   - "Proposed", "In Progress", "Completed" (current format)
   - "proposed", "in_progress", "completed" (normalized format)
   - "Ready", "abandoned" (mixed case)

3. **Output verification**:
   - Ensure output formatting remains user-friendly
   - Verify no regression in displayed information

## Dependencies

- Completion of `2025-07-26_update-index-status-normalization` task
- No new external dependencies required
- Existing: PyYAML, pathlib, re, os, subprocess

## Estimated Effort

**4 hours** - Similar changes to update_index.py but in a different script with additional output formatting considerations.

## Progress Updates

### 2025-07-26
- Task created with Proposed status
- Status changed to In Progress to begin implementation
- Added normalize_status() function to scripts/whats_next.py (matching update_index.py)
- Updated module docstring to document multi-format status support
- Applied status normalization in scan_backlog() for both YAML frontmatter and old format parsing
- Added comprehensive test suite (4 new tests) covering:
  - normalize_status() function testing with various inputs
  - scan_backlog() status normalization for YAML frontmatter
  - scan_backlog() status normalization for old format files  
  - Cross-script consistency testing between update_index.py and whats_next.py
- All 10 tests passing (4 new + 6 existing)
- Status changed to Completed - full implementation verified

## Related Items

- **Depends on**: `2025-07-26_update-index-status-normalization` (completed)
- **Follow-up of**: Update index script status normalization implementation
- **Related**: Status normalization consistency across VibeSafe scripts ✅ ACHIEVED

## Success Criteria

1. Both `update_index.py` and `whats_next.py` handle status formats consistently
2. No regression in existing functionality or output format
3. All status formats are correctly normalized and processed
4. Cross-script compatibility verified through testing