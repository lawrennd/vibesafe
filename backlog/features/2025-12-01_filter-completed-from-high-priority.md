---
title: "Filter Completed Items from High Priority Display in What's Next"
id: "2025-12-01_filter-completed-from-high-priority"
status: "completed"
priority: "medium"
created: "2025-12-01"
updated: "2025-12-01"
owner: "Neil"
dependencies: []
category: "features"
---

# Task: Filter Completed Items from High Priority Display in What's Next

## Description

The `whats_next.py` script was displaying completed high-priority backlog items in both the summary output and the "next steps" recommendations. This created confusion by suggesting users work on tasks that were already completed.

## Problem

When a high-priority backlog item was marked as completed, it would still appear in:
1. The high priority summary section
2. The "next steps" recommendations

This led to misleading output like:
```
High Priority: 3
  - Implement Feature X (completed)
  - Add Documentation Y (in_progress)
  - Fix Bug Z (ready)

Next Steps:
  - Address high priority backlog item: Implement Feature X
```

## Acceptance Criteria

- [x] Filter completed items from high priority display in summary
- [x] Filter completed items from high priority recommendations in next steps
- [x] Maintain backward compatibility with existing data structures
- [x] Update tests to include 'id' fields for backlog items
- [x] All tests pass

## Implementation Notes

### Changes Made

1. **`generate_next_steps()` function** (line ~543):
   - Added filtering to exclude completed items from high priority recommendations
   - Created `completed_ids` set from backlog status
   - Filter high priority items before selecting top 2 for recommendations

2. **`main()` function** (line ~691):
   - Added filtering for high priority display in summary output
   - Only show active (non-completed) high priority items
   - Maintain accurate count of active high priority items

3. **Test fixes**:
   - Updated test data to include 'id' fields for backlog items
   - Ensured tests validate the filtering behavior

### Code Changes

```python
# Filter out completed items from high priority
completed_ids = {task['id'] for task in backlog_info.get('by_status', {}).get('completed', [])}
high_priority_active = [
    item for item in backlog_info['by_priority']['high']
    if item['id'] not in completed_ids
]
```

## Testing

All tests pass:
```bash
python -m pytest tests/test_whats_next.py -v
# 16 passed in 0.16s
```

## Related Work

- **Script**: `scripts/whats_next.py`
- **Tests**: `tests/test_whats_next.py`
- **Related CIP**: CIP-0002 (Test Coverage Enhancement)

## Impact

### Benefits
- **Accurate Recommendations**: Users only see actionable high-priority items
- **Clearer Status**: Summary accurately reflects active high-priority work
- **Better UX**: No confusion from completed items appearing in recommendations

### Risks
- **Minimal**: Changes are purely filtering logic with no data structure changes
- **Backward Compatible**: Works with existing backlog data

## Progress Updates

### 2025-12-01
- Bug identified in high priority display logic
- Implemented filtering for completed items
- Fixed test data to include required 'id' fields
- All tests passing
- Task completed

