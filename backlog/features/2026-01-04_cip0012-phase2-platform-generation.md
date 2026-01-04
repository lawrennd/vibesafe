---
id: "2026-01-04_cip0012-phase2-platform-generation"
title: "CIP-0012 Phase 2: Platform Generation Logic"
status: "In Progress"
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
  - [ ] Generate single combined file: `.github/copilot-instructions.md`
  - [ ] Plain markdown (no special frontmatter needed)
  - [ ] Optionally: Generate path-specific `.github/instructions/*.instructions.md` files
  - [ ] Consider: Separate prompt files in `.github/prompts/*.prompt.md` (on-demand)
- [ ] Implement `generate_claude_context()` function:
  - [ ] Generate project memory: `CLAUDE.md` (root level)
  - [ ] Plain markdown with sections (no special frontmatter)
  - [ ] Alternative: `.claude/CLAUDE.md` (if we want namespacing)
  - [ ] Optionally: Generate slash commands in `.claude/commands/*.md`
- [ ] Implement `generate_codex_context()` function:
  - [ ] Generate project doc: `AGENTS.md` (root level)
  - [ ] Alternative: `codex.md` (root level)
  - [ ] Plain markdown (no special frontmatter)
  - [ ] Note: User-level `~/.codex/instructions.md` managed separately
- [ ] Consider generic fallback (optional):
  - [ ] May not be needed - each platform has specific paths
  - [ ] Could implement `.ai/context/` if community requests it
  - [ ] For now: Focus on the 4 major platforms with known paths
- [ ] Add platform detection/selection:
  - [ ] Support `VIBESAFE_PLATFORM` environment variable
  - [ ] Options: `cursor`, `copilot`, `claude`, `codex`, `all` (default)
  - [ ] Document in README
- [ ] Update `combine_tenets.py`:
  - [ ] Rename `--generate-cursor-rules` → `--generate-prompts`
  - [ ] Add `--platform` flag
  - [ ] Output to `templates/prompts/` (base format)
- [ ] Refactor `generate_tenet_cursor_rules()` in `install-minimal.sh`:
  - [ ] Rename to `generate_tenet_ai_prompts()` (platform-neutral)
  - [ ] Call new platform adapters instead of direct Cursor generation
  - [ ] Support VIBESAFE_PLATFORM environment variable

## Implementation Notes

**Platform Format Examples**:

**Cursor** (`.cursor/rules/backlog.mdc`):
```markdown
---
description: VibeSafe Backlog System
globs: backlog/**/*.md
alwaysApply: true
---
# VibeSafe Project Backlog System
[content...]
```

**Copilot** (`.github/copilot-instructions.md`):
```markdown
# VibeSafe Project Guidelines
## Backlog System
[content...]
## CIP Process
[content...]
[combined content, no frontmatter]
```

**Claude Code** (`CLAUDE.md`):
```markdown
# VibeSafe Project Memory
## Backlog System
[content...]
## CIP Process
[content...]
[combined content, plain markdown]
```

**Codex** (`AGENTS.md`):
```markdown
# VibeSafe Project Documentation
## Backlog System
[content...]
## CIP Process
[content...]
[combined content, plain markdown]
```

**Default Behavior**: Generate for ALL platforms by default (only a few KB, respects user autonomy).

**Testing**: Verify generated files are identical in content, just different formats.

## Progress Updates

### 2026-01-04
Task created. Depends on Phase 1 completion (base prompts infrastructure).

**Platform Research Applied**: Based on official documentation:
- **Cursor**: Multi-file directory (`.cursor/rules/*.mdc`) with YAML frontmatter
- **Copilot**: Single combined file (`.github/copilot-instructions.md`), plain markdown
- **Claude Code**: Single memory file (`CLAUDE.md`), plain markdown
- **Codex**: Single doc file (`AGENTS.md` or `codex.md`), plain markdown

**Key Decision**: Cursor gets multiple files (matches its pattern), other platforms get single combined files (matches their patterns).

