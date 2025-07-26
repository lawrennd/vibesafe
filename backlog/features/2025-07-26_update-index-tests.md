---
id: "2025-07-26_update-index-tests"
title: "Update Tests for Status Normalization in update_index.py"
status: "Completed"
priority: "High"
created: "2025-07-26"
last_updated: "2025-07-26"
category: "features"
---

# Task: Update Tests for Status Normalization in update_index.py

## Description

Update the existing test suite in `tests/test_update_index.py` to work with the new status normalization functionality implemented in the `update_index.py` script. Currently 5 out of 6 tests are failing due to changes in behavior.

## Motivation

The status normalization enhancement changed key behaviors:
- Status values are now normalized to lowercase with underscores
- The script now supports both YAML frontmatter AND old format (no longer raises ValueError)
- Tests need to reflect these new behaviors to ensure code quality

## Current Test Failures

```
FAILED (failures=5)

1. test_extract_yaml_frontmatter - Expected 'Ready' but got None
2. test_extract_task_metadata_yaml_frontmatter - Expected 'Ready' but got None  
3. test_extract_task_metadata_traditional - Expected ValueError but none raised
4. test_extract_task_metadata_both_formats - Different ID extraction behavior
5. test_case_insensitive_status_matching - Expected 'ready' but got None
```

## Acceptance Criteria

1. **Fix Status Normalization Tests**
   - [x] Update tests to expect normalized status values (lowercase with underscores)
   - [x] Verify `normalize_status()` function works correctly in tests
   - [x] Test multiple status formats: "Ready" → "ready", "In Progress" → "in_progress"

2. **Update Old Format Support Tests**
   - [x] Remove expectation of ValueError for missing YAML frontmatter
   - [x] Add tests for old format extraction working correctly
   - [x] Test that YAML frontmatter takes precedence when both formats present

3. **Add New Test Cases**
   - [x] Test `normalize_status()` function directly with various inputs
   - [x] Test handling of both 'updated' and 'last_updated' field names
   - [x] Test edge cases: empty status, None status, invalid status

4. **Update Expected Values**
   - [x] Change test assertions to expect normalized status values
   - [x] Update STATUSES constant expectations in tests
   - [x] Fix category and ID extraction test expectations

5. **Verify Backward Compatibility**
   - [x] Test that old task files still work
   - [x] Test that new YAML frontmatter files work
   - [x] Test mixed status formats are handled correctly

## Implementation Notes

### Key Changes Needed

1. **Fix status assertions**:
   ```python
   # OLD
   self.assertEqual(metadata['status'], 'Ready')
   
   # NEW 
   self.assertEqual(metadata['status'], 'ready')
   ```

2. **Remove ValueError expectations**:
   ```python
   # OLD - Remove this
   with self.assertRaises(ValueError):
       update_index.extract_task_metadata(Path(test_file_path))
   
   # NEW - Test that it works instead
   metadata = update_index.extract_task_metadata(Path(test_file_path))
   self.assertIsNotNone(metadata)
   ```

3. **Add normalize_status tests**:
   ```python
   def test_normalize_status(self):
       """Test the normalize_status function directly."""
       self.assertEqual(update_index.normalize_status('Ready'), 'ready')
       self.assertEqual(update_index.normalize_status('In Progress'), 'in_progress')
       self.assertEqual(update_index.normalize_status('proposed'), 'proposed')
       self.assertIsNone(update_index.normalize_status(''))
       self.assertIsNone(update_index.normalize_status(None))
   ```

### Investigation Needed

The tests show status values coming back as `None` instead of normalized values. Need to investigate:
- Is there an issue with the normalize_status function?
- Are the test files formatted correctly for the new parser?
- Is there a bug in the YAML frontmatter extraction?

## Testing Requirements

1. **All existing tests should pass** after updates
2. **New tests for normalization functionality**
3. **Edge case testing** for various status formats
4. **Integration testing** with real backlog files

## Files to Modify

- `tests/test_update_index.py` - Update all failing tests and add new ones

## Dependencies

- Completion of `2025-07-26_update-index-status-normalization` (completed)
- Python unittest framework

## Estimated Effort

**6 hours** - Need to investigate failures, update existing tests, and add comprehensive new test cases.

## Success Criteria

1. All tests in `test_update_index.py` pass 
2. Test coverage includes status normalization functionality
3. Both old and new format task files are tested
4. Edge cases are covered
5. No regression in existing functionality

## Progress Updates

### 2025-07-26
- Task created with Ready status
- Identified 5 failing tests due to status normalization changes
- Fixed import path issues in test file (added sys.path.insert)
- Updated all test expectations to match normalized status behavior
- Added comprehensive test for normalize_status() function directly
- Added test for both 'updated' and 'last_updated' field name support
- Removed ValueError expectations since both formats are now supported
- Status changed to Completed - all 8 tests now pass

## Related Items

- **Depends on**: `2025-07-26_update-index-status-normalization` (completed)
- **Blocks**: Confidence in status normalization implementation ✅ UNBLOCKED
- **Related**: Testing infrastructure for VibeSafe scripts 