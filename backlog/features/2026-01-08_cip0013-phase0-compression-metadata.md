---
id: "2026-01-08_cip0013-phase0-compression-metadata"
title: "CIP-0013 Phase 0: Add Compression Metadata to CIP Format"
status: "Completed"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: "Neil Lawrence"
dependencies: []
tags: ["documentation", "compression", "workflow", "metadata"]
---

# Task: CIP-0013 Phase 0: Add Compression Metadata to CIP Format

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 0 of CIP-0013 (Documentation Compression Stage).

## Description

Add `compressed` metadata field to the CIP YAML frontmatter format. This field tracks whether a closed CIP's key decisions have been compressed into formal documentation.

**Why this matters**: Without metadata tracking, we can't programmatically detect which closed CIPs need compression. This field enables `whats-next` to generate compression prompts (REQ-000E triggers).

**Scope**: Update CIP template and document the new field's usage.

## Acceptance Criteria

- [x] Add `compressed: false` field to `templates/cip/cip_template.md` YAML frontmatter ✅
- [x] Add comment explaining field purpose: `# Set to true after compressing CIP into formal docs (README, Sphinx)` ✅
- [x] Document `compressed` field in CIP template description section ✅
- [x] Update CIP README.md to explain compression metadata ✅
- [x] Provide example: Show a closed CIP with `compressed: true` (CIP-0012) ✅

## Implementation Notes

**YAML Frontmatter Addition**:
```yaml
compressed: false  # Set to true after compressing into formal documentation
```

**Field Semantics**:
- **Default**: `false` (or omitted, which means false)
- **Set to `true`**: After CIP's key decisions are reflected in formal docs (README, Sphinx, architecture.md)
- **Applies to**: Closed CIPs only (Proposed/Accepted/In Progress CIPs don't need compression yet)

**Backward Compatibility**:
- Existing CIPs without `compressed` field are treated as `compressed: false`
- No need to update all existing CIPs immediately
- Gradually add field as CIPs are compressed

## Related

- CIP: 0013 (Phase 0)
- Requirement: 000E (Documentation Synchronization)
- Next Phase: Phase 1 (Compression Checklist Template)

## Progress Updates

### 2026-01-08
Task created with "Ready" status. CIP-0013 accepted, ready to implement Phase 0.

### 2026-01-08 (Later)
Phase 0 completed! All acceptance criteria met:
- Added `compressed: false` field to `templates/cip/cip_template.md`
- Added inline comment explaining purpose
- Documented field in template with link to REQ-000E and CIP-0013
- Updated `cip/README.md` with comprehensive compression documentation
- Provided example: CIP-0012 marked with `compressed: true`

Next phase: Phase 1 (Compression Checklist Template)

