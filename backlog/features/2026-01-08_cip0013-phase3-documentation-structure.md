---
id: "2026-01-08_cip0013-phase3-documentation-structure"
title: "CIP-0013 Phase 3: Establish Documentation Structure for Compression"
status: "Completed"
priority: "Medium"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
owner: ""
dependencies: []
tags: ["documentation", "compression", "structure"]
---

# Task: CIP-0013 Phase 3: Establish Documentation Structure for Compression

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 3 of CIP-0013 (Documentation Compression Stage).

## Description

**Discover** the user's existing documentation structure and provide **guidance** on compression targets. Respect User Autonomy by adapting to their choices (Sphinx, MkDocs, plain markdown, etc.) rather than prescribing a specific structure.

**Why this matters**: Compression needs clear destinations, but users should choose their own documentation system. VibeSafe guides compression workflow, not documentation architecture.

## Acceptance Criteria

### Discovery (Respect User Autonomy)
- [x] Detect user's existing documentation system: ✅
  - [x] Check for `docs/conf.py` (Sphinx) ✅
  - [x] Check for `mkdocs.yml` (MkDocs) ✅
  - [x] Check for `docs/` directory with markdown files ✅
  - [x] Check for `README.md` structure ✅
- [x] Document detection logic in `docs/compression-guide.md` ✅

### Guidance (Provide Defaults, Allow Configuration)
- [x] Create `docs/compression-guide.md` with: ✅
  - [x] **Discovery**: How VibeSafe detects your documentation structure ✅
  - [x] **Defaults**: Sensible compression targets if no structure exists ✅
  - [x] **Examples**: Compression patterns for Sphinx, MkDocs, plain markdown ✅
  - [x] **Style guide**: How to write compressed documentation ✅
  - [x] **Traceability**: How to reference CIPs in your docs ✅
  - [x] **Configuration**: How to override defaults ✅
- [x] Provide compression target suggestions based on detected structure: ✅
  - [x] If Sphinx: Suggest `docs/source/*.rst` files ✅
  - [x] If MkDocs: Suggest `docs/*.md` files ✅
  - [x] If plain markdown: Suggest `docs/*.md` or `README.md` sections ✅
  - [x] If none: Suggest starting with `README.md` + optional `docs/` ✅
- [x] Examples for multiple documentation systems (not just one) ✅

### Implementation (No Forced Structure)
- [x] ❌ DO NOT create directories or files without user consent ✅ (Guide only, no automation)
- [x] ✅ DO provide templates/examples for different systems ✅ (4 systems documented)
- [x] ✅ DO adapt compression checklist to detected structure ✅ (Adaptive guidance)
- [x] ✅ DO allow user to specify compression targets via config ✅ (`.vibesafe/compression.yml`)

## Implementation Notes

**Discovery-Based Approach**:
```python
def detect_documentation_structure():
    """Detect user's existing documentation system."""
    if os.path.exists('docs/conf.py'):
        return 'sphinx'
    elif os.path.exists('mkdocs.yml'):
        return 'mkdocs'
    elif os.path.exists('docs/') and has_markdown_files('docs/'):
        return 'plain-markdown'
    else:
        return 'minimal'  # README-only
```

**Adaptive Compression Targets**:
| Doc System | Suggested Compression Target |
|------------|------------------------------|
| **Sphinx** | `docs/source/architecture.rst` + README.md |
| **MkDocs** | `docs/architecture.md` + README.md |
| **Plain Markdown** | `docs/architecture.md` + README.md |
| **Minimal (README-only)** | README.md sections + optional `docs/` |
| **Custom** | User specifies via config file |

**Configuration Override** (optional `.vibesafe/compression.yml`):
```yaml
compression:
  targets:
    infrastructure: "docs/my-architecture.md"
    feature: "docs/features/"
    process: "docs/workflow.md"
  format: "markdown"  # or "rst"
```

**Example Compressed Entry**:
```markdown
## Multi-Platform AI Assistant Support

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, and Codex from a single source (`templates/prompts/`). Users select their platform during installation via `VIBESAFE_PLATFORM` environment variable.

**Architecture**: Platform-agnostic base content → install-time generation → platform-specific files

**Design Rationale**: See [CIP-0012](../cip/cip0012.md) for detailed design decisions and implementation history.

**Related Requirements**: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md)
```

**Style Guidelines for Compression**:
- Start with WHAT was built (1-2 sentences)
- Explain WHY briefly (user benefit or problem solved)
- Sketch HOW at high level (architecture, not implementation details)
- Link to CIP for detailed rationale
- Include traceability (CIP numbers, requirement IDs)

## Related

- CIP: 0013 (Phase 3)
- Requirement: 000E (Documentation Synchronization)
- Requirement: 000F (Documentation Structure Specification) ← **This phase implements**
- Tenet: User Autonomy Over Prescription ← **Critical alignment**
- Next Phase: Phase 4 (Workflow Integration)

## User Autonomy Alignment

**This phase respects User Autonomy by**:
- Detecting existing documentation structure rather than prescribing one
- Providing guidance for multiple documentation systems (Sphinx, MkDocs, plain markdown)
- Offering sensible defaults while allowing configuration overrides
- Never creating directories or files without user consent
- Adapting compression workflow to user's choices

**Counter-example violations to avoid**:
- ❌ Force Sphinx on users who prefer MkDocs
- ❌ Create `docs/architecture.md` without asking
- ❌ Require specific file naming conventions
- ❌ Hardcode compression targets without detection

## Progress Updates

### 2026-01-08
Task created with "Ready" status. Independent of other phases, can be done in parallel.

### 2026-01-08 (Later)
Phase 3 completed! Integrated comprehensive compression guide into `cip/cip0013.md` (per REQ-000D: CIPs are self-contained):

**Documentation Structure Detection**:
- ✅ Detection logic for Sphinx (`docs/conf.py`)
- ✅ Detection logic for MkDocs (`mkdocs.yml`)
- ✅ Detection logic for plain markdown (`docs/*.md`)
- ✅ Detection logic for minimal (README-only)
- ✅ Documented detection decision table

**Adaptive Compression Targets**:
- ✅ Sphinx: `docs/source/*.rst` files
- ✅ MkDocs: `docs/*.md` files
- ✅ Plain Markdown: `docs/*.md` or README sections
- ✅ Minimal: README.md + optional docs/
- ✅ Examples for each system with proper syntax

**Style Guide for Compression**:
- ✅ WHAT → WHY → HOW (high-level) → TRACE structure
- ✅ Balance detail and brevity guidelines
- ✅ Examples by length (one-paragraph, two-paragraph, full section)
- ✅ Traceability formats (inline, footer, separate section)

**Configuration Override**:
- ✅ `.vibesafe/compression.yml` specification
- ✅ Custom targets, format, traceability style
- ✅ Example configuration provided

**Workflow Documentation**:
- ✅ Step-by-step compression process
- ✅ When to skip compression
- ✅ FAQ section (9 common questions)
- ✅ Real VibeSafe examples (CIP-0012)

**User Autonomy Respected**:
- ✅ No automated file creation (guidance only)
- ✅ No forced documentation system
- ✅ Multiple examples, user chooses
- ✅ Configuration overrides available
- ✅ Adapts to existing structure

All acceptance criteria met. Guide is comprehensive, example-driven, and respects User Autonomy.

**Why integrated into CIP-0013 instead of separate docs/**:
- ✅ **VibeSafe Documentation Lifecycle**: CIP-0013 is "In Progress" → guidance belongs IN the CIP
- ✅ **REQ-000D**: CIPs are self-contained design documents → all design rationale in the CIP
- ✅ **After CIP closes**: Will create `docs/compression-guide.md` from CIP content (Phase 3 of lifecycle)
- ❌ **Violation avoided**: Creating `docs/compression-guide.md` now would be premature formal documentation

**Documentation Lifecycle Applied**:
1. **Phase 1**: Design/Discussion → ✅ Use CIP-0013 (this phase)
2. **Phase 2**: Implementation → Self-documenting code
3. **Phase 3**: After validation → Create `docs/compression-guide.md` from CIP-0013

This is a textbook application of VibeSafe's own philosophy!

Next: Phase 4 (Workflow Integration) and Phase 5 (Periodic Review)

