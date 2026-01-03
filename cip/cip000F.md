---
id: "2025-07-26_vibesafe-auto-gitignore-protection"
title: "VibeSafe Auto-Gitignore Protection"
status: "Proposed"
priority: "High"
created: "2025-07-26"
last_updated: "2025-07-26"
---

# CIP-000F: VibeSafe Auto-Gitignore Protection

## Status
*Implemented* - Phase 1 completed, auto-gitignore protection active

## Description

Extend the Clean Installation Philosophy (CIP-000E) by automatically protecting VibeSafe system files through `.gitignore` entries during installation. This enhancement enables users to safely use generic git operations (like `git add .`) without accidentally committing VibeSafe infrastructure files.

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

- [ ] Create VibeSafe gitignore template
- [ ] Update `install-minimal.sh` with gitignore management
- [x] ~~Update `vibesafe-update` script~~ (superseded by CIP-000E)
- [ ] Test installation with existing .gitignore files
- [ ] Test installation without existing .gitignore files
- [ ] Update Cursor rules to remove surgical git warnings
- [ ] Update CIP-000E to reference this enhancement
- [ ] Update README.md installation documentation
- [ ] Create tests for gitignore management
- [x] Handle .venv contradiction (resolved with .venv-vibesafe in bug 2026-01-03)
- [ ] Test upgrade path for existing installations

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

- CIP-000E: Clean Installation Philosophy
- VibeSafe General Development Guidelines (`.cursor/rules/vibesafe_general.mdc`)
- VibeSafe Installation Script (`scripts/install-minimal.sh`)

## Author and Date

*Author*: Neil Lawrence
*Created*: 2025-07-26  
*Last Updated*: 2025-07-26 