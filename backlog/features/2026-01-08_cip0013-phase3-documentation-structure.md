---
id: "2026-01-08_cip0013-phase3-documentation-structure"
title: "CIP-0013 Phase 3: Establish Documentation Structure for Compression"
status: "Ready"
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
- [ ] Detect user's existing documentation system:
  - [ ] Check for `docs/conf.py` (Sphinx)
  - [ ] Check for `mkdocs.yml` (MkDocs)
  - [ ] Check for `docs/` directory with markdown files
  - [ ] Check for `README.md` structure
- [ ] Document detection logic in `docs/compression-guide.md`

### Guidance (Provide Defaults, Allow Configuration)
- [ ] Create `docs/compression-guide.md` with:
  - [ ] **Discovery**: How VibeSafe detects your documentation structure
  - [ ] **Defaults**: Sensible compression targets if no structure exists
  - [ ] **Examples**: Compression patterns for Sphinx, MkDocs, plain markdown
  - [ ] **Style guide**: How to write compressed documentation
  - [ ] **Traceability**: How to reference CIPs in your docs
  - [ ] **Configuration**: How to override defaults
- [ ] Provide compression target suggestions based on detected structure:
  - [ ] If Sphinx: Suggest `docs/source/*.rst` files
  - [ ] If MkDocs: Suggest `docs/*.md` files
  - [ ] If plain markdown: Suggest `docs/*.md` or `README.md` sections
  - [ ] If none: Suggest starting with `README.md` + optional `docs/`
- [ ] Examples for multiple documentation systems (not just one)

### Implementation (No Forced Structure)
- [ ] ❌ DO NOT create directories or files without user consent
- [ ] ✅ DO provide templates/examples for different systems
- [ ] ✅ DO adapt compression checklist to detected structure
- [ ] ✅ DO allow user to specify compression targets via config

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

