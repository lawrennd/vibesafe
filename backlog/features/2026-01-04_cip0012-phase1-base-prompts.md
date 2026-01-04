---
id: "2026-01-04_cip0012-phase1-base-prompts"
title: "CIP-0012 Phase 1: Base Prompts Infrastructure"
status: "Ready"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "features"
related_cips: ["0012"]
owner: ""
dependencies: []
tags: ["framework-independence", "ai-assistants", "prompts"]
---

# Task: CIP-0012 Phase 1: Base Prompts Infrastructure

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 1 of CIP-0012 (AI Assistant Framework Independence).

## Description

Create the base prompts infrastructure that will serve as the platform-agnostic source of truth for AI context files. Move existing `.cursor/rules/*.mdc` content to generic markdown prompts in `templates/prompts/`, stripping platform-specific metadata.

## Acceptance Criteria

- [ ] Research and document platform-specific discovery paths
  - [ ] Cursor: `.cursor/rules/` (verified)
  - [ ] GitHub Copilot: `.github/copilot/prompts/` (verify correct path)
  - [ ] Claude Code: `.claude/context/` (verify correct path or research)
  - [ ] Codex: Research discovery path and format requirements
  - [ ] Document findings in CIP-0012 or implementation notes
- [ ] Create `templates/prompts/` directory structure
- [ ] Convert existing cursor rules to base prompts:
  - [ ] `backlog.md` (strip YAML frontmatter, keep markdown content)
  - [ ] `cip.md` (strip YAML frontmatter)
  - [ ] `requirements.md` (strip YAML frontmatter)
  - [ ] `vibesafe_general.md`
  - [ ] `vibesafe_update.md`
  - [ ] `whats_next.md`
- [ ] Create platform adapter function stubs in `install-minimal.sh`:
  - [ ] `generate_prompts_for_platform()` dispatcher function
  - [ ] `generate_cursor_rules()` stub
  - [ ] `generate_copilot_prompts()` stub
  - [ ] `generate_claude_context()` stub
  - [ ] `generate_codex_context()` stub
  - [ ] `generate_generic_context()` stub

## Implementation Notes

**Key Principle**: Separate content from delivery format. Base prompts should be pure markdown with clear section headers, no platform-specific metadata.

**Discovery Path Research**:
- Test file discovery on each platform if possible
- Check official documentation for recommended paths
- Community feedback on what works

**Backward Compatibility**: Keep existing `.cursor/rules/` generation working during transition.

## Progress Updates

### 2026-01-04
Task created. CIP-0012 accepted and ready for implementation.

