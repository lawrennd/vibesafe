---
id: "2026-01-09_traceability-in-compressed-documentation"
title: "Traceability in Compressed Documentation"
status: "Proposed"
priority: "High"
category: "documentation"
created: "2026-01-09"
last_updated: "2026-01-09"
owner: "Neil Lawrence"
related_cips: ["0013"]
tags: ["documentation", "compression", "traceability", "quality"]
---

# Task: Traceability in Compressed Documentation

## Description

Current compressed documentation (e.g., `docs/source/architecture.md`, `docs/source/workflow.md`) primarily references CIPs (HOW) but lacks systematic references to requirements (WHAT) and tenets (WHY). This breaks the traceability chain that VibeSafe is designed to create and obscures the rationale behind architectural decisions.

**Problem identified:**
- ✅ CIPs (HOW) are consistently referenced
- ❌ Requirements (WHAT) are rarely linked
- ❌ Tenets (WHY) are inconsistently referenced

**Example of current approach:**
```markdown
### Clean Installation Philosophy
**Implemented in:** [CIP-000E](../../cip/cip000E.md)
```

**What we should have:**
```markdown
### Clean Installation Philosophy
**Need:** [REQ-0007](../../requirements/req0007_automatic-system-updates.md) - Automatic System Updates  
**Guided by:** [Simplicity at All Levels](../../tenets/vibesafe/simplicity-of-use.md) tenet  
**Solution:** CIPs [000E](../../cip/cip000E.md), [000F](../../cip/cip000F.md), [000B](../../cip/cip000B.md)
```

This task establishes traceability standards for compression and re-compresses existing documentation to meet those standards.

## Acceptance Criteria

### Phase 1: Establish Traceability Standards
- [ ] Update `docs/source/compression-guide.md` with traceability requirements
- [ ] Define standard format for WHY→WHAT→HOW traces in compressed docs
- [ ] Create examples showing proper traceability in compressed sections
- [ ] Document when/how to trace requirements and tenets

### Phase 2: Extend `whats-next` Script
- [ ] Add detection for compressed docs missing requirement references
- [ ] Add detection for compressed docs missing tenet references
- [ ] Generate warnings for sections with only CIP references
- [ ] Add `--check-traceability` flag for focused validation
- [ ] Update tests for new traceability checks

### Phase 3: Re-compress `architecture.md`
- [ ] Review each section and identify relevant requirements
- [ ] Review each section and identify relevant tenets
- [ ] Add WHY→WHAT→HOW traces to all major sections
- [ ] Verify all links are valid and accurate
- [ ] Update compression checklists for affected CIPs

### Phase 4: Re-compress `workflow.md`
- [ ] Review each section and identify relevant requirements
- [ ] Review each section and identify relevant tenets
- [ ] Add WHY→WHAT→HOW traces to all major sections
- [ ] Verify all links are valid and accurate
- [ ] Update compression checklists for affected CIPs

### Phase 5: Validation & Documentation
- [ ] Run `whats-next --check-traceability` on updated docs
- [ ] Verify no missing traceability warnings
- [ ] Update compression checklist template with traceability steps
- [ ] Document traceability standard in contributing guide
- [ ] Run full validation suite

## Implementation Notes

### Standard Traceability Format

For each major section in compressed documentation:

```markdown
## Feature/Architecture Name

**Need:** [REQ-XXXX](link) - Brief description  
**Guided by:** [Tenet Name](link) tenet (optional if indirect)  
**Solution:** [CIP-XXXX](link), [CIP-YYYY](link)  

[Content describing the feature/architecture]
```

**When to include each component:**
- **Need (REQ-XXXX)**: Always if a requirement exists that this directly addresses
- **Guided by**: When design decisions clearly align with specific tenets
- **Solution (CIP)**: Always (this is already done)

### Requirements to Map

Key requirements likely relevant to architecture/workflow docs:
- REQ-0001: YAML Standardization
- REQ-0002: Simplify Requirements Framework
- REQ-0005: Project Summary Tool
- REQ-0006: Process Conformance Validation
- REQ-0007: Automatic System Updates
- REQ-0008: Clear Framework Boundaries
- REQ-000B: AI Access to Project Tenets
- REQ-000C: AI Assistant Framework Independence
- REQ-000D: CIPs as Self-Contained Design Documents
- REQ-000E: Documentation Synchronization
- REQ-000F: Documentation Structure Specification

### Tenets to Map

Key tenets likely relevant:
- `simplicity-of-use.md` - Installation, tooling, defaults
- `user-autonomy.md` - Configuration, flexibility
- `documentation-as-code.md` - Documentation approach
- `validation-led-development.md` - Testing, validation
- `shared-information-landmarks.md` - Structure, navigation
- `information-exploration-patterns.md` - Documentation organization

### `whats-next` Detection Logic

Add to existing compression checks:

```python
def check_compressed_doc_traceability(doc_path):
    """Check if compressed docs have proper WHY→WHAT→HOW traces."""
    content = read_file(doc_path)
    sections = extract_sections(content)
    
    issues = []
    for section in sections:
        has_cip = "CIP-" in section or "[CIP" in section
        has_req = "REQ-" in section or "Requirement" in section
        has_tenet = "tenet" in section.lower()
        
        if has_cip and not has_req:
            issues.append(f"{section.title}: Has CIP but no requirement reference")
        if has_cip and not has_tenet:
            # Warning, not error (tenets are optional if indirect)
            issues.append(f"{section.title}: Consider adding tenet reference")
    
    return issues
```

### Migration Strategy

1. **Start with architecture.md** (more factual, less narrative)
2. **Then workflow.md** (more abstract, requires careful mapping)
3. **Update compression checklist template** so future compressions include traceability
4. **Validate with `whats-next`** before considering complete

## Related

- **CIP-0013**: Documentation Compression Stage (defines compression workflow)
- **REQ-000E**: Documentation Synchronization (requirement for accurate docs)
- **REQ-0006**: Process Conformance Validation (includes traceability validation)
- **CIP-0014**: Traceability Analysis in `whats-next` (complementary effort)

## Progress Updates

### 2026-01-09
Task created with Proposed status. Identified during compression of CIPs - noticed missing WHY→WHAT traces in compressed documentation.

