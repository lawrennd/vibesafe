---
id: "2026-01-08_cip0013-phase5-periodic-review"
title: "CIP-0013 Phase 5: Establish Periodic Compression Review Process"
status: "Completed"
priority: "Low"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: "Neil Lawrence"
dependencies: ["2026-01-08_cip0013-phase2-whats-next-integration"]
tags: ["documentation", "compression", "workflow", "maintenance"]
---

# Task: CIP-0013 Phase 5: Establish Periodic Compression Review Process

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 5 of CIP-0013 (Documentation Compression Stage).

## Description

Establish a periodic review process (quarterly) to ensure compression isn't falling behind. This catches any CIPs that slipped through the cracks and provides a forcing function for batch compression.

**Why this matters**: While `whats-next` prompts help, periodic reviews ensure nothing is forgotten. Quarterly rhythm provides natural checkpoints for documentation maintenance.

## Acceptance Criteria

- [x] Define quarterly compression review process in documentation
- [x] Create template for quarterly compression review:
  - [x] Run `whats-next --compression-check`
  - [x] Review list of uncompressed closed CIPs
  - [x] Prioritize: which CIPs are critical to document?
  - [x] Batch compress high-value CIPs
  - [x] Update compression quality metrics
- [x] Create recurring backlog task template: `YYYY-QX_quarterly-compression-review.md`
- [x] Establish compression quality metrics:
  - [x] % of closed CIPs compressed within 30 days (Target: >80%)
  - [x] % of closed CIPs compressed within 90 days (Target: >95%)
  - [x] Total uncompressed closed CIPs (Target: <5)
  - [x] Oldest uncompressed CIP age (Target: <120 days)
- [x] Document the review process (integrated into CIP-0013 per REQ-000D)
- [ ] Add calendar reminder mechanism (optional, deferred - out of scope)

## Implementation Notes

**Quarterly Review Workflow**:
```bash
# Step 1: Check compression status
./whats-next --compression-check

# Step 2: Review output
# Output: "15 closed CIPs need compression"
# Prioritize: Which are critical? Which can wait?

# Step 3: Batch compress
# Work through list, using compression checklist
# Focus on high-value CIPs first

# Step 4: Update metrics
# Track: How many compressed this quarter?
# Calculate: % compliance with 30-day target

# Step 5: Reflect
# What went well? What slipped through?
# Adjust workflow if needed
```

**Compression Quality Metrics**:
Track these quarterly:
- **30-day compliance**: X% of closed CIPs compressed within 30 days
- **90-day compliance**: X% of closed CIPs compressed within 90 days
- **Backlog size**: X uncompressed closed CIPs
- **Oldest CIP**: CIP-XXXX closed X days ago (still uncompressed)

**When to Skip Compression**:
Not all CIPs need compression. Skip if:
- Internal/minor process changes
- Superseded by later CIPs
- Implementation details captured in code/tests
- Rejected or deferred CIPs

**Quarterly Task Template**:
```markdown
---
id: "YYYY-QX_quarterly-compression-review"
title: "Q[X] YYYY Quarterly Compression Review"
status: "Ready"
priority: "Medium"
...
---

# Task: Quarterly Compression Review (Q[X] YYYY)

## Checklist
- [ ] Run `whats-next --compression-check`
- [ ] Review uncompressed closed CIPs
- [ ] Compress high-priority CIPs
- [ ] Update compression metrics
- [ ] Reflect on workflow effectiveness
```

## Related

- CIP: 0013 (Phase 5)
- Requirement: 000E (Documentation Synchronization)
- Previous Phase: Phase 2 (whats-next Integration)

## Progress Updates

### 2026-01-08 (Initial)
Task created with "Ready" status. Depends on Phase 2 for `--compression-check` functionality. Lowest priority phase.

### 2026-01-08 (Later)
Phase 5 completed! Established periodic compression review process:

**1. Created Quarterly Review Template** (`templates/quarterly_compression_review_template.md`):
- ✅ Complete workflow: Check status → Prioritize → Batch compress → Update metrics → Reflect
- ✅ Compression quality metrics table with targets
- ✅ Guidance on when to skip compression
- ✅ Template for creating next quarter's review task
- ✅ Progress tracking section for metrics

**2. Documented Periodic Review Process** (in CIP-0013):
- ✅ Added "Periodic Compression Review" section to CIP-0013's Compression Guide
- ✅ Explained quarterly review workflow (5 steps)
- ✅ Defined compression quality metrics with targets:
  - 30-day compliance: >80%
  - 90-day compliance: >95%
  - Uncompressed backlog: <5 CIPs
  - Oldest uncompressed: <120 days
- ✅ Documented template usage and first review recommendation (Q2 2026)

**3. Established Metrics Framework**:
- ✅ Four key metrics defined with measurable targets
- ✅ Rationale provided for each metric
- ✅ Quarterly tracking cadence established

**Why Quarterly?**
- Monthly: Too frequent, creates overhead
- Quarterly: Natural checkpoint, manageable workload
- Annual: Too infrequent, allows drift

**Calendar Reminder**: Deferred (optional, out of scope). Users can set their own reminders.

**First Review Recommendation**: Q2 2026 (Apr-Jun) to establish baseline metrics.

All acceptance criteria met. Phase 5 complete!

