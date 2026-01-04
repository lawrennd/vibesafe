---
id: "000D"
title: "CIPs as Self-Contained Design Documents"
status: "Proposed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
related_tenets: ["documentation-implementation-unified", "simplicity-of-use"]
stakeholders: ["developers", "ai-assistants"]
tags: ["documentation", "cips", "design", "architecture"]
---

# REQ-000D: CIPs as Self-Contained Design Documents

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.
>
> ✅ Good: "CIPs contain all design rationale needed to understand and implement them"
> ❌ Bad: "Add a 'Detailed Description' section to CIP template" (that's HOW)

## Description

Code Improvement Plans (CIPs) should be self-contained documents that include all design rationale, architectural decisions, and implementation plans within the CIP file itself. AI assistants and developers should not need to create or consult separate design documents, architecture documents, or planning documents to understand a CIP.

When design complexity requires extensive exploration, supplementary materials (research notes, alternative approaches) may be placed in a CIP-specific subdirectory (e.g., `cip/cip0012/`), but the core design decisions and rationale **must be in the CIP itself**.

**Why this matters**: This requirement directly supports the "Documentation and Implementation as a Unified Whole" tenet by preventing the creation of separate design documents that can drift out of sync with the actual CIP. It also aligns with "Simplicity at All Levels" by maintaining a single authoritative source for each improvement plan.

**Who benefits**:
- **Developers**: Single source of truth for understanding a CIP
- **AI Assistants**: Clear guidance to enhance CIPs rather than create separate docs
- **Reviewers**: All design context in one place for easier review
- **Future maintainers**: Historical design rationale preserved with the CIP

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] AI assistants consistently enhance CIPs rather than creating separate design documents
- [ ] CIP files contain sufficient design detail to understand motivation and approach
- [ ] Supplementary materials (if needed) are organized in CIP-specific subdirectories, not as standalone docs
- [ ] No standalone files like `DESIGN.md`, `ARCHITECTURE.md`, or `cip0012-strategy.md` exist for design content
- [ ] CIP template structure supports comprehensive design documentation
- [ ] Documentation clearly guides AI assistants to integrate design into CIPs
- [ ] Existing separate design documents are integrated back into their respective CIPs

## Notes (Optional)

**Current State**: VibeSafe has experienced the exact anti-pattern this requirement addresses:
- `cip/cip0012-prompt-composition-strategy.md` was created as a separate design doc
- Content should have been in the "Detailed Description" section of `cip0012.md`
- This violated the "Documentation and Implementation as a Unified Whole" tenet

**Constraints**:
- Some CIPs may need supplementary research materials
- Solution: Use `cip/cipXXXX/` subdirectories for supporting docs, but keep core design in the CIP

**Trade-offs**:
- CIP files may become longer (more content)
- Benefit: Single source of truth, no synchronization issues

**For AI Assistants**:
When you feel the urge to create a separate design document:
1. **STOP** - Check if this content belongs in an existing CIP
2. **Enhance the CIP** - Add a "Detailed Description" section or expand it
3. **Only if necessary** - Create supplementary materials in `cip/cipXXXX/` subdirectory

## References

- **Related Tenets**:
  - [Documentation and Implementation as a Unified Whole](tenets/vibesafe/documentation-implementation-unified.md)
  - [Simplicity at All Levels](tenets/vibesafe/simplicity-of-use.md)
- **Example Issue**:
  - `cip/cip0012-prompt-composition-strategy.md` (should be integrated into `cip0012.md`)

## Progress Updates

### 2026-01-04
Requirement created after observing AI assistant tendency to create separate design documents (like `cip0012-prompt-composition-strategy.md`) instead of enhancing CIPs directly. This violates VibeSafe's "Documentation and Implementation as a Unified Whole" tenet. Status: Proposed, needs review and refinement before moving to Ready.

