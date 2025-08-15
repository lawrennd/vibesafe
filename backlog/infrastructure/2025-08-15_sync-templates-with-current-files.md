---
id: "sync-templates-with-current-files"
title: "Implement VibeSafe self-update workflow to prevent template drift"
status: "Ready"
priority: "High"
created: "2025-08-15"
last_updated: "2025-08-15"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ""
tags:
- templates
- installation
- maintenance
- system-files
- self-update
---

# Task: Implement VibeSafe self-update workflow to prevent template drift

## Description

The VibeSafe templates directory contains outdated versions of system files that are being installed by the `install-minimal.sh` script. This causes new installations to get old versions of files like `update_index.py` that don't support YAML frontmatter. We need to implement a comprehensive workflow that prevents this drift and allows VibeSafe to self-update.

## Problem

- `templates/backlog/update_index.py` is from May 5th (8027 bytes) but current version is from July 28th (10676 bytes)
- `templates/tenets/combine_tenets.py` is from May 5th (2490 bytes) but current version is from July 28th (6947 bytes)
- `templates/scripts/whats_next.py` doesn't exist but should be copied from current version
- Other template files may also be outdated
- No systematic process to keep templates in sync with current files
- Risk of this happening again with future updates

## Root Cause Analysis

The fundamental issue is that VibeSafe development happens in the main directories (backlog/, scripts/, etc.) but the install script copies from templates/. There's no automated process to keep these in sync, leading to template drift.

## Impact

- New VibeSafe installations get outdated system files
- Users experience issues like YAML frontmatter not being parsed correctly
- Inconsistent behavior between development and installed versions
- Manual maintenance burden for keeping templates current
- Risk of breaking installations with new features

## Proposed Solution: Self-Update Workflow

### 1. Template-First Development
- All system files should be developed in the templates directory first
- Templates become the source of truth for system files
- Development workflow: templates → test → commit

### 2. VibeSafe Self-Update Capability
- Modify `.gitignore` to exclude installed system files from VibeSafe's own repository
- VibeSafe should always install from templates, even in its own directory
- Add `vibesafe self-update` command to refresh system files

### 3. Automated Template Sync
- Create a maintenance script that can sync templates with current files
- Add pre-commit hooks to ensure templates are current
- Implement CI/CD checks to detect template drift

## Acceptance Criteria

### Phase 1: Immediate Fix
- [ ] Identify all outdated files in templates directory
- [ ] Copy current versions of system files to templates directory
- [ ] Verify file sizes and dates are updated
- [ ] Test that install-minimal.sh installs current versions

### Phase 2: Self-Update Implementation
- [ ] Modify VibeSafe's `.gitignore` to exclude installed system files
- [ ] Update install-minimal.sh to always install from templates (even in VibeSafe itself)
- [ ] Create `vibesafe self-update` command
- [ ] Test self-update workflow in VibeSafe repository

### Phase 3: Template-First Workflow
- [ ] Document template-first development process
- [ ] Create maintenance script for template sync
- [ ] Add pre-commit hooks for template validation
- [ ] Update development documentation

### Phase 4: Automation
- [ ] Implement CI/CD checks for template drift
- [ ] Create automated testing for template installation
- [ ] Document maintenance procedures

## Implementation Notes

### Template-First Development Process
1. Make changes to files in templates/ directory
2. Test changes by running install-minimal.sh in a test project
3. Commit template changes
4. Use self-update to refresh VibeSafe's own installation

### Self-Update Command Design
```bash
vibesafe self-update [--force] [--dry-run]
```
- Always installs from templates directory
- Can be run in any VibeSafe-managed project
- --force to overwrite local modifications
- --dry-run to preview changes

### .gitignore Strategy
- Exclude all system files that are installed from templates
- Keep templates/ directory in version control
- Allow user content (backlog items, CIPs, tenets) to be committed

## Related

- VibeSafe installation process
- YAML frontmatter support in update_index.py
- System file maintenance
- Development workflow improvements
- CI/CD automation

## Progress Updates

### 2025-08-15
Task created with Ready status after discovering outdated templates during GPy integration. Expanded scope to address root cause and prevent future drift.
