---
id: "2025-07-26_update-index-status-normalization"
title: "Update Index Script Status Normalization Enhancement"
status: "Completed"
priority: "Medium"
created: "2025-07-26"
last_updated: "2025-07-26"
category: "features"
---

# Task: Update Index Script Status Normalization Enhancement

## Description

Enhance the `update_index.py` script to better handle status values in multiple formats by implementing status normalization. This will make the script more robust when processing task files with different status formatting conventions.

## Motivation

Currently, the script expects status values in a specific format (capitalized with spaces like "In Progress"), but task files may use various formats like lowercase with underscores ("in_progress") or mixed case. This inconsistency can cause tasks to be incorrectly categorized or skipped entirely.

## Acceptance Criteria

1. **Status Normalization Function**
   - [x] Add `normalize_status()` function that converts status values to lowercase with underscores
   - [x] Handle conversion of spaces to underscores and hyphens to underscores
   - [x] Return None for empty/invalid status values

2. **Constants Update**
   - [x] Change `STATUSES` constant to use lowercase with underscores format: `['proposed', 'ready', 'in_progress', 'completed', 'abandoned']`

3. **Documentation Enhancement**
   - [x] Update module docstring to explain that the script accepts status values in multiple formats
   - [x] Document the normalization behavior (lowercase with underscores, spaces/hyphens converted)
   - [x] Provide examples of accepted formats

4. **Metadata Extraction Improvements**
   - [x] Apply `normalize_status()` when extracting status from YAML frontmatter
   - [x] Handle both 'updated' and 'last_updated' field names in frontmatter parsing
   - [x] Rename `frontmatter` variable to `front_matter` for consistency

5. **Index Generation Updates**
   - [x] Use normalized status values throughout the `generate_index_content()` function
   - [x] Apply normalization when checking task status validity
   - [x] Update status references in completed/abandoned task sections
   - [x] Improve sort key function to handle empty strings properly (`return task.get('updated', '') or ''`)

6. **Backward Compatibility**
   - [x] Ensure existing task files with current status formats continue to work
   - [x] Maintain existing index.md output format with proper status display

## Implementation Notes

### Key Changes Required

1. **Add normalize_status function**:
   ```python
   def normalize_status(status):
       """Normalize status to lowercase with underscores."""
       if not status:
           return None
       # Convert to lowercase and replace spaces with underscores
       return status.lower().replace(' ', '_').replace('-', '_')
   ```

2. **Update STATUSES constant**:
   ```python
   STATUSES = ['proposed', 'ready', 'in_progress', 'completed', 'abandoned']
   ```

3. **Apply normalization in metadata extraction**:
   - Use `normalize_status(front_matter.get('status', None))`
   - Handle both 'updated' and 'last_updated' fields

4. **Update index generation logic**:
   - Use `normalize_status(task['status'])` when categorizing
   - Update status references throughout

## Testing Requirements

1. **Test with multiple status formats**:
   - "Proposed", "In Progress", "Completed" (current format)
   - "proposed", "in_progress", "completed" (new format)
   - "Ready", "abandoned" (mixed case)

2. **Verify backward compatibility**:
   - Existing task files should continue to be processed correctly
   - Index output should remain consistent

3. **Edge case handling**:
   - Empty status values
   - Invalid status values
   - Missing status fields

## Files to Modify

- `backlog/update_index.py` - Main implementation

## Dependencies

- No new dependencies required
- Existing: PyYAML, pathlib, re, os

## Estimated Effort

**1 day** - This is a focused enhancement to an existing script with clear requirements.

## Progress Updates

### 2025-07-26
- Task created with Proposed status
- All acceptance criteria implemented and verified
- Status changed to Completed
- Implementation tested successfully with 19 backlog tasks

## Related Items

- **Follow-up**: `2025-07-26_whats-next-status-normalization` (apply same improvements to whats_next.py)
- None currently identified 