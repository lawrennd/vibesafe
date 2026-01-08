# Compression Checklist Template

> **Purpose**: This template guides you through compressing a closed CIP's key decisions into formal documentation.
>
> **When to use**: After a CIP is closed (implementation complete and verified), use this checklist to extract essential knowledge and update formal docs.
>
> **Why compression matters**: CIPs document the development journey (design evolution, alternatives considered, implementation details). Formal documentation should capture the final outcome (WHAT was built, essential WHY, architecture patterns). Users shouldn't need to read dozens of CIPs to understand current architecture.

## How to Use This Template

1. **Copy this file** for each CIP you're compressing
2. **Fill in CIP-specific details** in brackets `[...]`
3. **Check off tasks** as you complete them
4. **Adapt to your documentation system** (Sphinx, MkDocs, plain markdown, etc.)
5. **Commit** when compression is complete

---

# Compression Checklist: CIP-XXXX [Title]

**CIP**: [CIP-XXXX](../cip/cipXXXX.md)  
**Type**: [Infrastructure / Feature / Process]  
**Closed Date**: [YYYY-MM-DD]  
**Compression Date**: [YYYY-MM-DD]

## Pre-Compression Review

- [ ] Read closed CIP completely
- [ ] Identify key decisions and outcomes
- [ ] Note which tenets/requirements informed this CIP
- [ ] Determine CIP type (infrastructure, feature, or process)
- [ ] Identify target documentation locations (README, Sphinx, architecture docs)

### What to Extract (Compress)

✅ **DO extract and document**:
- Final architecture decisions and rationale
- WHAT was built (high-level)
- WHY it was built (user benefit, problem solved)
- HOW it works (architectural patterns, not implementation details)
- Key design tradeoffs and resolutions
- Links to related requirements and tenets

❌ **DON'T extract (leave in CIP history)**:
- Alternatives that were rejected (keep in CIP for historical context)
- Detailed implementation steps (captured in code and git history)
- Iteration and discussion history (keep in CIP)
- Temporary workarounds or experimental approaches
- Step-by-step backlog tasks (archived or deleted)

## Documentation Updates

### README.md Updates
- [ ] Add high-level feature description: [which section?]
- [ ] Update architecture overview if applicable
- [ ] Add to feature list or capabilities section
- [ ] Include user-facing benefit statement
- [ ] Reference CIP number: e.g., "Multi-platform support ([CIP-0012](cip/cip0012.md))"

### Architecture Documentation (docs/architecture.md or equivalent)
- [ ] Document architectural pattern or design decision
- [ ] Explain WHY this approach was chosen
- [ ] Describe key components and their interactions
- [ ] Note any important tradeoffs
- [ ] Link to CIP for detailed rationale

### API / Technical Documentation (Sphinx/MkDocs/etc.)
- [ ] Update API documentation if applicable
- [ ] Add code examples or tutorials
- [ ] Document new configuration options
- [ ] Update user guides or how-tos

### Other Documentation (specify)
- [ ] [Other location]: [what to add]

## Traceability

- [ ] Formal docs reference CIP number (e.g., "Compression stage ([CIP-0013](cip/cip0013.md))")
- [ ] Add "See [CIP-XXXX](../cip/cipXXXX.md) for detailed design rationale" links
- [ ] Verify links work correctly
- [ ] Ensure traceability from formal docs → CIP → requirements → tenets

## Finalization

- [ ] Set CIP `compressed: true` in YAML frontmatter
- [ ] Verify all compressed documentation is accurate
- [ ] Check that examples/code snippets work
- [ ] Commit with message: `"Compress CIP-XXXX into formal documentation"`
- [ ] Review: Can a new user understand the feature without reading the CIP?

---

## Example 1: Infrastructure CIP Compression

**Scenario**: CIP-0012 (AI Assistant Framework Independence)  
**Type**: Infrastructure  
**Target Docs**: README.md + docs/architecture.md

### Compression Summary:
- **From**: 15-page CIP with 4 implementation phases, 50+ commits, detailed design evolution
- **To**: 
  - README: 2-paragraph overview of multi-platform support
  - Architecture doc: Platform-agnostic prompt generation pattern
  - Reference to CIP-0012 for detailed implementation history

### Checklist Adaptations:
- ✅ Focus on **architecture patterns** (single source of truth → multi-platform generation)
- ✅ Document **platform detection logic** at high level
- ✅ Explain **WHY**: User autonomy (choose your AI assistant)
- ❌ Skip detailed implementation of each platform generator (in code)
- ❌ Skip iteration history (4 phases, design refinements) - keep in CIP

### Example Compressed Entry (README.md):
```markdown
## Multi-Platform AI Assistant Support

VibeSafe generates AI assistant prompts for Cursor, GitHub Copilot, Claude Code, and Codex from a single source (`templates/prompts/`). Users select their platform during installation via the `VIBESAFE_PLATFORM` environment variable.

**Design**: Platform-agnostic base content → install-time generation → platform-specific files

See [CIP-0012](cip/cip0012.md) for detailed design decisions and implementation history. Related: [REQ-000C](requirements/req000C_ai-assistant-framework-independence.md).
```

---

## Example 2: Feature CIP Compression

**Scenario**: Hypothetical CIP-00XX (Add Search Functionality)  
**Type**: Feature  
**Target Docs**: README.md + docs/features.md + Sphinx API docs

### Compression Summary:
- **From**: CIP with search algorithm comparison, implementation details, performance testing
- **To**: 
  - README: Feature announcement and user benefit
  - Features doc: How to use search
  - API docs: Search API reference with examples

### Checklist Adaptations:
- ✅ Focus on **user-facing functionality** (what can users do?)
- ✅ Document **API usage** with code examples
- ✅ Explain **search capabilities** and limitations
- ❌ Skip algorithm comparison details (in CIP)
- ❌ Skip performance benchmarks (captured in tests, summarized in CIP)

### Example Compressed Entry (docs/features.md):
```markdown
## Search Functionality

VibeSafe provides full-text search across CIPs, backlog tasks, and requirements using semantic indexing.

**Usage**:
```python
from vibesafe.search import search_documents

results = search_documents("compression workflow", doc_types=["cip", "requirements"])
for result in results:
    print(f"{result.title} (score: {result.relevance})")
```

**Capabilities**: Natural language queries, fuzzy matching, filtering by document type, relevance ranking.

Implementation details and algorithm selection rationale: [CIP-00XX](../cip/cip00XX.md).
```

---

## Example 3: Process CIP Compression

**Scenario**: CIP-0013 (Documentation Compression Stage)  
**Type**: Process  
**Target Docs**: README.md workflow diagram + docs/compression-guide.md

### Compression Summary:
- **From**: CIP with 5 implementation phases, whats-next integration details, tenet analysis
- **To**:
  - README: Updated workflow diagram (WHY→WHAT→HOW→DO→DOCUMENT)
  - Compression guide: How to compress CIPs (this checklist!)
  - CIP rules: Updated natural breakpoints

### Checklist Adaptations:
- ✅ Focus on **workflow changes** (new DOCUMENT stage)
- ✅ Document **how to perform compression** (user-facing process)
- ✅ Update **AI assistant prompts** to recognize compression stage
- ❌ Skip detailed whats-next implementation (in code)
- ❌ Skip phase-by-phase development (in CIP backlog tasks)

### Example Compressed Entry (README.md):
```markdown
## VibeSafe Workflow

```
WHY (Tenets) → WHAT (Requirements) → HOW (CIPs) → DO (Backlog) → DOCUMENT (Compression)
     ↑                                                                      ↓
     └─────────────────────── feedback loop ──────────────────────────────┘
```

After completing implementation, compress CIP knowledge into formal documentation so users can understand current architecture without reading development history. See [docs/compression-guide.md](docs/compression-guide.md) and [CIP-0013](cip/cip0013.md).
```

---

## Tips for Effective Compression

### Balance Detail and Brevity
- **Too brief**: "Added search" (users don't understand capability)
- **Too detailed**: "Implemented BM25 algorithm with tf-idf weighting and cosine similarity..." (belongs in CIP)
- **Just right**: "Full-text search with semantic indexing and relevance ranking" (user benefit clear, implementation abstracted)

### Maintain Traceability
Always link formal docs → CIP for readers who want deeper understanding:
- "See [CIP-XXXX](../cip/cipXXXX.md) for implementation details"
- "Design rationale: [CIP-XXXX](../cip/cipXXXX.md)"
- "Architecture decisions documented in [CIP-XXXX](../cip/cipXXXX.md)"

### Adapt to Your Documentation System
This checklist assumes a common structure, but adapt to your reality:
- **No Sphinx?** Use plain markdown in `docs/`
- **No architecture doc?** Add architecture section to README
- **Using MkDocs?** Adapt paths and format accordingly
- **Custom structure?** Use `.vibesafe/compression.yml` to configure targets

### When to Skip Compression
Not every CIP needs compression:
- **Minor/internal changes**: Small refactorings, code cleanups
- **Rejected CIPs**: Already documented as rejected, no formal docs needed
- **Superseded CIPs**: Replaced by later CIP, compress the superseding one instead
- **Implementation details only**: Changes fully captured in code comments and tests

---

## Related

- [CIP-0013: Documentation Compression Stage](../cip/cip0013.md) - Full design rationale
- [REQ-000E: Documentation Synchronization](../requirements/req000E_documentation-synchronization.md) - Requirements
- [CIP README: Documentation Compression](../cip/README.md#documentation-compression) - Overview

## Questions?

If you're unsure:
1. **What to compress?** Extract WHAT+WHY+HOW (high-level), leave detailed implementation in CIP
2. **Where to put it?** Start with README for visibility, then architecture docs for depth
3. **How much detail?** Enough for users to understand, not so much they need to read the CIP
4. **Traceability?** Always link formal docs → CIP for deeper rationale

When in doubt, compress less rather than more - you can always add detail later based on user questions.

