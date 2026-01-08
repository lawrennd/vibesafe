---
id: "YYYY-QX_quarterly-compression-review"
title: "QX YYYY Quarterly Compression Review"
status: "Ready"
priority: "Medium"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
category: "documentation"
related_cips: ["0013"]
owner: ""
dependencies: []
tags: ["compression", "documentation", "maintenance", "periodic-review"]
---

# Task: Quarterly Compression Review (QX YYYY)

> **Note**: This is a recurring task to ensure documentation compression stays current.  
> Run this quarterly (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec).

## Description

Periodic review of closed CIPs to ensure documentation compression isn't falling behind. This catches any CIPs that slipped through immediate compression and provides a forcing function for batch compression.

**Why quarterly?** Balances thoroughness with overhead. Monthly is too frequent; annual allows too much drift.

## Acceptance Criteria

- [ ] Run `./whats-next --compression-check` and review output
- [ ] Identify high-value uncompressed closed CIPs
- [ ] Batch compress critical CIPs (use `templates/compression_checklist.md`)
- [ ] Update compression quality metrics (see below)
- [ ] Reflect on workflow effectiveness and adjust if needed
- [ ] Create next quarter's review task

## Quarterly Review Workflow

### Step 1: Check Compression Status

```bash
./whats-next --compression-check
```

**Output example**:
```
Compression Candidates: 15 closed CIPs
  - CIP-0042: Closed 95 days ago (High priority)
  - CIP-0038: Closed 67 days ago (Medium priority)
  - CIP-0031: Closed 45 days ago (Low priority)
  ...
```

### Step 2: Prioritize

**High-value CIPs** (compress first):
- Architecture changes
- Major features
- User-facing changes
- Process improvements

**Can defer** (or skip):
- Internal/minor changes
- Superseded by later CIPs
- Details fully captured in code/tests
- Rejected or deferred CIPs

### Step 3: Batch Compress

For each high-priority CIP:
1. Copy compression checklist: `cp templates/compression_checklist.md cip/cipXXXX-compression.md`
2. Read closed CIP
3. Extract key decisions, rationale, outcomes
4. Update formal documentation (README, Sphinx, etc.)
5. Mark CIP as compressed: `compressed: true`
6. Commit: `git commit -m "Compress CIP-XXXX"`

**Batch efficiency**: Compress similar CIPs together (e.g., all infrastructure CIPs at once).

### Step 4: Update Metrics

Calculate and document:
- **30-day compliance**: X% of closed CIPs compressed within 30 days
- **90-day compliance**: X% of closed CIPs compressed within 90 days
- **Current backlog**: X uncompressed closed CIPs remaining
- **Oldest CIP**: CIP-XXXX closed X days ago (still uncompressed)

### Step 5: Reflect

Questions to consider:
- What went well this quarter?
- Which CIPs slipped through immediate compression, and why?
- Should we adjust the workflow?
- Are the metrics meaningful?
- Is compression burden manageable?

## Compression Quality Metrics

Track these quarterly in this task's "Progress Updates" section:

| Metric | This Quarter | Target |
|--------|--------------|--------|
| 30-day compliance | __%  | >80% |
| 90-day compliance | __%  | >95% |
| Uncompressed backlog | __ CIPs | <5 |
| Oldest uncompressed | __ days | <120 days |

## When to Skip Compression

Not all closed CIPs need formal documentation compression. Skip if:
- Internal process changes with no external impact
- CIP was superseded by a later CIP (compress the newer one)
- Implementation details are fully captured in code/tests
- CIP was rejected or deferred (mark `compressed: true` to remove from list)

## Creating Next Quarter's Review Task

At the end of this review:
1. Copy this template: `cp templates/quarterly_compression_review_template.md backlog/documentation/[NEXT-YYYY-QX]_quarterly-compression-review.md`
2. Update dates and quarter number
3. Set status to "Ready"

## Related

- CIP: 0013 (Documentation Compression Stage)
- Requirement: 000E (Documentation Synchronization)
- Template: `templates/compression_checklist.md`

## Progress Updates

### [Date]
Review started.

### [Date]
Metrics:
- 30-day compliance: __% (Target: >80%)
- 90-day compliance: __% (Target: >95%)
- Uncompressed backlog: __ CIPs (Target: <5)
- Oldest uncompressed: CIP-____ (__ days old)

### [Date]
Compressed CIPs: [List CIP numbers]

### [Date]
Review completed. Next quarter's task created.

Reflections:
- [What went well?]
- [What should we adjust?]

