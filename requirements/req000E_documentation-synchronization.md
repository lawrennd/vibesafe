---
id: "000E"
title: "Documentation Synchronization with Implementation"
status: "Ready"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
related_tenets: ["documentation-as-code", "user-autonomy"]  # Documentation as Unified Whole + User Autonomy
stakeholders: ["users", "ai-assistants", "maintainers", "contributors"]
tags: ["documentation", "knowledge-management", "compression", "workflow"]
---

# REQ-000E: Documentation Synchronization with Implementation

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.
> 
> ✅ Good: "Formal documentation reflects all closed CIPs"  
> ❌ Bad: "Create compression script to update docs" (that's HOW/DO)

## Description

Formal documentation should accurately reflect all finalized implementation decisions captured in closed CIPs and validated requirements. Users and AI assistants should be able to understand the current state of the system by reading formal documentation without needing to trace through the complete development history of dozens of CIPs and backlog tasks.

This requirement addresses the "documentation drift" problem where:
- CIPs close with valuable architectural decisions
- Formal documentation (README, Sphinx, architecture guides) never gets updated
- New users must read 50+ closed CIPs to understand current architecture
- AI assistants lack compressed context about finalized decisions
- Implementation and documentation diverge over time

**Why this matters**: 

This requirement stems from two tenets:

1. **"Documentation and Implementation as a Unified Whole"**: *"Document to guide implementation; implement to validate documentation."* The compression stage closes the feedback loop by validating that implementation matches design intent and capturing that validated knowledge in permanent, accessible documentation.

2. **"User Autonomy Over Prescription"**: *"We optimize for configurability over our own preferences."* The acceptance criteria serve as prompts/suggestions via `whats-next`, not blocking requirements. Users choose when and how to compress documentation based on their judgment and workflow.

**Who benefits**: 

- **Users**: Find answers in docs without reading CIP history
- **AI Assistants**: Get compressed context about finalized architecture
- **Contributors**: Understand current state quickly before making changes
- **Maintainers**: Have single source of truth for current architecture
- **Future Teams**: Inherit clear documentation of why and how systems were built

## Acceptance Criteria

What does "done" look like? These criteria serve as **triggers for `whats-next` prompts**, not blocking gates. Per the "User Autonomy" tenet, VibeSafe guides but doesn't prescribe.

**Measurability**: Each criterion should be detectable by `whats-next` and turned into an actionable prompt. For example: "3 closed CIPs need documentation compression (CIP-0012, CIP-0013, CIP-0014)".

- [ ] **Prompt Trigger 1**: When a CIP is closed without `compressed: true` metadata, `whats-next` suggests compression within 30 days
- [ ] **Prompt Trigger 2**: When formal documentation hasn't been updated in X days, `whats-next` suggests reviewing closed CIPs for compression candidates
- [ ] **Prompt Trigger 3**: When a CIP is marked `compressed: true`, formal docs reference that CIP number (e.g., "Multi-platform support (CIP-0012)")
- [ ] **Prompt Trigger 4**: When a requirement status changes to "Validated", `whats-next` suggests documenting its outcomes in formal docs
- [ ] **Prompt Trigger 5**: `whats-next` can list closed CIPs that lack `compressed: true` metadata (visible compression backlog)
- [ ] **Prompt Trigger 6**: `whats-next --compression-check` shows priority-ordered list of compression candidates
- [ ] **Prompt Trigger 7**: When multiple CIPs close in short timeframe, `whats-next` suggests batch compression task
- [ ] **Prompt Trigger 8**: When compression task is created, it includes checklist: update README, update Sphinx, add traceability, mark CIP compressed

**Note**: These triggers guide workflow but don't block progress. Users can close CIPs without immediate compression. The prompts ensure compression doesn't get forgotten.

## Notes (Optional)

### Scope of "Formal Documentation"

**User Autonomy**: This requirement applies to whatever documentation system the user has chosen. VibeSafe detects and adapts to user preferences rather than prescribing structure.

**Common documentation systems** (all supported):
- **README.md** (project root): High-level features, architecture overview
- **Sphinx** (`docs/source/*.rst`): Detailed API docs, tutorials, architecture guides
- **MkDocs** (`docs/*.md`): Detailed API docs, tutorials, architecture guides
- **Plain Markdown** (`docs/*.md`): Architecture docs, design decisions
- **Custom**: User-specified compression targets via configuration

**VibeSafe adapts to**:
- Your existing directory structure
- Your chosen documentation format (markdown, reStructuredText, etc.)
- Your documentation system (Sphinx, MkDocs, Hugo, etc.)
- Your file naming conventions

Does NOT apply to:
- CIPs themselves (they remain as historical record, unchanged)
- Backlog tasks (temporary, deleted/archived after completion)
- Code comments (covered by "self-documenting code" practice)

### Compression vs. Duplication

This is NOT about copying CIP content verbatim into formal docs. Instead:
- **Extract essence**: Distill 15-page CIP into 2-paragraph architecture doc entry
- **Focus on outcomes**: Document WHAT was built and WHY, not detailed HOW
- **Provide context**: Link formal docs → CIPs for readers who want detailed rationale
- **Maintain traceability**: Formal docs reference CIP numbers (e.g., "Multi-platform support (CIP-0012)...")

### Compression is a Loop Closure

The full VibeSafe workflow:
```
WHY (Tenets)
  ↓ informs
WHAT (Requirements) 
  ↓ guides
HOW (CIPs)
  ↓ breaks into
DO (Backlog)
  ↓ produces
IMPLEMENTATION (Code)
  ↓ validates & compresses into
DOCUMENT (Formal Docs)
  ↓ feedback: validates alignment with
WHY (Tenets) ← loop closes
```

Compression validates the loop: Does the formal documentation align with our tenets? If not, we've drifted.

### Implementation Note: whats-next Integration

The `whats-next` script must implement detection for these prompt triggers. This should be documented as part of CIP-0013 implementation (likely Phase 2: Integration with whats-next). The implementation will:

1. Check for closed CIPs without `compressed: true` metadata
2. Calculate time since CIP closure (trigger 30-day reminders)
3. Detect validated requirements without formal documentation updates
4. Provide `--compression-check` flag for focused compression view
5. Generate prioritized suggestions based on:
   - Age of closed CIP (older = higher priority)
   - Importance of CIP (based on `priority` or `related_requirements`)
   - Number of uncompressed CIPs (batch suggestions for 3+)

**User Autonomy Alignment**: These prompts are suggestions, not blockers. Users can choose to:
- Compress immediately after CIP closure
- Batch compress multiple CIPs together
- Defer compression for lower-priority CIPs
- Skip compression entirely for minor/internal CIPs

The system guides toward best practices but respects user judgment.

## References

- **Related Tenets**: `documentation-as-code` (Documentation and Implementation as a Unified Whole)
- **Related CIPs**: CIP-0013 (defines HOW to achieve this requirement through compression stage)
- **External Links**: VibeSafe General Development Guidelines, Section 7 (Documentation Lifecycle)

## Progress Updates

### 2026-01-08
Requirement created with "Proposed" status.

### 2026-01-08 (Later)
Refined acceptance criteria to be "prompt triggers" for `whats-next` rather than blocking gates. Added User Autonomy tenet. Status changed to "Ready" - fully defined and ready for CIP implementation.

