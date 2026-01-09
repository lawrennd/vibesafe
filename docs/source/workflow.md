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

## Process: Human-AI Collaboration Patterns

**Implemented in:** [CIP-0008](../../cip/cip0008.md) - Unified Philosophy and New Tenets

### Overview

VibeSafe's approach to human-AI collaboration is grounded in research on how humans and AI systems can effectively work together. CIP-0008 formalized this through new tenets and documented patterns.

### New Tenets Created

1. **Shared Information Landmarks**: Creates explicit "information landmarks" (CIPs, tenets, directory structures) that serve as fixed reference points for both humans and AI

2. **Information Exploration Patterns**: Supports different patterns of navigation - from detailed focus on specific improvements to broader conceptual understanding

**Key insight**: Reliable collaboration between humans and AI requires shared reference points and flexible exploration patterns, similar to how human visual attention works.

### The Breadcrumbs Pattern

Through development, an emergent pattern was recognized: leaving explicit traces of thinking through CIPs, tenets, and documentation. This creates a navigable trail that both humans and AI can follow to understand rationale and context.

**Examples**:
- CIPs that document not just WHAT was built, but WHY decisions were made
- Requirements that trace back to tenets (showing WHY this matters)
- Documentation that links to CIPs (showing HOW it was built)

**Impact**: Makes VibeSafe self-documenting and enables effective context restoration for both humans and AI assistants.

**See also:**
- [Shared Information Landmarks tenet](../../tenets/vibesafe/shared-information-landmarks.md)
- [Information Exploration Patterns tenet](../../tenets/vibesafe/information-exploration-patterns.md)
- [CIP-0008 details](../../cip/cip0008.md) - Full rationale and research foundations

---

## Process: AI-Assisted Requirements Gathering

**Implemented in:** [CIP-0009](../../cip/cip0009.md) - Requirements Conversation Framework

### Overview

VibeSafe provides a structured framework for AI-assisted requirements gathering through conversation patterns and stage-specific prompts. Located in `templates/ai-requirements/`, this framework helps teams articulate and refine requirements through guided conversations with AI assistants.

### Four Stages

1. **Discovery**: Initial requirements identification through open conversation
2. **Refinement**: Clarifying and detailing requirements
3. **Validation**: Ensuring requirements are clear, testable, and complete
4. **Testing**: Defining acceptance criteria and test strategies

### Conversation Patterns

**Stakeholder Identification**: Systematically identify who is affected by requirements  
**Goal Decomposition**: Break high-level goals into concrete, actionable requirements

### Integration with VibeSafe

- Requirements link to tenets (WHY) via `related_tenets` field
- CIPs reference requirements (HOW implements WHAT)  
- Backlog tasks reference CIPs (DO executes HOW)
- Status synchronization across all levels

**Key insight**: AI assistants excel at helping humans articulate implicit knowledge through structured conversation, making requirements more explicit and actionable.

**See also:**
- [AI-Requirements Framework](../../templates/ai-requirements/README.md) - Full framework documentation
- [CIP-0009 details](../../cip/cip0009.md) - Implementation history and rationale

---

*Last updated: 2026-01-09*
*This file is part of the VibeSafe formal documentation system.*

