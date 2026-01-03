---
id: "2025-07-26_vibesafe-auto-gitignore-protection"
title: "VibeSafe Auto-Gitignore Protection"
status: "Implemented"
priority: "High"
created: "2025-07-26"
last_updated: "2026-01-03"
related_requirements:
  - "000A"
---

# CIP-000F: VibeSafe Auto-Gitignore Protection

## Status
*Implemented* - Phase 1 completed (2025-07-26), Phase 2/3 documentation deferred

## Description

Implements REQ-000A (Minimal Version Control Footprint) by automatically protecting VibeSafe system files through `.gitignore` entries during installation. This enhancement enables users to safely use generic git operations (like `git add .`) without accidentally committing VibeSafe infrastructure files.

Extends the Clean Installation Philosophy (CIP-000E) with automatic version control protection.

## Motivation

### Current Problem
The Clean Installation Philosophy distinguishes between VibeSafe system files (templates, scripts, cursor rules) and user content (actual tasks, CIPs). However, users must manually avoid committing system files using "surgical git add" operations:

```bash
# Current requirement - cognitive burden
git add backlog/features/my-task.md          # ✅ User content  
git add cip/cip0001.md                      # ✅ User content
# Never: git add backlog/README.md          # ❌ System file
# Never: git add .cursor/rules/             # ❌ System files
```

### Benefits of Auto-Protection
1. *🔒 Automatic Safety*: Impossible to accidentally commit system files
2. *🚀 Simplified Workflow*: Users can safely use `git add .` and standard workflows
3. *📋 Enforced Classification*: Built-in distinction between system vs user files
4. *🧠 Reduced Cognitive Load*: No need to remember file classification rules
5. *🎯 Better Developer Experience*: Focus on work, not git mechanics

## Implementation

### Phase 1: Core Protection System

*1. Create VibeSafe .gitignore Template*
```
# VibeSafe System Files (Auto-added during installation)
# These are VibeSafe infrastructure - not your project content

# Backlog system files
backlog/README.md
backlog/task_template.md
backlog/update_index.py
backlog/index.md

# CIP system files  
cip/README.md
cip/cip_template.md

# Cursor AI rules (VibeSafe-managed)
.cursor/rules/
# Generated project tenet cursor rules
.cursor/rules/project_tenet_*.mdc

# VibeSafe scripts and tools
scripts/whats_next.py
install-whats-next.sh
whats-next

# VibeSafe templates directory
templates/

# AI-Requirements framework (VibeSafe-managed)
ai-requirements/README.md
ai-requirements/requirement_template.md
ai-requirements/prompts/
ai-requirements/patterns/
ai-requirements/integrations/
ai-requirements/examples/
ai-requirements/guidance/

# Tenets system files
tenets/README.md
tenets/tenet_template.md
tenets/combine_tenets.py

# VibeSafe documentation (system files)
docs/whats_next_script.md
docs/yaml_frontmatter_examples.md
```

*2. Update Installation Script*
- Modify `scripts/install-minimal.sh` to append VibeSafe gitignore entries
- Handle existing .gitignore files gracefully (merge, don't overwrite)
- Add section headers and comments for clarity

*3. ~~Update vibesafe-update Script~~ (superseded by CIP-000E)*
- ~~Add gitignore management as a new component~~ (no longer needed)
- ~~Allow checking/updating gitignore entries~~ (install-minimal.sh handles this)

### Phase 2: Documentation and Workflow Updates

*1. Update Cursor Rules*
- Modify `vibesafe_general.mdc` to remove "surgical git add" warnings
- Add new guidance about safe generic git operations
- Update file classification sections

*2. Update CIP-000E*
- Add reference to Auto-Gitignore Protection
- Update implementation status

*3. Update Installation Documentation*
- Revise README.md installation instructions
- Remove surgical git add warnings from documentation

### Phase 3: Edge Case Handling

*1. Virtual Environment Handling*
- User's `.venv` is preserved (user content) and typically in user's .gitignore
- VibeSafe's `.venv-vibesafe` is auto-managed (system file) and in VibeSafe gitignore section
- Clear separation avoids conflicts between user and VibeSafe dependencies

*2. Conflict Resolution*
- Handle cases where user has custom .gitignore entries that conflict
- Provide clear messaging about what's being added

*3. Upgrade Path*
- Ensure existing VibeSafe installations get gitignore protection
- Provide migration instructions

## Implementation Status

### Phase 1: Core Protection System ✅ COMPLETED 2025-07-26
- [x] Create VibeSafe gitignore template (in `get_vibesafe_gitignore_entries()`)
- [x] Update `install-minimal.sh` with gitignore management (`add_vibesafe_gitignore()`)
- [x] ~~Update `vibesafe-update` script~~ (superseded by CIP-000E)
- [x] Implement idempotent updates (check existing section, add only missing entries)
- [x] Implement coverage checking (`check_gitignore_coverage()`)
- [x] Test installation with existing .gitignore files (works)
- [x] Test installation without existing .gitignore files (works)
- [x] Handle dogfood installs specially (templates/ not ignored for VibeSafe itself)
- [x] Handle .venv contradiction (resolved with .venv-vibesafe in bug 2026-01-03)
- [x] Test upgrade path for existing installations (idempotent, safe to rerun)

### Phase 2 & 3: Documentation Updates - DEFERRED
These are documentation updates that would be nice but aren't blocking functionality:
- [ ] Update Cursor rules to remove surgical git warnings (still recommend surgical adds)
- [ ] Update CIP-000E to reference this enhancement
- [ ] Update README.md installation documentation
- [ ] Create explicit tests for gitignore management (currently manual testing)

## Technical Considerations

### Gitignore Management Strategy
1. *Non-destructive*: Never overwrite existing .gitignore content
2. *Idempotent*: Safe to run multiple times
3. *Sectioned*: Clear VibeSafe section with headers
4. *Reversible*: Ability to remove VibeSafe entries if needed

### Implementation Details
```bash
# In install-minimal.sh
add_vibesafe_gitignore() {
    local gitignore_file=".gitignore"
    local vibesafe_section="# VibeSafe System Files"
    
    # Check if VibeSafe section already exists
    if ! grep -q "$vibesafe_section" "$gitignore_file" 2>/dev/null; then
        echo "Adding VibeSafe gitignore protection..."
        cat >> "$gitignore_file" << 'EOF'

# VibeSafe System Files (Auto-added during installation)
# These are VibeSafe infrastructure - not your project content
[... entries ...]
EOF
    fi
}
```

## Supersedes

This CIP extends CIP-000E (Clean Installation Philosophy) and will modify:
- VibeSafe General Development Guidelines (less restrictive git operations)
- Installation documentation (simplified workflow)
- User experience (from "surgical" to "automatic" protection)

## References

- REQ-000A: Minimal Version Control Footprint (WHAT this achieves)
- CIP-000E: Clean Installation Philosophy (related HOW)
- VibeSafe General Development Guidelines (`.cursor/rules/vibesafe_general.mdc`)
- VibeSafe Installation Script (`scripts/install-minimal.sh`)

## Implementation Notes (2026-01-03)

**Phase 1 is complete and working:**
- The gitignore protection is fully functional in `install-minimal.sh`
- Users can safely use `git add .` without committing VibeSafe system files
- The implementation is idempotent and handles edge cases (dogfooding, existing files)
- REQ-000A acceptance criteria are all met

**Phase 2 & 3 (documentation) are deferred:**
- The actual behavior works as designed
- The documentation (cursor rules, README) still recommend "surgical git add"
- This is conservative/safe but not strictly necessary anymore
- Could be updated in future but not blocking

**Relationship with REQ-000A:**
- REQ-000A was created retroactively (2026-01-03) to document the requirement this CIP fulfills
- This CIP was implemented first (2025-07-26), requirement documented later
- Normal flow would be: Requirement → CIP → Implementation
- This case: Implementation → CIP documentation → Requirement documentation (reverse engineering)

## Author and Date

*Author*: Neil Lawrence
*Created*: 2025-07-26  
*Last Updated*: 2026-01-03 