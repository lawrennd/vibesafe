---
id: "2026-01-04_cip0012-phase2-platform-generation"
title: "CIP-0012 Phase 2: Platform Generation Logic"
status: "Proposed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "features"
related_cips: ["0012"]
owner: ""
dependencies: ["2026-01-04_cip0012-phase1-base-prompts"]
tags: ["framework-independence", "ai-assistants", "installation"]
---

# Task: CIP-0012 Phase 2: Platform Generation Logic

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 2 of CIP-0012 (AI Assistant Framework Independence).

## Description

Implement platform-specific generators that transform base prompts into the correct format for each AI assistant platform. Add platform detection/selection support via environment variables.

## Acceptance Criteria

- [ ] Implement `generate_cursor_rules()` function:
  - [ ] Add YAML frontmatter wrapper (description, globs, alwaysApply)
  - [ ] Use `.mdc` extension
  - [ ] Install to `.cursor/rules/`
- [ ] Implement `generate_copilot_prompts()` function:
  - [ ] Use simpler format (verify what Copilot needs)
  - [ ] Use `.md` extension
  - [ ] Install to `.github/copilot/prompts/`
- [ ] Implement `generate_claude_context()` function:
  - [ ] Adapt format for Claude Code (research needed)
  - [ ] Install to `.claude/context/`
- [ ] Implement `generate_generic_context()` function:
  - [ ] Plain markdown files
  - [ ] Install to `.ai/context/` (if this path makes sense)
- [ ] Add platform detection/selection:
  - [ ] Support `VIBESAFE_PLATFORM` environment variable
  - [ ] Options: `cursor`, `copilot`, `claude`, `all` (default)
  - [ ] Document in README
- [ ] Update `combine_tenets.py`:
  - [ ] Rename `--generate-cursor-rules` → `--generate-prompts`
  - [ ] Add `--platform` flag
  - [ ] Output to `templates/prompts/` (base format)

## Implementation Notes

**Platform Frontmatter Examples**:
- **Cursor**: YAML with `description`, `globs`, `alwaysApply`
- **Copilot**: TBD (research needed)
- **Claude Code**: TBD (research needed)

**Default Behavior**: Generate for ALL platforms by default (only a few KB, respects user autonomy).

**Testing**: Verify generated files are identical in content, just different formats.

## Progress Updates

### 2026-01-04
Task created. Depends on Phase 1 completion (base prompts infrastructure).

