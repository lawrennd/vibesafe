---
id: "2026-01-08_cip0013-phase1-compression-checklist"
title: "CIP-0013 Phase 1: Create Compression Checklist Template"
status: "Ready"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: ""
dependencies: ["2026-01-08_cip0013-phase0-compression-metadata"]
tags: ["documentation", "compression", "workflow", "templates"]
---

# Task: CIP-0013 Phase 1: Create Compression Checklist Template

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 1 of CIP-0013 (Documentation Compression Stage).

## Description

Create a reusable checklist template that guides users through compressing a closed CIP into formal documentation. The template should be adaptable to different types of CIPs (infrastructure, features, process improvements).

**Why this matters**: Compression is a new workflow step. A clear checklist ensures consistency and completeness when transforming detailed CIP content into concise formal docs.

## Acceptance Criteria

- [ ] Create `templates/compression_checklist.md` with standardized compression tasks
- [ ] Checklist includes sections for:
  - [ ] README.md updates (high-level feature description)
  - [ ] Sphinx/docs/ updates (detailed documentation)
  - [ ] Architecture doc updates (design decisions, patterns)
  - [ ] Traceability (ensure docs reference CIP number)
  - [ ] Metadata update (set `compressed: true` in CIP)
- [ ] Provide 3 example checklists:
  - [ ] Infrastructure CIP example (e.g., CIP-0012 platform independence)
  - [ ] Feature CIP example (e.g., adding new VibeSafe component)
  - [ ] Process CIP example (e.g., CIP-0013 compression stage itself)
- [ ] Document checklist usage in `templates/compression_checklist.md` header
- [ ] Include guidance: "What to extract vs. what to leave in CIP history"

## Implementation Notes

**Checklist Structure**:
```markdown
# Compression Checklist: CIP-XXXX [Title]

## Pre-Compression Review
- [ ] Read closed CIP completely
- [ ] Identify key decisions and outcomes
- [ ] Note which tenets/requirements are relevant

## Documentation Updates
- [ ] Update README.md: [describe what section]
- [ ] Update docs/architecture.md: [describe what]
- [ ] Update Sphinx API docs: [if applicable]
- [ ] Add code examples/tutorials: [if applicable]

## Traceability
- [ ] Formal docs reference CIP number (e.g., "Multi-platform support (CIP-0012)")
- [ ] Link from formal docs → CIP for detailed rationale

## Finalization
- [ ] Set CIP `compressed: true` in YAML frontmatter
- [ ] Commit with message: "Compress CIP-XXXX into formal documentation"
- [ ] Verify links work, docs are accurate
```

**Different CIP Types Need Different Approaches**:
- **Infrastructure**: Focus on architecture diagrams, system design
- **Features**: Focus on user-facing documentation, API examples
- **Process**: Focus on workflow documentation, tool usage

## Related

- CIP: 0013 (Phase 1)
- Requirement: 000E (Documentation Synchronization)
- Previous Phase: Phase 0 (Compression Metadata)
- Next Phase: Phase 2 (whats-next Integration)

## Progress Updates

### 2026-01-08
Task created with "Ready" status. Depends on Phase 0 completion.

