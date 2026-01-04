---
id: "2026-01-04_cip0012-phase3-documentation"
title: "CIP-0012 Phase 3: Documentation Update"
status: "Proposed"
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

- [x] Add "Framework Independence" section to README.md ← Already done!
- [ ] Update all base prompts in `templates/prompts/` to be platform-neutral:
  - [ ] Remove references to "Cursor rules" → "AI context" or "AI prompts"
  - [ ] Add note that content works with all AI assistants
  - [ ] Mention platform-specific discovery as transparent detail
- [ ] Update installation documentation:
  - [ ] Explain `VIBESAFE_PLATFORM` environment variable
  - [ ] Document default behavior (all platforms)
  - [ ] Show examples for single-platform installs
- [ ] Create platform-specific setup guides (optional):
  - [ ] `docs/setup-cursor.md`
  - [ ] `docs/setup-claude-code.md`
  - [ ] `docs/setup-copilot.md`
- [ ] Update gitignore patterns if needed:
  - [ ] `.github/copilot/prompts/` (system files)
  - [ ] `.claude/context/` (system files)
  - [ ] `.ai/context/` (system files)

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

