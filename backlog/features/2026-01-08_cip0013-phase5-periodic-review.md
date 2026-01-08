---
id: "2026-01-08_cip0013-phase5-periodic-review"
title: "CIP-0013 Phase 5: Establish Periodic Compression Review Process"
status: "Ready"
priority: "Low"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: ""
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

- [ ] Define quarterly compression review process in documentation
- [ ] Create template for quarterly compression review:
  - [ ] Run `whats-next --compression-check`
  - [ ] Review list of uncompressed closed CIPs
  - [ ] Prioritize: which CIPs are critical to document?
  - [ ] Batch compress high-value CIPs
  - [ ] Update compression quality metrics
- [ ] Create recurring backlog task template: `YYYY-QX_quarterly-compression-review.md`
- [ ] Establish compression quality metrics:
  - [ ] % of closed CIPs compressed within 30 days
  - [ ] % of closed CIPs compressed within 90 days
  - [ ] Total uncompressed closed CIPs
  - [ ] Oldest uncompressed CIP age
- [ ] Document the review process in `docs/compression-guide.md`
- [ ] Add calendar reminder mechanism (optional, low priority)

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

### 2026-01-08
Task created with "Ready" status. Depends on Phase 2 for `--compression-check` functionality. Lowest priority phase.

