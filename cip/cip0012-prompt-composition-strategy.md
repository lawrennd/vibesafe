# CIP-0012: Prompt Composition Strategy

**Status**: Design Document (for Phase 1 implementation)  
**Date**: 2026-01-04  
**Purpose**: Define how VibeSafe prompts should be decomposed/composed for different AI platforms

---

## Current VibeSafe Prompt Structure (Cursor)

VibeSafe currently uses **path-specific prompts** with separate concerns:

| File | Scope | Application |
|------|-------|-------------|
| `backlog.mdc` | `globs: backlog/**/*.md` | Backlog-specific guidance |
| `cip.mdc` | `globs: cip/**/*.md` | CIP-specific guidance |
| `requirements_rule.mdc` | `globs: requirements/**/*.md` | Requirements-specific guidance |
| `vibesafe_general.mdc` | `globs: "**/*"` | Project-wide best practices |
| `vibesafe_update.mdc` | Likely general | Update/maintenance guidance |
| `whats_next.mdc` | Likely general | Project status tool guidance |

**Key Pattern**: Separate files for **separate concerns**, with **path-specific application** (globs).

---

## Platform Prompt Capabilities

Based on research, here's what each platform supports:

### Cursor
- ✅ **Multi-file directory**: `.cursor/rules/*.mdc`
- ✅ **Path-specific**: `globs: backlog/**/*.md`
- ✅ **Always applied**: `alwaysApply: true`
- **Best match**: Current structure works perfectly

### GitHub Copilot
- ✅ **Single repo-wide file**: `.github/copilot-instructions.md`
- ✅ **Path-specific files**: `.github/instructions/*.instructions.md` with `applyTo` frontmatter
- ⚠️ **On-demand prompts**: `.github/prompts/*.prompt.md` (invoked via `/...`)
- **Best match**: Can use path-specific instructions!

### Claude Code
- ✅ **Single project memory**: `CLAUDE.md`
- ✅ **Slash commands**: `.claude/commands/*.md` (on-demand)
- ❌ **No automatic path-specific**: Memory applies to whole project
- **Best match**: Single combined file OR separate slash commands

### Codex CLI
- ✅ **Single project doc**: `AGENTS.md` or `codex.md`
- ❌ **No automatic path-specific**: Applies to whole project
- **Best match**: Single combined file

---

## Composition Strategies (Options)

### Option 1: Maintain Separation (Recommended for Cursor + Copilot)

**Cursor**: Keep current structure (multi-file, path-specific)

**Copilot**: Use path-specific instructions
```
.github/instructions/
├── backlog.instructions.md     # applyTo: ["backlog/**/*.md"]
├── cip.instructions.md          # applyTo: ["cip/**/*.md"]
├── requirements.instructions.md # applyTo: ["requirements/**/*.md"]
└── general.instructions.md      # applyTo: ["**/*"]
```

**Claude Code**: Single combined file
```
CLAUDE.md  # All guidance in sections
```

**Codex**: Single combined file
```
AGENTS.md  # All guidance in sections
```

**Pros**:
- ✅ Maintains path-specific intelligence for platforms that support it
- ✅ Minimal loss of context specificity
- ✅ Copilot gets same precision as Cursor

**Cons**:
- ⚠️ Claude and Codex lose path-specific guidance
- ⚠️ More files to manage for Copilot

---

### Option 2: Always Combine (Simplest)

**All platforms except Cursor**: Single combined file

```
# For Copilot
.github/copilot-instructions.md  # All sections combined

# For Claude Code
CLAUDE.md  # All sections combined

# For Codex
AGENTS.md  # All sections combined
```

**Pros**:
- ✅ Simplest implementation
- ✅ Single file per platform (except Cursor)
- ✅ Easier to maintain

**Cons**:
- ❌ Loses path-specific context for Copilot (which supports it!)
- ❌ AI sees all guidance even when not relevant
- ❌ Doesn't use platform capabilities fully

---

### Option 3: Hybrid (Best of Both)

**Cursor**: Multi-file (current structure)

**Copilot**: Path-specific files (like Cursor, but Copilot format)

**Claude Code**: 
- `CLAUDE.md` (general + always-apply guidance)
- `.claude/commands/` (on-demand, topic-specific)

**Codex**: Single combined (no path-specific support)

**Pros**:
- ✅ Uses each platform's capabilities fully
- ✅ Path-specific where supported
- ✅ Combined where necessary

**Cons**:
- ⚠️ Most complex to implement
- ⚠️ Different structures per platform

---

## Recommendation: **Option 3 (Hybrid)**

### Rationale:

1. **Cursor** (70%+ of current users):
   - Keep current multi-file structure
   - Best user experience, already working

2. **Copilot** (supports path-specific):
   - Use `.github/instructions/*.instructions.md`
   - Maintain same precision as Cursor
   - Use platform capability

3. **Claude Code** (memory + commands):
   - `CLAUDE.md` for always-apply guidance (general, update, whats-next)
   - `.claude/commands/backlog.md`, `cip.md`, `requirements.md` for on-demand
   - User invokes with `/backlog` when working in backlog/

4. **Codex** (single file only):
   - `AGENTS.md` combined file
   - Trade-off: lose path-specificity, but platform doesn't support it anyway

---

## Implementation Mapping

### Base Prompts (Phase 1)

Create in `templates/prompts/`:

```
templates/prompts/
├── always-apply/          # Guidance that applies everywhere
│   ├── vibesafe_general.md
│   ├── vibesafe_update.md
│   └── whats_next.md
└── context-specific/      # Guidance for specific contexts
    ├── backlog.md
    ├── cip.md
    └── requirements.md
```

### Platform Generation (Phase 2)

**Cursor** (`generate_cursor_rules()`):
```bash
# Generate separate .mdc files with globs
for prompt in templates/prompts/context-specific/*.md; do
  add_cursor_frontmatter "$prompt" > ".cursor/rules/$(basename $prompt .md).mdc"
done
for prompt in templates/prompts/always-apply/*.md; do
  add_cursor_frontmatter "$prompt" > ".cursor/rules/$(basename $prompt .md).mdc"
done
```

**Copilot** (`generate_copilot_prompts()`):
```bash
# Generate path-specific instruction files
mkdir -p .github/instructions
create_copilot_instruction "backlog" "backlog/**/*.md" > .github/instructions/backlog.instructions.md
create_copilot_instruction "cip" "cip/**/*.md" > .github/instructions/cip.instructions.md
create_copilot_instruction "general" "**/*" > .github/instructions/general.instructions.md
```

**Claude Code** (`generate_claude_context()`):
```bash
# Combine always-apply prompts into CLAUDE.md
cat templates/prompts/always-apply/*.md > CLAUDE.md

# Create slash commands for context-specific
mkdir -p .claude/commands
cp templates/prompts/context-specific/*.md .claude/commands/
```

**Codex** (`generate_codex_context()`):
```bash
# Combine everything into AGENTS.md
{
  echo "# VibeSafe Project Documentation"
  cat templates/prompts/always-apply/*.md
  cat templates/prompts/context-specific/*.md
} > AGENTS.md
```

---

## Frontmatter Examples

### Copilot Path-Specific Instruction

```markdown
---
applyTo:
  - "backlog/**/*.md"
description: "VibeSafe Backlog System guidance"
---

# VibeSafe Backlog System
[content from templates/prompts/context-specific/backlog.md]
```

### Claude Slash Command

```markdown
# VibeSafe Backlog System

[content from templates/prompts/context-specific/backlog.md]

Usage: /backlog when working with backlog tasks
```

---

## Open Questions

1. **Copilot `applyTo` globs**: Does Copilot support the same glob syntax as Cursor?
   - Research needed during Phase 2 implementation

2. **Claude command naming**: Should commands be `/vibesafe-backlog` or `/backlog`?
   - May conflict with user's own commands
   - Suggest: `/vibesafe-backlog` for safety

3. **Always-apply vs context-specific**: Should we have MORE granularity?
   - e.g., separate "git operations" from "python environment"?
   - Current: vibesafe_general.md contains both
   - Suggestion: Start with current, refine later based on feedback

---

## Benefits of This Approach

✅ **Cursor users**: No change (best UX maintained)  
✅ **Copilot users**: Get path-specific guidance (uses platform capability)  
✅ **Claude users**: Get on-demand commands (natural workflow)  
✅ **Codex users**: Get all guidance (simple, no alternative)  
✅ **Maintainability**: Single source (`templates/prompts/`), multiple outputs

---

## Next Steps (Phase 1)

1. ✅ Document this strategy (this file)
2. Create `templates/prompts/always-apply/` directory
3. Create `templates/prompts/context-specific/` directory
4. Extract content from current `.cursor/rules/*.mdc` into base prompts
5. Create platform adapter functions per this strategy
6. Update Phase 2 task with specific implementation details

---

## References

- Current Cursor rules: `templates/.cursor/rules/*.mdc`
- Research summary: See CIP-0012 Phase 1 task progress notes
- Copilot instructions docs: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- Claude commands docs: https://www.anthropic.com/engineering/claude-code-best-practices

