# VibeSafe Development Workflow

This document describes VibeSafe's development processes and how different components work together.

## Process: Tenet Creation and Evolution

**Implemented in:** [CIP-0007](../../cip/cip0007.md) - Documentation and Implementation as a Unified Whole

### Overview

VibeSafe tenets can evolve over time as we learn from practice. The process for creating or evolving a tenet involves:

1. **Identification**: Recognize a pattern that emerges from development
2. **Proposal**: Create a CIP to propose the new or evolved tenet
3. **Implementation**: Create the tenet file in `tenets/vibesafe/`
4. **Integration**: Update related documentation to reference the tenet

### Example: Documentation and Implementation as Unified Whole

Originally, VibeSafe had separate tenets for "documentation-first" and "self-documentation". Through CIP-0007, these were unified into a single, more comprehensive tenet: **"Documentation and Implementation as a Unified Whole"**.

**Key insight**: Documentation and implementation are not separate concerns but interdependent parts of a unified system. Documentation guides implementation; implementation validates documentation.

**Quote**: *"Document to guide implementation; implement to validate documentation."*

This tenet now informs how we approach all VibeSafe development:
- CIPs define expected behaviors before implementation
- Code uses self-explanatory naming and structure
- Tests validate documented behaviors
- When documentation changes, implementation follows (and vice versa)

**See also:**
- [Tenet file](../../tenets/vibesafe/documentation-implementation-unified.md)
- [CIP-0007 details](../../cip/cip0007.md) - Full rationale and implementation history

---

## Process: Documentation Compression

**Implemented in:** [CIP-0013](../../cip/cip0013.md) - Documentation Compression Stage

### Overview

After CIPs are closed (implementation complete and verified), their key decisions should be compressed into formal documentation. This prevents users from needing to read 50+ closed CIPs to understand current architecture.

**Workflow**: WHY → WHAT → HOW → DO → **DOCUMENT**

The DOCUMENT stage extracts:
- **WHAT** was built
- Essential **WHY** (rationale)
- Architecture patterns
- Usage examples

### Compression Process

1. CIP closes (status: Closed, compressed: false)
2. Review CIP for key decisions
3. Extract essential information
4. Update formal documentation:
   - Infrastructure CIPs → `docs/source/architecture.md`
   - Feature CIPs → `docs/source/features.md`
   - Process CIPs → `docs/source/workflow.md` (this file)
5. Add traceability link to CIP
6. Set `compressed: true` in CIP frontmatter

### When to Compress

- After CIP is closed and validated
- During batch compression (3+ CIPs closed within 7 days)
- Run `./whats-next --compression-check` to see candidates

**See also:**
- [Compression Guide](compression-guide.md) - Detailed compression workflow
- [CIP-0013 details](../../cip/cip0013.md) - Full compression system design
- [REQ-000E](../../requirements/req000E_documentation-synchronization.md) - Documentation synchronization requirement

---

*Last updated: 2026-01-09*
*This file is part of the VibeSafe formal documentation system.*

