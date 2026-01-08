---
id: "2026-01-08_integrate-documentation-spec"
title: "Integrate Documentation Specification with Compression Tools"
status: "Proposed"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "features"
related_cips: ["0013"]
related_requirements: ["000F"]
owner: ""
dependencies: ["2026-01-08_migrate-docs-to-sphinx"]
tags: ["documentation", "compression", "whats-next", "integration", "req-000f"]
---

# Task: Integrate Documentation Specification with Compression Tools

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements REQ-000F Trigger 4: "Compression tools use specification to provide specific suggestions"

## Description

We've created `.vibesafe/documentation.yml` to document VibeSafe's documentation structure (REQ-000F), but `whats-next.py` and compression tools don't read or use it yet. This task integrates the specification so compression suggestions are **specific and actionable** rather than generic.

**Current State** (Generic):
```bash
$ ./whats-next
...
3. Batch compression opportunity: 9 CIPs closed within 7 days
4.    - CIP-0013: Documentation Compression Stage
5.    Use template: templates/compression_checklist.md
```

**Desired State** (Specific):
```bash
$ ./whats-next
...
3. Batch compression opportunity: 9 CIPs closed within 7 days
4.    - CIP-0013: Documentation Compression Stage (process)
5.      → Compress to: docs/source/workflow.md
6.    - CIP-000E: Clean Installation (infrastructure)
7.      → Compress to: docs/source/architecture.md
8.    Use template: templates/compression_checklist.md
9.    Targets from: .vibesafe/documentation.yml
```

**Why this matters**:
- **Actionable guidance**: Users know exactly where to compress CIPs
- **Consistency**: All infrastructure CIPs go to the same place
- **REQ-000F compliance**: Specification is actually used, not just documentation
- **Reduced friction**: No need to guess or ask where docs should go
- **Quality**: Traceability improves when targets are explicit

## Acceptance Criteria

### Phase 1: Detection and Loading
- [ ] `whats-next.py` detects `.vibesafe/documentation.yml` if it exists
- [ ] Parse YAML and extract `documentation.targets` configuration
- [ ] Gracefully handle missing specification (fall back to current behavior)
- [ ] Handle YAML parsing errors with helpful error messages
- [ ] Add `--show-doc-spec` flag to display loaded specification

### Phase 2: CIP Type Detection
- [ ] Add logic to infer CIP type from CIP content:
  - **infrastructure**: Installation, architecture, system changes (CIP-000E, CIP-000F, CIP-000A)
  - **feature**: New functionality, user-facing changes (CIP-0012)
  - **process**: Workflow, methodology, procedures (CIP-0013)
- [ ] Use CIP tags if present in frontmatter (`tags: ["infrastructure"]`)
- [ ] Default to `guides` type if unable to infer
- [ ] Add `type: infrastructure` field support in CIP frontmatter (optional)

### Phase 3: Enhanced Compression Suggestions
- [ ] When displaying compression candidates, show target location:
  ```
  CIP-0013: Documentation Compression Stage
    → Compress to: docs/source/workflow.md (process)
  ```
- [ ] Group CIPs by target location for batch compression
- [ ] Show warning if target file doesn't exist yet (but still suggest it)
- [ ] Include specification source: `(per .vibesafe/documentation.yml)`

### Phase 4: Compression Checklist Enhancement
- [ ] Update `templates/compression_checklist.md` to reference specification
- [ ] Add step: "Consult .vibesafe/documentation.yml for target location"
- [ ] Provide examples of target detection for different CIP types
- [ ] Add note about creating target files if they don't exist

### Phase 5: REQ-000F Prompt Triggers
Implement the missing REQ-000F acceptance criteria:

- [ ] **Trigger 1**: When compression attempted but no `.vibesafe/documentation.yml` exists:
  ```
  ⚠️  No documentation specification found
  → Create .vibesafe/documentation.yml to define compression targets
  → See: REQ-000F, docs/source/compression-guide.md
  ```

- [ ] **Trigger 4**: Compression tools use specification (this whole task!)

- [ ] **Trigger 5**: When docs structure changes, suggest updating specification:
  ```
  ℹ️  Documentation structure may have changed
  → Review .vibesafe/documentation.yml
  → New doc files: docs/source/new-file.md
  ```

- [ ] **Trigger 6**: New projects prompted to create specification before first compression:
  ```
  ℹ️  First compression detected, no specification exists
  → Create .vibesafe/documentation.yml to define structure
  → Run: ./whats-next --help-doc-spec
  ```

### Phase 6: Testing
- [ ] Unit tests for YAML loading and parsing
- [ ] Unit tests for CIP type detection logic
- [ ] Unit tests for target suggestion generation
- [ ] Integration tests for compression suggestions with spec
- [ ] Test graceful degradation when spec is missing/invalid

## Implementation Notes

### Specification File Location

**Standard location**: `.vibesafe/documentation.yml`

**Detection order** (for flexibility):
1. `.vibesafe/documentation.yml` (primary)
2. `.vibesafe/docs.yml` (alternative)
3. `docs/.vibesafe.yml` (alternative)
4. Auto-detect from presence of `docs/source/conf.py` (Sphinx) or `mkdocs.yml` (MkDocs)
5. Fall back to generic suggestions (current behavior)

### YAML Structure Expected

```yaml
documentation:
  system: "sphinx"  # or "mkdocs", "plain-markdown", "readme-only"
  targets:
    infrastructure: "docs/source/architecture.md"
    feature: "docs/source/features.md"
    process: "docs/source/workflow.md"
    guides: "docs/source/"  # Directory for general guides
```

### CIP Type Detection Strategy

**Order of detection**:
1. **Explicit tag**: Check `tags` in CIP frontmatter for type keywords
2. **Title keywords**: Search CIP title for "Installation", "Architecture", "Workflow", etc.
3. **Content analysis**: Scan "Summary" and "Motivation" sections for type indicators
4. **Related requirements**: Check if linked requirements have type hints
5. **Default**: Use `guides` as fallback

**Type keyword mapping**:
- `infrastructure`: "install", "architecture", "system", "deployment", "setup"
- `feature`: "implement", "add", "create", "functionality", "user"
- `process`: "workflow", "process", "methodology", "compression", "lifecycle"

### Code Changes Required

**In `scripts/whats_next.py`**:
```python
# New functions to add:

def load_documentation_spec(vibesafe_dir=".vibesafe") -> Optional[Dict[str, Any]]:
    """Load documentation specification from .vibesafe/documentation.yml"""
    # Try multiple locations
    # Parse YAML
    # Return targets dict or None

def detect_cip_type(cip_path: str, cip_info: Dict[str, Any]) -> str:
    """Detect CIP type (infrastructure, feature, process, guides)"""
    # Check tags
    # Check title/content keywords
    # Return detected type or "guides"

def get_compression_target(cip_type: str, doc_spec: Optional[Dict]) -> str:
    """Get compression target location for CIP type"""
    # Use doc_spec if available
    # Fall back to generic suggestion
    # Return target path

def generate_compression_suggestions(...):
    # Modify to include target locations
    # Group by target
    # Add spec source attribution
```

### Example Output Formats

**With specification**:
```
Compression Candidates (per .vibesafe/documentation.yml):

Infrastructure CIPs → docs/source/architecture.md:
  - CIP-000E: Clean Installation (234 days ago)
  - CIP-000F: Auto-Gitignore Protection (234 days ago)

Process CIPs → docs/source/workflow.md:
  - CIP-0013: Documentation Compression Stage (0 days ago)

Feature CIPs → docs/source/features.md:
  - CIP-0012: AI Assistant Framework Independence (0 days ago)
```

**Without specification** (current):
```
Compression Candidates:
  - CIP-0013: Documentation Compression Stage (0 days ago)
  - CIP-0012: AI Assistant Framework Independence (0 days ago)
  
Use template: templates/compression_checklist.md
```

### Graceful Degradation

**Missing specification**: Fall back to current behavior, optionally suggest creating one

**Invalid YAML**: Show error, fall back to current behavior:
```
⚠️  Could not parse .vibesafe/documentation.yml
Error: Invalid YAML syntax at line 12
→ Fix or remove file to continue
→ Falling back to generic compression suggestions
```

**Missing target in spec**: Use `guides` directory as fallback:
```
ℹ️  No target defined for 'testing' CIPs
→ Defaulting to: docs/source/ (guides)
→ Consider adding to .vibesafe/documentation.yml
```

## Testing Strategy

### Unit Tests (add to `tests/test_whats_next.py`)

```python
class TestDocumentationSpecIntegration(unittest.TestCase):
    def test_load_documentation_spec_valid(self):
        """Test loading valid documentation specification"""
        
    def test_load_documentation_spec_missing(self):
        """Test graceful handling of missing specification"""
        
    def test_load_documentation_spec_invalid_yaml(self):
        """Test error handling for invalid YAML"""
        
    def test_detect_cip_type_from_tags(self):
        """Test CIP type detection from frontmatter tags"""
        
    def test_detect_cip_type_from_title(self):
        """Test CIP type detection from title keywords"""
        
    def test_detect_cip_type_fallback(self):
        """Test fallback to 'guides' when type unclear"""
        
    def test_get_compression_target_with_spec(self):
        """Test target suggestion with specification present"""
        
    def test_get_compression_target_without_spec(self):
        """Test target suggestion without specification (fallback)"""
        
    def test_compression_suggestions_grouped_by_target(self):
        """Test that compression suggestions group CIPs by target"""
```

### Integration Tests

```bash
# Test with valid specification
cp fixtures/documentation.yml .vibesafe/
./whats-next --compression-check
# Verify specific targets are shown

# Test without specification
rm .vibesafe/documentation.yml
./whats-next --compression-check
# Verify generic suggestions are shown

# Test with invalid YAML
echo "invalid: yaml: syntax:" > .vibesafe/documentation.yml
./whats-next --compression-check
# Verify error handling and fallback
```

## Related

- **REQ-000F**: Documentation Structure Specification (this implements Triggers 1, 4, 5, 6)
- **CIP-0013**: Documentation Compression Stage (compression workflow)
- **Backlog**: 2026-01-08_migrate-docs-to-sphinx.md (created the specification)
- **File**: `.vibesafe/documentation.yml` (created 2026-01-08)

## Progress Updates

### 2026-01-08
Task created with "Proposed" status, High priority.

**Discovery**: While implementing REQ-000F, we created `.vibesafe/documentation.yml` but didn't integrate it with `whats-next.py` or compression tools. This means:
- ✅ Specification exists and documents VibeSafe's structure
- ❌ Specification isn't being used yet
- ❌ REQ-000F Trigger 4 not implemented

**Why High Priority**:
- Makes REQ-000F actually useful (not just documentation)
- Directly improves compression workflow UX
- Provides actionable, specific guidance
- Prevents users from guessing where to compress CIPs

**Dependencies**:
- Requires completion of 2026-01-08_migrate-docs-to-sphinx (creates `.vibesafe/documentation.yml`)

## Benefits

- **Actionable guidance**: Users know exactly where to compress
- **Consistency**: Enforces documented structure
- **Reduced friction**: No guessing about target locations
- **REQ-000F compliance**: Specification is actually used
- **Better UX**: Specific suggestions > generic prompts
- **Quality**: Improves traceability and documentation organization

