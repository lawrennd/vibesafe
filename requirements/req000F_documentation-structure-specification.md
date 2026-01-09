---
id: "000F"
title: "Projects Have Documented Documentation Structure"
status: "Implemented"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
related_tenets: ["user-autonomy", "documentation-as-code"]
stakeholders: ["users", "ai-assistants", "maintainers"]
tags: ["documentation", "structure", "specification", "compression"]
---

# REQ-000F: Projects Have Documented Documentation Structure

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.
> 
> ✅ Good: "Projects have explicit documentation structure specifications"  
> ❌ Bad: "Create .vibesafe/documentation.yml file" (that's HOW/DO)

## Description

Projects should have an explicit, documented specification of their documentation structure. This specification captures the user's chosen documentation system, file locations, and compression targets. It serves as the single source of truth for where documentation lives and how CIPs should be compressed into formal docs.

**Why this matters**: 

Without a documented structure:
- Compression becomes ad-hoc (each CIP compressed differently)
- Inconsistent documentation locations (some in README, some in docs/, some in Sphinx)
- AI assistants can't reliably guide compression
- New contributors don't know where to document changes
- `whats-next` can't provide specific compression suggestions

With a documented structure:
- Consistent compression targets (all infrastructure CIPs → `docs/architecture.md`)
- Clear expectations for contributors
- Automated compression guidance possible
- Respects User Autonomy (their choice, explicitly captured)

**Why this requirement stems from tenets**:

1. **User Autonomy**: We don't prescribe documentation structure, but we do need to capture the user's chosen structure explicitly. The specification documents their autonomous choice.

2. **Documentation and Implementation as Unified Whole**: Documentation structure is itself something that should be documented. The specification validates that the user has thought through their documentation approach.

**Who benefits**: 

- **Users**: Clear expectations for where to document changes
- **AI Assistants**: Can provide specific, actionable compression suggestions
- **Maintainers**: Consistent documentation structure over time
- **Contributors**: Know where to add new documentation

## Acceptance Criteria

What does "done" look like? These criteria serve as **triggers for `whats-next` prompts**, not blocking gates.

- [ ] **Prompt Trigger 1**: When compression is attempted but no documentation specification exists, `whats-next` prompts to create one
- [ ] **Prompt Trigger 2**: Documentation specification is discoverable (standard location like `.vibesafe/documentation.yml`, `docs/README.md`, or detected automatically)
- [ ] **Prompt Trigger 3**: Specification includes minimum required fields: documentation system type, primary compression targets
- [ ] **Prompt Trigger 4**: Compression tools (checklist, `whats-next`) use specification to provide specific suggestions
- [ ] **Prompt Trigger 5**: When documentation structure changes, `whats-next` suggests updating specification
- [ ] **Prompt Trigger 6**: New projects are prompted to create specification before first compression

**Note**: Specification is guidance, not enforcement. Users can compress CIPs without a specification (ad-hoc), but the system prompts them to create one for consistency.

## Notes (Optional)

### Specification Format Options

**User Autonomy**: Users choose how to specify their documentation structure. Common options:

**Option 1: Configuration File** (`.vibesafe/documentation.yml`)
```yaml
documentation:
  system: "sphinx"  # or "mkdocs", "plain-markdown", "readme-only"
  targets:
    infrastructure: "docs/source/architecture.rst"
    feature: "docs/source/features.rst"
    process: "docs/source/workflow.rst"
  format: "rst"  # or "md"
```

**Option 2: Documentation README** (`docs/README.md`)
```markdown
# Documentation Structure

- **System**: Sphinx (reStructuredText)
- **Compression Targets**:
  - Infrastructure CIPs → `docs/source/architecture.rst`
  - Feature CIPs → `docs/source/features.rst`
  - Process CIPs → `docs/source/workflow.rst`
```

**Option 3: Auto-Detection** (implicit specification)
```python
# VibeSafe detects structure and asks user to confirm:
# "Detected Sphinx docs in docs/source/. Use this structure? (y/n)"
# If confirmed, stores detection results
```

### Minimum Specification Requirements

At minimum, specification should include:
- **Documentation system type**: Sphinx, MkDocs, plain markdown, or README-only
- **Primary compression targets**: Where infrastructure/feature/process CIPs get compressed

Optional but recommended:
- Format preference (markdown vs. reStructuredText)
- Traceability style (inline links vs. footnotes)
- Custom compression rules

### When Specification is Missing

**Prompt-based approach** (User Autonomy):
```bash
$ ./whats-next
...
No documentation structure specification found.
Would you like to create one? This helps provide consistent compression guidance.
Run: ./vibesafe-init-docs (or create manually in .vibesafe/documentation.yml)
```

**Not blocking**: Users can still compress CIPs without a specification by manually specifying targets each time.

### Integration with Compression Workflow

**Phase 3** (CIP-0013) implements specification detection/creation:
1. Check for existing specification
2. If not found, prompt to create one (guided questionnaire)
3. Store specification in user's chosen format
4. Use specification for compression target suggestions

**whats-next** uses specification to provide specific prompts:
```
Before specification:
"Compress CIP-0012 into formal documentation"

After specification:
"Compress CIP-0012 (infrastructure) into docs/source/architecture.rst + README.md"
```

## References

- **Related Tenets**: `user-autonomy` (capture user's choice), `documentation-as-code` (document the documentation)
- **Related Requirements**: REQ-000E (Documentation Synchronization) - this requirement supports compression consistency
- **Related CIPs**: CIP-0013 Phase 3 implements specification detection/creation

## Progress Updates

### 2026-01-08
Requirement created with "Proposed" status. Identified during CIP-0013 implementation as missing requirement for consistent compression.

### 2026-01-08 (Later)
Requirement reviewed and approved. Status changed to "Ready" - fully defined and ready for CIP implementation (Phase 3).

