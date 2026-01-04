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

- [x] Research and document platform-specific discovery paths ← RESEARCH COMPLETE!
  - [x] **Cursor**: `.cursor/rules/*.mdc` (confirmed working)
    - Uses Cursor-specific Markdown format with YAML frontmatter
    - Legacy: `.cursorrules` (single file, older mechanism)
  - [x] **GitHub Copilot**: Multiple instruction paths
    - Repository-wide: `.github/copilot-instructions.md`
    - Path-specific: `.github/instructions/*.instructions.md` (with `applyTo` globs)
    - Prompt files: `.github/prompts/*.prompt.md` (on-demand via `/...`)
  - [x] **Claude Code**: Memory + slash commands
    - Project memory: `CLAUDE.md` OR `.claude/CLAUDE.md`
    - Slash commands: `.claude/commands/*.md`
    - User config: `~/.claude.json`
  - [x] **Codex CLI**: Multi-layer instructions
    - User config: `~/.codex/config.yaml`
    - Global instructions: `~/.codex/instructions.md`
    - Project docs: `codex.md` OR `AGENTS.md`
    - Override via: `experimental_instructions_file=<path>` config flag
- [ ] Create `templates/prompts/` directory structure (per composition strategy):
  - [ ] `templates/prompts/always-apply/` (general, update, whats-next)
  - [ ] `templates/prompts/context-specific/` (backlog, cip, requirements)
- [ ] Convert existing cursor rules to base prompts:
  - [ ] `always-apply/vibesafe_general.md` (strip YAML, keep markdown)
  - [ ] `always-apply/vibesafe_update.md` (strip YAML)
  - [ ] `always-apply/whats_next.md` (strip YAML)
  - [ ] `context-specific/backlog.md` (strip YAML)
  - [ ] `context-specific/cip.md` (strip YAML)
  - [ ] `context-specific/requirements.md` (strip YAML)
- [ ] Create platform adapter function stubs in `install-minimal.sh`:
  - [ ] `generate_prompts_for_platform()` dispatcher function
  - [ ] `generate_cursor_rules()` stub
  - [ ] `generate_copilot_prompts()` stub
  - [ ] `generate_claude_context()` stub
  - [ ] `generate_codex_context()` stub
  - [ ] `generate_generic_context()` stub

## Implementation Notes

**Key Principle**: Separate content from delivery format. Base prompts should be pure markdown with clear section headers, no platform-specific metadata.

**Discovery Path Research** ✅ COMPLETE:

Platform-specific paths (based on official docs):
1. **Cursor**: `.cursor/rules/*.mdc` (+ legacy `.cursorrules`)
2. **Copilot**: `.github/copilot-instructions.md` (repo-wide)
3. **Claude Code**: `CLAUDE.md` or `.claude/CLAUDE.md` (project memory)
4. **Codex**: `codex.md` or `AGENTS.md` (project docs)

**Key Insight**: Each platform has different discovery patterns:
- Cursor: Multi-file directory (`.cursor/rules/`)
- Copilot: GitHub-namespaced directory (`.github/...`)
- Claude: Single project file (`CLAUDE.md`) + commands directory
- Codex: Project doc file (`codex.md` or `AGENTS.md`)

**Implementation Strategy**:
For VibeSafe, generate multiple files per platform to match their patterns:
- Cursor: Generate separate `.mdc` files (backlog.mdc, cip.mdc, etc.)
- Copilot: Generate single `.github/copilot-instructions.md` (combined)
- Claude: Generate single `CLAUDE.md` (combined) OR separate command files
- Codex: Generate single `AGENTS.md` (combined)

**Backward Compatibility**: Keep existing `.cursor/rules/` generation working during transition.

## Progress Updates

### 2026-01-04
Task created. CIP-0012 accepted and ready for implementation.

**Platform Research Completed**: Documented official discovery paths for all 4 platforms:
- Cursor: `.cursor/rules/*.mdc`
- Copilot: `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md`
- Claude Code: `CLAUDE.md` / `.claude/CLAUDE.md` + `.claude/commands/*.md`
- Codex: `codex.md` / `AGENTS.md` + `~/.codex/instructions.md`

Ready to proceed with base prompts creation and platform adapter implementation.

**Composition Strategy Defined**: Created design doc `cip/cip0012-prompt-composition-strategy.md` defining:
- **Option 3 (Hybrid)** recommended: Use each platform's capabilities fully
- **Base structure**: `always-apply/` vs `context-specific/`
- **Platform mapping**: Multi-file for Cursor, path-specific for Copilot, commands for Claude, combined for Codex
- **Key insight**: VibeSafe already uses path-specific prompts (globs in frontmatter)!

See design doc for complete implementation mapping.

