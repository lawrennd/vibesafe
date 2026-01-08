# Documentation Compression Guide

> **Purpose**: This guide helps you compress closed CIPs into formal documentation while respecting your chosen documentation system.

## Overview

After implementing a CIP, you should compress its key decisions and outcomes into formal documentation. This guide shows you **HOW** to compress effectively, adapting to **YOUR** documentation system.

**What is compression?**
- **Extract**: WHAT was built, WHY it matters, essential HOW
- **Distill**: From 15-page CIP → 2-paragraph summary + reference
- **Document**: In your chosen documentation system
- **Trace**: Link formal docs back to CIP for detailed rationale

---

## Quick Start

### 1. Check Current CIPs Needing Compression

```bash
./whats-next --compression-check
```

Shows all closed CIPs without `compressed: true` metadata, sorted by priority and age.

### 2. Use the Compression Checklist Template

```bash
cp templates/compression_checklist.md cip/cip0012-compression.md
```

The template guides you through the compression process with examples for different CIP types.

### 3. Compress into Your Documentation System

See "Adaptive Compression Targets" below for guidance on where to compress based on your system.

### 4. Mark CIP as Compressed

```yaml
# In cip/cip0012.md YAML frontmatter:
compressed: true
```

---

## Documentation Structure Detection

VibeSafe **detects** your existing documentation structure and adapts guidance accordingly. We never force a specific system on you.

### How VibeSafe Detects Your System

| Check | Detection | Result |
|-------|-----------|--------|
| `docs/conf.py` exists? | **Sphinx** detected | Suggest `.rst` files in `docs/source/` |
| `mkdocs.yml` exists? | **MkDocs** detected | Suggest `.md` files in `docs/` |
| `docs/*.md` exist? | **Plain Markdown** detected | Suggest `docs/` structure |
| None of above? | **Minimal** detected | Suggest `README.md` + optional `docs/` |

### What VibeSafe Does NOT Do

❌ **We never**:
- Create documentation directories without your consent
- Force you to use Sphinx/MkDocs/etc.
- Require specific file naming conventions
- Prescribe documentation structure

✅ **We do**:
- Detect your existing system
- Provide guidance for your chosen system
- Offer sensible defaults
- Allow configuration overrides

---

## Adaptive Compression Targets

### For Sphinx Users

**Detected**: `docs/conf.py` exists

**Suggested compression targets**:
- **Infrastructure CIPs** → `docs/source/architecture.rst`
- **Feature CIPs** → `docs/source/features.rst` or feature-specific files
- **Process CIPs** → `docs/source/workflow.rst`
- **High-level summary** → `README.md`

**Example** (`docs/source/architecture.rst`):
```rst
Multi-Platform AI Assistant Support
====================================

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, 
and Codex from a single source (``templates/prompts/``). Users select their platform 
during installation via the ``VIBESAFE_PLATFORM`` environment variable.

Architecture
------------

**Design**: Platform-agnostic base content → install-time generation → platform-specific files

**Rationale**: See :doc:`CIP-0012 <../cip/cip0012>` for detailed design decisions and 
implementation history.

**Related**: :doc:`REQ-000C <../requirements/req000C_ai-assistant-framework-independence>`
```

---

### For MkDocs Users

**Detected**: `mkdocs.yml` exists

**Suggested compression targets**:
- **Infrastructure CIPs** → `docs/architecture.md`
- **Feature CIPs** → `docs/features.md` or `docs/features/feature-name.md`
- **Process CIPs** → `docs/workflow.md`
- **High-level summary** → `README.md`

**Example** (`docs/architecture.md`):
```markdown
# Architecture

## Multi-Platform AI Assistant Support

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, and Codex 
from a single source (`templates/prompts/`). Users select their platform during installation 
via the `VIBESAFE_PLATFORM` environment variable.

**Architecture**: Platform-agnostic base content → install-time generation → platform-specific files

**Rationale**: See [CIP-0012](../cip/cip0012.md) for detailed design decisions and 
implementation history.

**Related**: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md)
```

---

### For Plain Markdown Users

**Detected**: `docs/` directory with `.md` files, but no `mkdocs.yml`

**Suggested compression targets**:
- **Infrastructure CIPs** → `docs/architecture.md`
- **Feature CIPs** → `docs/features.md`
- **Process CIPs** → `docs/workflow.md`
- **High-level summary** → `README.md`

**Same format as MkDocs**, but you're managing the structure manually.

---

### For Minimal Documentation Users

**Detected**: No `docs/` directory or documentation system

**Suggested compression targets**:
- **Start with** → `README.md` sections
- **When it grows** → Create `docs/` directory

**Example** (`README.md`):
```markdown
# MyProject

Brief project description.

## Features

### Multi-Platform AI Assistant Support

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, and Codex 
from a single source. Select your platform during installation.

**Details**: See [CIP-0012](cip/cip0012.md) for architecture and design decisions.

## Architecture

See [CIP-0012](cip/cip0012.md) for multi-platform prompt generation architecture.

## Requirements

See [requirements/](requirements/) directory for full requirements specification.
```

---

## Style Guide for Compression

### Structure Your Compressed Content

**Good compressed documentation follows this pattern**:

1. **WHAT**: What was built (1-2 sentences)
2. **WHY**: Why it matters (user benefit or problem solved)
3. **HOW** (high-level): Architecture or design pattern (not implementation details)
4. **TRACE**: Link to CIP for detailed rationale
5. **RELATE**: Link to related requirements/tenets

### Balance Detail and Brevity

**Too brief**: "Added search" ❌
- Users don't understand the capability

**Too detailed**: "Implemented BM25 algorithm with tf-idf weighting and cosine similarity scoring across a distributed index with sharding..." ❌
- Implementation details belong in CIP, not compressed docs

**Just right**: "Full-text search with semantic indexing and relevance ranking. See [CIP-00XX](../cip/cip00XX.md) for algorithm selection rationale." ✅
- User benefit clear, architecture abstracted, detailed rationale referenced

### Examples by Length

**One-paragraph** (for README.md):
```markdown
## Multi-Platform AI Assistant Support

VibeSafe works with Cursor, GitHub Copilot, Claude Code, and Codex. Install-time 
generation creates platform-specific prompts from a single source. 
See [CIP-0012](cip/cip0012.md).
```

**Two-paragraph** (for docs/features.md):
```markdown
## Multi-Platform AI Assistant Support

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, 
and Codex from a single source (`templates/prompts/`). Users select their platform 
during installation via the `VIBESAFE_PLATFORM` environment variable.

**Architecture**: Platform-agnostic base content is stored in `templates/prompts/`. 
During installation, the system detects or prompts for platform choice, then generates 
platform-specific files (`.cursor/rules/`, `CLAUDE.md`, etc.). This design enables 
consistent content across platforms while respecting each platform's discovery mechanism.

**Design Rationale**: [CIP-0012](../cip/cip0012.md) | **Requirements**: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md)
```

**Full section** (for docs/architecture.md):
```markdown
## Multi-Platform AI Assistant Support

### Overview

VibeSafe supports multiple AI coding assistants: Cursor, GitHub Copilot, Claude Code, and Codex. 
This enables users to choose their preferred assistant without sacrificing VibeSafe's guidance.

### Architecture

**Single Source of Truth**: Platform-agnostic content in `templates/prompts/`
- `always-apply/`: Core VibeSafe guidance (general development, requirements, CIPs, etc.)
- `context-specific/`: Component-specific guidance (backlog, tenets, etc.)

**Install-Time Generation**: Platform-specific files created during `install-minimal.sh`
- Detects user's chosen platform via `VIBESAFE_PLATFORM` environment variable
- Generates files in platform-specific locations:
  - Cursor: `.cursor/rules/*.mdc` with YAML frontmatter
  - Copilot: `.github/copilot-instructions.md` (concatenated)
  - Claude Code: `CLAUDE.md` (concatenated)
  - Codex: `AGENTS.md` (concatenated)

**Platform Detection**: Automatic or user-specified
- Auto-detects if `.cursor/` exists or `VIBESAFE_PLATFORM` set
- Defaults to generating all platforms if ambiguous
- User can specify: `VIBESAFE_PLATFORM=cursor ./install-minimal.sh`

### Design Rationale

**Why single source?**
- Consistency: All platforms receive identical guidance
- Maintainability: Update once, deploy everywhere
- User Autonomy: Choose any assistant without feature loss

**Why install-time generation?**
- Respects platform discovery mechanisms (Cursor uses specific paths, Copilot uses different ones)
- Avoids bloating user repositories with multiple copies
- Enables platform-specific formatting (YAML vs. plain markdown)

**Alternatives considered**:
- Symlinks: Doesn't work across platforms, requires git configuration
- Manual duplication: High maintenance burden, inconsistency risk
- Runtime generation: Adds complexity, slower feedback

See [CIP-0012](../cip/cip0012.md) for complete design evolution, alternatives analysis, 
and implementation phases.

### Related

- **Requirements**: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md) (Multi-platform support)
- **Tenets**: User Autonomy Over Prescription, Simplicity at All Levels
```

---

## Traceability

**Always link formal docs back to CIPs**. This enables:
- Readers to find detailed rationale when needed
- Maintaining connection between WHAT (docs) and HOW (CIP)
- Validation that docs match implementation

### Traceability Formats

**Inline reference** (preferred):
```markdown
Multi-platform support ([CIP-0012](../cip/cip0012.md)) enables users to choose their AI assistant.
```

**Section footer**:
```markdown
## Feature Name

[Description here]

**Design**: [CIP-0012](../cip/cip0012.md) | **Requirements**: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md)
```

**Separate references section**:
```markdown
## Feature Name

[Description here]

### References

- Architecture: [CIP-0012](../cip/cip0012.md)
- Requirements: [REQ-000C](../requirements/req000C_ai-assistant-framework-independence.md)
- Related: [CIP-0007](../cip/cip0007.md)
```

---

## Configuration Override

**Optional**: Create `.vibesafe/compression.yml` to customize compression targets.

```yaml
compression:
  # Specify system type (overrides detection)
  system: "sphinx"  # or "mkdocs", "plain-markdown", "minimal", "custom"
  
  # Custom compression targets
  targets:
    infrastructure: "docs/architecture/systems.md"
    feature: "docs/features/"
    process: "docs/workflow/practices.md"
  
  # Format preference
  format: "markdown"  # or "rst"
  
  # Traceability style
  traceability: "inline"  # or "footer", "separate-section"
```

**When to use configuration**:
- You have a custom documentation structure
- Default detection doesn't match your setup
- You want specific file naming conventions
- You're using a documentation system VibeSafe doesn't detect

---

## Compression Workflow

### Step-by-Step Process

1. **Identify Compression Candidates**
   ```bash
   ./whats-next --compression-check
   ```

2. **Copy Compression Checklist**
   ```bash
   cp templates/compression_checklist.md cip/cip0012-compression.md
   ```

3. **Read the Closed CIP**
   - Identify key decisions, outcomes, architecture
   - Note which tenets/requirements informed the design

4. **Choose Compression Targets**
   - Use detection-based suggestions (see "Adaptive Compression Targets" above)
   - Or specify custom targets in `.vibesafe/compression.yml`

5. **Write Compressed Documentation**
   - Follow style guide: WHAT → WHY → HOW (high-level) → TRACE
   - Balance detail and brevity
   - Include traceability links

6. **Mark CIP as Compressed**
   ```yaml
   # In cip/cipXXXX.md:
   compressed: true
   ```

7. **Commit**
   ```bash
   git add cip/cipXXXX.md docs/ README.md
   git commit -m "Compress CIP-XXXX into formal documentation"
   ```

---

## When to Skip Compression

**Not every CIP needs compression**. Skip if:

- **Minor/internal changes**: Small refactorings, code cleanups
- **Rejected CIPs**: Already documented as rejected
- **Superseded CIPs**: Replaced by later CIP (compress the superseding one instead)
- **Implementation details only**: Fully captured in code comments and tests

**When in doubt**: Compress. Users can always read formal docs to understand current state without reading every CIP.

---

## FAQ

### Q: What if I don't have a docs/ directory yet?

**A**: Start with `README.md` sections. When it grows, create `docs/` and move content there. VibeSafe adapts to your choice.

### Q: Can I use a different documentation system than the ones listed?

**A**: Yes! Create `.vibesafe/compression.yml` and specify your custom targets.

### Q: Should I compress every detail from the CIP?

**A**: No! Compress WHAT+WHY+HOW (high-level). Leave detailed implementation in CIP.

### Q: What if my CIP is 30 pages?

**A**: That's perfect for compression! Distill to 2-3 paragraphs + link to CIP.

### Q: Do I need to compress CIPs immediately after closing?

**A**: No rush. `./whats-next` will remind you. Older CIPs get higher priority.

### Q: What if I realize I need more detail after compression?

**A**: The CIP is still there with full history! Formal docs should link back to it.

---

## Examples from VibeSafe

### CIP-0012: Multi-Platform AI Assistant Support

**Before compression**: 15-page CIP with 4 implementation phases, detailed design evolution, alternatives analysis

**After compression**:
- `README.md`: 1 paragraph overview (see "Examples by Length" above)
- `docs/architecture.md`: 3-paragraph architecture section
- CIP-0012: Marked `compressed: true`, full history preserved

**Traceability**: README → docs/architecture.md → CIP-0012 → REQ-000C

### CIP-0013: Documentation Compression Stage

**Before compression**: This CIP! (5 phases, extensive design rationale)

**After compression** (will happen when CIP closes):
- `README.md`: Add compression to workflow diagram
- `docs/compression-guide.md`: This file!
- `docs/workflow.md`: Compression stage in VibeSafe workflow
- CIP-0013: Mark `compressed: true`

---

## Related

- **Template**: [templates/compression_checklist.md](../templates/compression_checklist.md) - Use this for each CIP
- **CIP-0013**: [cip/cip0013.md](../cip/cip0013.md) - Full compression stage design
- **REQ-000E**: [requirements/req000E_documentation-synchronization.md](../requirements/req000E_documentation-synchronization.md)
- **REQ-000F**: [requirements/req000F_documentation-structure-specification.md](../requirements/req000F_documentation-structure-specification.md)

---

## Summary

**Remember**:
1. ✅ **Detect**, don't prescribe (respect your chosen documentation system)
2. ✅ **Guide**, don't force (sensible defaults, allow overrides)
3. ✅ **Compress**, don't duplicate (WHAT+WHY+HOW → CIP for details)
4. ✅ **Trace**, don't orphan (always link docs → CIP)
5. ✅ **Adapt**, don't standardize (works with any documentation system)

Run `./whats-next --compression-check` to see what needs compressing!

