---
id: "2026-01-04_cip0012-phase2-platform-generation"
title: "CIP-0012 Phase 2: Platform Generation Logic"
status: "Completed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "features"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies: ["2026-01-04_cip0012-phase1-base-prompts"]
tags: ["framework-independence", "ai-assistants", "installation"]
---

# Task: CIP-0012 Phase 2: Platform Generation Logic

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 2 of CIP-0012 (AI Assistant Framework Independence).

## Description

Implement platform-specific generators that transform base prompts into the correct format for each AI assistant platform. Add platform detection/selection support via environment variables.

## Acceptance Criteria

- [x] Implement `generate_cursor_rules()` function:
  - [x] Add YAML frontmatter wrapper (description, globs, alwaysApply)
  - [x] Use `.mdc` extension
  - [x] Install to `.cursor/rules/`
- [x] Implement `generate_copilot_prompts()` function:
  - [x] Generate single combined file: `.github/copilot-instructions.md`
  - [x] Plain markdown (no special frontmatter needed)
  - [ ] Optionally: Generate path-specific `.github/instructions/*.instructions.md` files (deferred)
  - [ ] Consider: Separate prompt files in `.github/prompts/*.prompt.md` (on-demand) (deferred)
- [x] Implement `generate_claude_context()` function:
  - [x] Generate project memory: `CLAUDE.md` (root level)
  - [x] Plain markdown with sections (no special frontmatter)
  - [ ] Alternative: `.claude/CLAUDE.md` (if we want namespacing) (deferred)
  - [ ] Optionally: Generate slash commands in `.claude/commands/*.md` (deferred)
- [x] Implement `generate_codex_context()` function:
  - [x] Generate project doc: `AGENTS.md` (root level)
  - [x] Plain markdown (no special frontmatter)
  - [ ] Alternative: `codex.md` (root level) (deferred - AGENTS.md is standard)
  - [x] Note: User-level `~/.codex/instructions.md` managed separately
- [x] Consider generic fallback (optional):
  - [x] Decision: Not needed - each platform has specific paths
  - [x] Could implement `.ai/context/` if community requests it (deferred)
  - [x] For now: Focus on the 4 major platforms with known paths
- [x] Add platform detection/selection:
  - [x] Support `VIBESAFE_PLATFORM` environment variable
  - [x] Options: `cursor`, `copilot`, `claude`, `codex`, `all` (default)
  - [x] Document in README
- [x] Update `combine_tenets.py`:
  - [x] Rename `--generate-cursor-rules` → `--generate-prompts`
  - [x] Add `--platform` flag
  - [x] Keep backward compatibility with deprecated flag
- [x] Refactor `generate_tenet_cursor_rules()` in `install-minimal.sh`:
  - [x] Rename to `generate_tenet_ai_prompts()` (platform-neutral)
  - [x] Keep legacy wrapper for backward compatibility
  - [x] Support VIBESAFE_PLATFORM environment variable

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

### 2026-01-04 (later)
**Phase 2 COMPLETED!** ✅

All core acceptance criteria met:
1. ✅ Implemented all 4 platform generators (cursor, copilot, claude, codex)
2. ✅ Added VIBESAFE_PLATFORM environment variable support
3. ✅ Updated combine_tenets.py with --generate-prompts flag
4. ✅ Refactored generate_tenet_cursor_rules() → generate_tenet_ai_prompts()
5. ✅ Documented in README.md
6. ✅ Tested Cursor generator successfully
7. ✅ Maintained backward compatibility throughout

**Platform Generators Implemented**:
- `generate_cursor_rules()`: Generates .cursor/rules/*.mdc with YAML frontmatter
- `generate_copilot_prompts()`: Generates .github/copilot-instructions.md (combined)
- `generate_claude_context()`: Generates CLAUDE.md (combined)
- `generate_codex_context()`: Generates AGENTS.md (combined)

**Installation System Updated**:
- Respects VIBESAFE_PLATFORM env var (default: "all")
- Fallback to legacy cursor rules if base prompts missing
- Backward compatible with old installations

**Scripts Updated**:
- `combine_tenets.py`: New --generate-prompts flag, --platform option, deprecated --generate-cursor-rules with warning
- `install-minimal.sh`: Calls generate_tenet_ai_prompts() instead of generate_tenet_cursor_rules()

**Documentation**:
- README "Framework Independence" section expanded with platform details
- README "Advanced Usage" section includes VIBESAFE_PLATFORM examples

**Deferred items** (not blocking, can be added later):
- Path-specific Copilot instructions (.github/instructions/*.instructions.md)
- Claude slash commands (.claude/commands/*.md)
- Generic fallback (.ai/context/)

**Ready for Phase 3**: Documentation Update (update all cursor rule references)

