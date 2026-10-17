# VibeSafe Documentation Compression Guide

> **Extracted from**: [CIP-0013: Documentation Compression Stage](../cip/cip0013.md)  
> **Status**: Formal documentation (compressed from closed CIP)

## What is Documentation Compression?

**Documentation compression** is the systematic process of distilling knowledge from closed CIPs (design rationale), completed backlog tasks (implementation details), and finalized code into streamlined formal documentation that future users can understand without reading the entire development history.

**The Compression Metaphor**: During active development, information is "expanded" across CIPs, backlog tasks, and code. After completion, this information should be "compressed" into permanent, accessible documentation.

**Workflow**: WHY (Tenets) → WHAT (Requirements) → HOW (CIPs) → DO (Backlog) → **DOCUMENT** (Compression)

---

## Documentation Structure Detection

VibeSafe **detects** your existing documentation structure and adapts guidance accordingly. We never force a specific system.

**Detection Logic**:

| Check | Result | Suggested Targets |
|-------|--------|-------------------|
| `docs/conf.py` exists? | **Sphinx** (✨ supports Markdown via MyST) | `docs/source/*.{rst,md}` + README.md |
| `mkdocs.yml` exists? | **MkDocs** | `docs/*.md` + README.md |
| `docs/*.md` exist? | **Plain Markdown** | `docs/*.md` + README.md |
| None of above? | **Minimal** | README.md + optional `docs/` |

**💡 Recommended: Sphinx with MyST Parser**

Sphinx with the MyST parser gives you:
- ✅ Professional documentation with Markdown (no need to learn reStructuredText)
- ✅ ReadTheDocs integration for hosting
- ✅ Cross-references, table of contents, search
- ✅ Multiple output formats (HTML, PDF, ePub)
- ✅ Full Markdown syntax support

See [MyST Parser documentation](https://myst-parser.readthedocs.io/) for setup.

---

## Adaptive Compression Targets

### For Sphinx Users (with MyST for Markdown)

- Infrastructure CIPs → `docs/source/architecture.md` (or `.rst`)
- Feature CIPs → `docs/source/features.md` (or `.rst`)
- Process CIPs → `docs/source/workflow.md` (or `.rst`)
- High-level → `README.md`

**Note**: With MyST parser, you can write Sphinx docs in Markdown! VibeSafe itself uses this approach.

### For MkDocs/Plain Markdown Users

- Infrastructure CIPs → `docs/architecture.md`
- Feature CIPs → `docs/features.md`
- Process CIPs → `docs/workflow.md`
- High-level → `README.md`

### For Minimal Users

- Start with `README.md` sections
- Create `docs/` when it grows

---

## Style Guide for Compression

**Structure**: WHAT → WHY → HOW (high-level) → TRACE

### Balance Detail and Brevity

- ❌ **Too brief**: "Added search" (no context)
- ❌ **Too detailed**: "Implemented BM25 algorithm with tf-idf weighting..." (belongs in CIP)
- ✅ **Just right**: "Full-text search with semantic indexing. See [CIP-00XX](../cip/cip00XX.md) for details"

### Examples by Length

**One-paragraph (README)**:
```markdown
## Multi-Platform AI Assistant Support
VibeSafe works with Cursor, Copilot, Claude, and Codex. See [CIP-0012](cip/cip0012.md).
```

**Two-paragraph (docs/features.md)**:
```markdown
## Multi-Platform AI Assistant Support

VibeSafe generates prompts for Cursor, Copilot, Claude, and Codex from `templates/prompts/`. 
Users select platform via `VIBESAFE_PLATFORM` during installation.

**Architecture**: Platform-agnostic base → install-time generation → platform-specific files.
See [CIP-0012](../cip/cip0012.md) for detailed rationale.
```

---

## Traceability Formats

**Always link docs → CIP**. This maintains traceability and allows readers to dive deeper when needed.

### Inline References

```markdown
Multi-platform support ([CIP-0012](../cip/cip0012.md)) enables...
```

### Footer References

```markdown
**Design**: [CIP-0012](../cip/cip0012.md) | **Requirements**: [REQ-000C](../requirements/req000C.md)
```

---

## Compression Workflow (7 Steps)

1. **Identify**: Run `./whats-next --compression-check` to find closed CIPs needing compression
2. **Copy template**: `cp templates/compression_checklist.md cip/cipXXXX-compression.md`
3. **Read CIP**: Identify key decisions, outcomes, and essential knowledge
4. **Choose targets**: Use detection-based suggestions or custom config
5. **Write compressed docs**: Follow WHAT→WHY→HOW→TRACE structure
6. **Mark compressed**: Set `compressed: true` in CIP YAML frontmatter
7. **Commit**: `git commit -m "Compress CIP-XXXX: [description]"`

---

## When to Skip Compression

Not all closed CIPs need formal documentation compression. Skip if:

- **Minor/internal changes**: Small process adjustments with no external impact
- **Rejected CIPs**: No implementation to document
- **Superseded CIPs**: Compress the replacement instead
- **Implementation details only**: Fully captured in code/tests

When skipping, still set `compressed: true` to remove the CIP from compression suggestions.

---

## Configuration Override (Optional)

Create `.vibesafe/documentation.yml` to customize compression behavior:

```yaml
documentation:
  # Recommended: Sphinx with MyST for Markdown support
  system: "sphinx-myst"  # Options: sphinx, sphinx-myst, mkdocs, plain-markdown, readme-only
  source_dir: "docs/source"
  format: "markdown"  # Primary format (markdown or rst)
  parser: "myst"  # For Sphinx: myst (Markdown) or default (reStructuredText)
  
  targets:
    infrastructure: "docs/source/architecture.md"
    feature: "docs/source/features.md"
    process: "docs/source/workflow.md"
    guides: "docs/source/"

compression:
  enabled: true
  traceability: "inline"  # or "footer"
```

**Why sphinx-myst?** Get professional documentation capabilities while writing in Markdown!

---

## Periodic Compression Review

**Why periodic reviews?** While `whats-next` prompts help, periodic reviews ensure nothing is forgotten. Quarterly rhythm provides natural checkpoints for documentation maintenance.

### Quarterly Review Workflow

1. **Check Status**: `./whats-next --compression-check`
2. **Prioritize**: Which CIPs are critical to document? Which can wait?
3. **Batch Compress**: Work through high-value CIPs using compression checklist
4. **Update Metrics**: Track compression quality (see below)
5. **Reflect**: What went well? What slipped through? Adjust workflow if needed

### Compression Quality Metrics

Track these quarterly:

| Metric | Target | Why |
|--------|--------|-----|
| 30-day compliance | >80% | Most CIPs compressed quickly |
| 90-day compliance | >95% | Nearly all CIPs compressed eventually |
| Uncompressed backlog | <5 CIPs | Manageable queue |
| Oldest uncompressed | <120 days | Nothing forgotten >4 months |

### Creating Quarterly Review Tasks

```bash
# At end of each quarter (or start of next)
cp templates/quarterly_compression_review_template.md \
   backlog/documentation/YYYY-QX_quarterly-compression-review.md
# Edit dates, quarter number, set status to "Ready"
```

**First Review**: Recommend Q2 2026 (Apr-Jun) as the first periodic review, allowing time for initial CIPs to close and establish baseline metrics.

---

## Compression vs. CIP History

### Compression is NOT

- ❌ Deleting CIPs (they remain for historical reference)
- ❌ Rewriting CIPs (they stay as-is, documenting the journey)
- ❌ Creating duplicate documentation (extract essence, don't copy)
- ❌ Required before CIP closure (recommended after)

### Compression IS

- ✅ Extracting essential knowledge from development artifacts
- ✅ Creating accessible documentation for future users
- ✅ Validating that implementation matches design intent
- ✅ Closing the feedback loop: WHY→WHAT→HOW→DO→DOCUMENT→WHY

---

## Tools and Templates

- **Compression Checklist**: `templates/compression_checklist.md` - Step-by-step guide for compressing a single CIP
- **Quarterly Review Template**: `templates/quarterly_compression_review_template.md` - Periodic review workflow
- **Detection Script**: `./whats-next --compression-check` - Find CIPs needing compression
- **Example**: This guide was created by compressing [CIP-0013](../cip/cip0013.md) using its own process!

---

## References

- **Design**: [CIP-0013: Documentation Compression Stage](../cip/cip0013.md)
- **Requirements**: 
  - [REQ-000E: Documentation Synchronization with Implementation](../requirements/req000E_documentation-synchronization.md)
  - [REQ-000F: Documentation Structure Specification](../requirements/req000F_documentation-structure-specification.md)
- **Templates**: 
  - [Compression Checklist](../templates/compression_checklist.md)
  - [Quarterly Review Template](../templates/quarterly_compression_review_template.md)
- **Related CIPs**:
  - [CIP-0007: Documentation and Implementation as a Unified Whole](../cip/cip0007.md)

---

*Last updated: 2026-01-08*  
*Compressed from CIP-0013 (closed 2026-01-08)*

