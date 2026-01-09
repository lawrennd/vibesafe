---
id: "2026-01-09_validate-human-authorship"
title: "Validate Human Authorship in YAML Frontmatter"
status: "Proposed"
priority: "Medium"
created: "2026-01-09"
last_updated: "2026-01-09"
category: "infrastructure"
related_cips: []  # Could relate to validation/testing CIPs if they exist
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- validation
- accountability
- metadata
---

# Task: Validate Human Authorship in YAML Frontmatter

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Add validation to ensure that `author` and `owner` fields in YAML frontmatter never contain references to AI assistants, LLMs, coding agents, or similar non-human entities. 

**Rationale**: AI assistants lack social agency - they cannot be held accountable for decisions or documentation. All VibeSafe documentation must be traceable to a human author who has a stake in society and can be held responsible for the content.

**Scope**: This validation should check:
- CIP frontmatter (`author` field)
- Backlog task frontmatter (`owner` field)
- Requirements frontmatter (`owner` field, if present)
- Any other YAML frontmatter that includes authorship/ownership fields

**Prohibited values** (case-insensitive, partial match):
- "AI Assistant"
- "LLM"
- "Coding Agent"
- "AI"
- "ChatGPT"
- "Claude"
- "Copilot"
- "Cursor"
- Similar patterns indicating non-human authorship

## Acceptance Criteria

- [ ] Validation script detects prohibited authorship values in YAML frontmatter
- [ ] Validation checks all relevant file types (CIPs, backlog, requirements)
- [ ] Validation provides clear error messages indicating which files and fields violate the rule
- [ ] Validation includes pattern matching to catch variations (e.g., "ai assistant", "AI-Assistant", etc.)
- [ ] Tests confirm that valid human names pass validation
- [ ] Tests confirm that prohibited AI references fail validation
- [ ] Documentation explains the accountability rationale for this validation
- [ ] Integration with existing validation infrastructure (e.g., `validate_vibesafe_structure.py` or similar)

## Implementation Notes

### Approach

1. **Extend existing validation**: Add to `scripts/validate_vibesafe_structure.py` or create dedicated authorship validator
2. **Pattern matching**: Use regular expressions to catch variations:
   - Case-insensitive matching
   - Partial matches (e.g., "created by AI" should fail)
   - Common AI assistant names and terms
3. **Integration points**:
   - Pre-commit hooks (optional)
   - CI/CD pipeline checks
   - `./whats-next` script warnings for invalid authorship

### Technical Notes

```python
# Example validation logic
PROHIBITED_AUTHOR_PATTERNS = [
    r'\bai\b',
    r'\bllm\b',
    r'ai[\s\-]?assistant',
    r'coding[\s\-]?agent',
    r'chatgpt',
    r'claude',
    r'copilot',
    r'cursor',
    r'artificial[\s\-]?intelligence',
]

def validate_author_field(author_value, file_path):
    """Validate that author field contains a human name."""
    if not author_value:
        return False, "Author field is empty"
    
    author_lower = author_value.lower()
    for pattern in PROHIBITED_AUTHOR_PATTERNS:
        if re.search(pattern, author_lower):
            return False, f"Author field contains prohibited value: '{author_value}'"
    
    return True, None
```

### Fields to check by file type:
- **CIPs**: `author` field
- **Backlog**: `owner` field  
- **Requirements**: `owner` field (if present), `stakeholders` (if contains AI refs)
- **Tenets**: `author` field (if we add one)

### Edge cases:
- Empty/missing fields: Should warn but might not be critical (separate validation)
- Multiple authors: Check each name in the list
- Organization names: May need allowlist for legitimate org names that contain "AI" (e.g., "AI Research Lab" as an org)

## Related

- **Tenet**: Documentation and Implementation as a Unified Whole - accountability requires human ownership
- **Tenet**: Build Verification Before Implementation - validation ensures standards
- **Philosophy**: Social agency and accountability in documentation
- **Script**: `scripts/validate_vibesafe_structure.py` (likely integration point)
- **Script**: `scripts/whats_next.py` (could show warnings)

## Progress Updates

### 2026-01-09

Task created with Proposed status. Identified need for validation to ensure human accountability in all VibeSafe documentation authorship fields.

