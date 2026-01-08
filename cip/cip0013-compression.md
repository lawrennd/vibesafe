# Compression Checklist: CIP-0013 (Documentation Compression Stage)

**CIP**: 0013  
**Title**: Documentation Compression Stage  
**Closed**: 2026-01-08  
**Priority**: Medium  
**Type**: Process/Workflow  

## Quick Assessment

**Should this CIP be compressed?** ✅ Yes - This is THE meta compression CIP. Must compress it using its own workflow!

**Compression Targets**:
- ✅ README.md (already updated in Phase 4)
- ⬜ docs/compression-guide.md (extract from CIP-0013)
- ⬜ docs/whats_next_script.md (add compression section)

---

## Phase 1: Read & Extract

### Key Decisions from CIP-0013
- Established 5-stage workflow: WHY→WHAT→HOW→DO→DOCUMENT
- Added `compressed` metadata to CIP templates
- Integrated compression detection into `whats-next` (8 prompt triggers)
- Created compression checklist template
- Created quarterly review template
- Updated documentation lifecycle from 3 phases to 4 phases
- Added 6th natural breakpoint for AI assistants (compression after closure)

### Essential Outcomes
1. **Compression workflow** is now part of VibeSafe's standard process
2. **`whats-next`** automatically detects and suggests compression
3. **Templates** exist for compression checklists and quarterly reviews
4. **Workflow documentation** updated to include compression stage

### Implementation Artifacts
- `templates/compression_checklist.md` - Compression checklist template
- `templates/quarterly_compression_review_template.md` - Quarterly review template
- `scripts/whats_next.py` - Compression detection logic (8 functions added)
- `tests/test_whats_next.py` - 22 new tests for compression features
- `templates/cip/cip_template.md` - Added `compressed` field
- Updated cursor rules, README, workflow docs

---

## Phase 2: Identify Targets

### README.md
- [x] **Status**: Already updated in Phase 4
- [x] **Content**: Added compression to "What's Inside" (#6)
- [x] **Content**: Updated "Why the Process?" with compression explanation
- [x] **Content**: Added workflow diagram: WHY→WHAT→HOW→DO→DOCUMENT
- [ ] **Add**: Link to formal compression guide (after creating it)

### docs/compression-guide.md (NEW)
- [ ] **Create**: Extract "Compression Guide" section from CIP-0013
- [ ] **Include**: Documentation structure detection logic
- [ ] **Include**: Adaptive compression targets (Sphinx, MkDocs, plain markdown, minimal)
- [ ] **Include**: Style guide (WHAT→WHY→HOW→TRACE)
- [ ] **Include**: Traceability formats (inline, footer)
- [ ] **Include**: Compression workflow (7 steps)
- [ ] **Include**: When to skip compression
- [ ] **Include**: Configuration override (.vibesafe/compression.yml)

### docs/whats_next_script.md
- [ ] **Add**: New section on `--compression-check` flag
- [ ] **Add**: Explanation of compression suggestions
- [ ] **Add**: Link to compression guide

---

## Phase 3: Update Documentation

### Extract Compression Guide from CIP-0013

Source: `cip/cip0013.md` lines ~262-373 ("Compression Guide" section)

Destination: `docs/compression-guide.md`

**Content Structure**:
1. Introduction (what is compression?)
2. Documentation Structure Detection (4 systems: Sphinx, MkDocs, Markdown, Minimal)
3. Adaptive Compression Targets (tables for each system)
4. Style Guide (WHAT→WHY→HOW→TRACE with examples)
5. Traceability Formats (inline, footer)
6. Compression Workflow (7 steps)
7. When to Skip Compression (4 cases)
8. Configuration Override (optional `.vibesafe/compression.yml`)
9. Periodic Review Process (quarterly)

### Update README.md

Add link to compression guide:
```markdown
6. *Documentation Compression*: A systematic workflow (WHY→WHAT→HOW→DO→DOCUMENT) 
   that consolidates closed CIPs and completed implementations into permanent, accessible 
   formal documentation. See [CIP-0013](cip/cip0013.md) and [Compression Guide](docs/compression-guide.md).
```

### Update docs/whats_next_script.md

Add new section:
```markdown
## Compression Detection (New in v2.0)

The "What's Next" script now detects closed CIPs that haven't been compressed into formal documentation and suggests compression actions.

### --compression-check Flag

```bash
./whats-next --compression-check
```

Shows detailed compression candidates with age, priority, and batch opportunities.

### Compression Suggestions

When closed CIPs need compression, `whats-next` will suggest:
- Use `templates/compression_checklist.md` to guide the process
- Batch compress multiple CIPs if 3+ closed within 7 days
- Prioritize: High-priority and older CIPs first

See [Compression Guide](compression-guide.md) for the full workflow.
```

---

## Phase 4: Traceability

### Add References

In `docs/compression-guide.md`, add footer:
```markdown
---

## References

- **Design**: [CIP-0013](../cip/cip0013.md) - Documentation Compression Stage
- **Requirements**: [REQ-000E](../requirements/req000E_documentation-synchronization.md), [REQ-000F](../requirements/req000F_documentation-structure-specification.md)
- **Templates**: [Compression Checklist](../templates/compression_checklist.md), [Quarterly Review](../templates/quarterly_compression_review_template.md)
```

In README.md, ensure link exists.

In `docs/whats_next_script.md`, link to compression guide.

---

## Phase 5: Mark Compressed

After completing all updates:

1. Set `compressed: true` in `cip/cip0013.md` frontmatter
2. Commit with message:
   ```
   Compress CIP-0013: Extract compression guide into formal docs
   
   Created docs/compression-guide.md from CIP-0013
   Updated README.md with compression guide link
   Updated docs/whats_next_script.md with compression detection docs
   Marked CIP-0013 compressed: true
   ```

---

## Compression Quality Check

- [ ] README.md links to compression guide
- [ ] docs/compression-guide.md created with all sections
- [ ] docs/whats_next_script.md documents compression features
- [ ] All traceability links work
- [ ] CIP-0013 marked `compressed: true`
- [ ] Commit message references CIP-0013

---

## Notes

**Why This Matters**: CIP-0013 is the meta CIP that defines the compression workflow. Compressing it using its own process validates the workflow and provides the canonical example for future compressions.

**Dogfooding**: We're using the compression checklist (that CIP-0013 created) to compress CIP-0013 itself. Beautiful recursion! 🪞

**Status**: Ready to execute
