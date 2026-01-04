---
id: "2026-01-04_cip0012-phase3-documentation"
title: "CIP-0012 Phase 3: Documentation Update"
status: "Completed"
priority: "Medium"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "documentation"
related_cips: ["0012"]
owner: ""
dependencies: ["2026-01-04_cip0012-phase2-platform-generation"]
tags: ["framework-independence", "documentation"]
---

# Task: CIP-0012 Phase 3: Documentation Update

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> This task implements Phase 3 of CIP-0012 (AI Assistant Framework Independence).

## Description

Update all documentation to emphasize framework independence and provide platform-specific guidance where needed. Ensure base prompts are platform-neutral.

## Acceptance Criteria

- [x] Add "Framework Independence" section to README.md ← Done in Phase 2!
- [x] Update all base prompts in `templates/prompts/` to be platform-neutral:
  - [x] Remove references to "Cursor rules" → "AI context" or "AI prompts"
  - [x] Update file classification sections to list all platform files
  - [x] Keep platform names as examples (Cursor, Claude Code, Copilot, Codex)
- [x] Update installation documentation: ← Done in Phase 2!
  - [x] Explain `VIBESAFE_PLATFORM` environment variable
  - [x] Document default behavior (all platforms)
  - [x] Show examples for single-platform installs
- [ ] Create platform-specific setup guides (optional - deferred):
  - [ ] `docs/setup-cursor.md` (not blocking)
  - [ ] `docs/setup-codex.md` (not blocking)
  - [ ] `docs/setup-claude-code.md` (not blocking)
  - [ ] `docs/setup-copilot.md` (not blocking)
- [x] Update gitignore patterns:
  - [x] `.github/copilot-instructions.md` (system file)
  - [x] `CLAUDE.md` (system file)
  - [x] `AGENTS.md` (system file)
  - [x] Updated in `.gitignore` and `install-minimal.sh`

## Implementation Notes

**Platform-Neutral Language**:
- "AI context files" or "AI prompts" instead of "Cursor rules"
- "Works with Cursor, Claude Code, GitHub Copilot, and other AI assistants"
- Platform names as examples, not requirements

**Documentation Hierarchy**:
1. README: High-level framework independence statement
2. Base prompts: Platform-neutral content
3. Platform guides: Specific setup details (optional)

## Progress Updates

### 2026-01-04
Task created. README already updated in earlier session. Remaining work focuses on base prompts and optional platform guides.

### 2026-01-04 (later)
**Phase 3 COMPLETED!** ✅

All core acceptance criteria met:
1. ✅ README "Framework Independence" section already done in Phase 2
2. ✅ Updated all 6 base prompt files to be platform-neutral:
   - Changed "Cursor Rule" → "These guidelines"
   - Updated VibeSafe file classification sections to list all platforms
   - Listed: `.cursor/rules/*`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`
   - Files updated: vibesafe_general.md, backlog.md, cip.md, requirements.md, tenets.md
3. ✅ Installation docs already done in Phase 2 (VIBESAFE_PLATFORM examples)
4. ✅ Updated gitignore patterns:
   - Updated `.gitignore` file
   - Updated `get_vibesafe_gitignore_entries()` function in install-minimal.sh
   - Now protects: .github/copilot-instructions.md, CLAUDE.md, AGENTS.md

**Deferred items** (not blocking, can be added later):
- Platform-specific setup guides (docs/setup-*.md files)

**Result**: All VibeSafe documentation now emphasizes framework independence.  
No platform-specific language in base prompts. Platform names used only as examples.

**Ready for Phase 4**: Testing & Validation (final phase!)

