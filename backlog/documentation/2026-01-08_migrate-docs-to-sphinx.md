---
id: "2026-01-08_migrate-docs-to-sphinx"
title: "Migrate Documentation to Consistent Sphinx Structure"
status: "Proposed"
priority: "High"
created: "2026-01-08"
last_updated: "2026-01-08"
category: "documentation"
related_cips: ["0013"]
related_requirements: ["000F"]
owner: ""
dependencies: []
tags: ["documentation", "sphinx", "structure", "migration", "compression"]
---

# Task: Migrate Documentation to Consistent Sphinx Structure

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task fixes documentation drift and implements REQ-000F (Documentation Structure Specification).

## Description

VibeSafe has documentation drift. We started with Sphinx (`docs/source/conf.py` exists), but recent documentation has been created as plain markdown files directly in `docs/` instead of following the Sphinx structure. This violates REQ-000F (documentation should have an explicit, documented structure).

**Current State** (Inconsistent):
```
docs/
├── source/                    # Sphinx structure ✅
│   ├── conf.py
│   ├── index.rst
│   ├── getting_started.md
│   └── whats_next_script.md
├── compression-guide.md       # ❌ Should be in source/
├── whats_next_script.md       # ❌ Should be in source/ or duplicate?
├── yaml_frontmatter_*.md      # ❌ Should be in source/
└── patterns/                  # ❓ Should this be in source/?
```

**Why this matters**: 
- Sphinx won't build these orphaned markdown files
- Inconsistent structure confuses contributors
- Compression guide won't appear in built documentation
- Violates REQ-000F (undocumented documentation structure)
- Makes it unclear where new docs should go

## Acceptance Criteria

### Phase 1: Migrate Existing Documentation
- [ ] Move `docs/compression-guide.md` → `docs/source/compression-guide.md`
- [ ] Check if `docs/whats_next_script.md` duplicates `docs/source/whats_next_script.md`
  - [ ] If duplicate: Delete `docs/whats_next_script.md`, keep `docs/source/` version
  - [ ] If different: Merge and keep in `docs/source/`
- [ ] Move `docs/yaml_frontmatter_examples.md` → `docs/source/yaml_frontmatter_examples.md`
- [ ] Move `docs/yaml_frontmatter_schema.md` → `docs/source/yaml_frontmatter_schema.md`
- [ ] Evaluate `docs/patterns/` - should it be `docs/source/patterns/`?

### Phase 2: Update Sphinx Index
- [ ] Add compression-guide to `docs/source/index.rst` table of contents
- [ ] Add yaml_frontmatter docs to index if appropriate
- [ ] Ensure all moved docs are discoverable in Sphinx navigation

### Phase 3: Fix All Traceability Links
- [ ] Update `README.md` link: `docs/compression-guide.md` → `docs/source/compression-guide.md`
- [ ] Update `docs/source/whats_next_script.md` internal links (if affected)
- [ ] Search for any other links to moved files: `grep -r "docs/compression-guide.md" .`
- [ ] Test all links work after migration

### Phase 4: Document the Documentation Structure (REQ-000F)
- [ ] Create `.vibesafe/documentation.yml` specification:
  ```yaml
  documentation:
    system: "sphinx"
    source_dir: "docs/source"
    build_dir: "docs/_build"
    format: "markdown"  # or "rst" if we convert
    targets:
      infrastructure: "docs/source/architecture.md"
      feature: "docs/source/features.md"
      process: "docs/source/workflow.md"
      guides: "docs/source/"
    compression_guide: "docs/source/compression-guide.md"
  ```
- [ ] Update compression guide to reference this specification
- [ ] Update `docs/source/index.rst` to document structure

### Phase 5: Build and Verify
- [ ] Run Sphinx build: `cd docs && make html`
- [ ] Verify all migrated docs appear in built documentation
- [ ] Check that compression-guide is accessible
- [ ] Fix any broken internal links in built docs

### Phase 6: Update Compression Workflow
- [ ] Update `docs/source/compression-guide.md` to reflect Sphinx structure
- [ ] Update examples to use `docs/source/` paths
- [ ] Add note about documentation specification in compression guide

## Implementation Notes

### Detecting Documentation Drift

**Root cause**: During CIP-0013 implementation, we created `docs/compression-guide.md` directly without checking the existing Sphinx structure. This happened because:
1. No explicit documentation specification (REQ-000F not yet implemented)
2. Followed "plain markdown" pattern seen in some docs
3. Didn't verify Sphinx setup before creating new docs

**Prevention**: Once REQ-000F is implemented, the specification will make it obvious where docs belong.

### Migration Strategy

**Option 1: Move files (preferred)**
- Preserves git history with `git mv`
- Maintains existing content
- Updates links to new locations

**Option 2: Convert to RST (more work)**
- Convert `.md` to `.rst` for true Sphinx integration
- Better long-term if we want Sphinx features (cross-refs, autodoc)
- More disruptive, requires link format changes

**Recommendation**: Start with Option 1 (move), consider Option 2 later if needed.

### Sphinx Build Commands

```bash
# Build HTML documentation
cd docs
make html

# View built docs
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux

# Clean build (if problems)
make clean
make html
```

### File Comparison

Check if `docs/whats_next_script.md` and `docs/source/whats_next_script.md` are duplicates:

```bash
diff docs/whats_next_script.md docs/source/whats_next_script.md
# If identical: delete docs/whats_next_script.md
# If different: merge and keep in docs/source/
```

### Link Update Strategy

Search for all references to moved files:

```bash
# Find all markdown links to compression-guide
grep -r "docs/compression-guide.md" .

# Find all markdown links to whats_next_script
grep -r "docs/whats_next_script.md" .

# Check relative links in moved files
grep -r "\.\./" docs/source/compression-guide.md
```

## Testing Strategy

### Before Migration
1. Document current state: `ls -R docs/ > before.txt`
2. Save list of all links: `grep -r "docs/" . --include="*.md" > links-before.txt`

### After Migration
1. Compare structure: `ls -R docs/ > after.txt && diff before.txt after.txt`
2. Verify no broken links: Build docs and check for warnings
3. Test compression workflow still works with new paths

### Validation Checklist
- [ ] `make html` completes without errors
- [ ] All migrated docs appear in `_build/html/`
- [ ] Compression guide is accessible via Sphinx navigation
- [ ] All README.md links work
- [ ] All internal doc links work
- [ ] Git history preserved for moved files

## Related

- **REQ-000F**: Documentation Structure Specification (the requirement driving this)
- **CIP-0013**: Documentation Compression Stage (created compression-guide.md)
- **Sphinx docs**: `docs/source/` (the correct location)
- **Drift**: `docs/*.md` files outside Sphinx structure

## Progress Updates

### 2026-01-08
Task created with "Proposed" status, High priority.

**Discovery**: During CIP-0013 compression, we created `docs/compression-guide.md` directly in `docs/` without realizing VibeSafe uses Sphinx (`docs/source/conf.py` exists). This created inconsistent structure.

**Why High Priority**: 
- Affects how future CIPs are compressed
- Compression guide won't build with Sphinx
- No clear documentation structure (violates REQ-000F)
- Confuses contributors about where docs belong

**Root Cause**: REQ-000F (Documentation Structure Specification) exists but wasn't implemented yet. Without explicit specification, it wasn't obvious VibeSafe uses Sphinx.

**Fix**: Migrate docs to Sphinx structure AND implement REQ-000F to prevent future drift.

## Benefits

- **Consistency**: All docs in one structure (Sphinx)
- **Discoverability**: Sphinx navigation makes docs easy to find
- **Build quality**: Sphinx features (search, theming, cross-refs)
- **REQ-000F compliance**: Explicit documentation specification
- **Prevents drift**: Clear structure documented going forward
- **Compression clarity**: Compression guide properly integrated

