---
id: "effortless-context-restoration"
title: "Effortless Context Restoration"
status: "Active"
created: "2026-01-09"
last_reviewed: "2026-01-09"
review_frequency: "Annual"
conflicts_with: ["user-autonomy", "simplicity-of-use"]
related_requirements:
  - "0005"  # Clear Understanding of Project Status
  - "0001"  # Standardized Component Metadata
  - "0002"  # Simple and Accessible Requirements Framework
  - "000B"  # AI Access to Project Tenets
tags:
  - cognitive-load
  - workflow
  - developer-experience
  - status-tracking
  - context-switching
---

# Project Tenet: Effortless Context Restoration

## Description

Software development work is intermittent—developers context-switch between projects, return after days or weeks away, and often juggle multiple codebases simultaneously. VibeSafe must enable developers to **quickly understand project state and make informed decisions** without requiring them to remember previous context or reconstruct where they left off.

This tenet recognizes that cognitive load is the enemy of progress, but **agency is essential**. VibeSafe should reduce the mental burden of tracking state while keeping developers firmly in control of all decisions.

Developers should not need to:
- Remember which CIPs are in progress
- Recall which backlog tasks are ready to work on
- Reconstruct what requirements need attention
- Figure out which files are missing YAML frontmatter
- Remember what branch they're on or what they last committed
- Manually track relationships between requirements, CIPs, and backlog tasks

Instead, VibeSafe's `./whats-next` tool answers three questions instantly:
1. **Where am I?** (Git status, current branch, recent commits)
2. **What's missing?** (Files needing frontmatter, incomplete documentation)
3. **What's next?** (Prioritized recommendations—developer decides what to do)

**Critical distinction**: VibeSafe **informs and suggests**, it never **decides or acts** without explicit developer command. Every action requires developer initiation. The goal is effortless context restoration so developers can make quick, confident decisions—not to automate away their agency.

This is fundamentally about respecting that software development competes with work, meetings, other projects, and life. A system that requires sustained focus and perfect memory will fail; a system that enables quick, informed decision-making will succeed.

## Quote

*"The system remembers, so you don't have to—but you're always in control."*

## Examples

### Good: Single Command Status Check

```bash
# Developer returns after 2 weeks away
./whats-next

📋 Requirements Status
  Total: 16 requirements
  Implemented: 8
  In Progress: 4 (REQ-0005, REQ-0006, REQ-000D, REQ-000F)
  Ready: 4

🎯 CIP Status
  Accepted: 2 CIPs ready for implementation
  In Progress: 3 CIPs
  Proposed: 1 CIP needs review

📝 Backlog Status
  In Progress: 5 tasks
  Ready: 12 tasks

🔄 Git Status
  Branch: cip0012-validation-improvements
  Uncommitted: 2 files modified
  Last commit: "Add YAML validation for tenets" (2 weeks ago)
```

**Developer immediately knows**: What's in flight, what needs attention, where they left off.  
**Developer decides**: Continue CIP-0012? Switch to ready backlog task? Review proposed CIP? Their call.

### Good: Progressive Disclosure

```bash
# Quick overview
./whats-next --quiet

# Detailed breakdown if needed
./whats-next

# Specific component focus
./whats-next --cip-only
./whats-next --requirements-only
```

**Developer controls detail level** based on how much they remember.

### Good: Clear Next Actions

```bash
./whats-next

📌 Recommended Next Steps:
  1. Review proposed CIP-0013 (compression improvements)
  2. Complete in-progress task: 2026-01-08_validation-improvements
  3. Add YAML frontmatter to 3 files:
     - cip/cip0012.md
     - backlog/features/2026-01-05_new-feature.md
     - requirements/req0010_example.md
```

**Developer has exact next steps** without analysis paralysis.

### Good: Relationship Tracking

```bash
# Developer doesn't need to remember which CIPs implement which requirements
./whats-next --requirements-only

REQ-0005 (In Progress): Clear Understanding of Project Status
  Implemented by: CIP-0009 (whats-next script)
  Backlog tasks: 2 in progress, 1 completed

REQ-000D (Ready): CIPs as Self-Contained Design Documents
  Not yet implemented
  Action: Create CIP to address this requirement
```

**System shows**: Requirements coverage without manual tracking.

### Good: AI Assistant Context

When an AI assistant starts a session, it runs `./whats-next` to understand:
- Current branch and uncommitted work
- Which CIPs are active
- Which requirements need attention
- Priority backlog tasks

**AI can immediately provide relevant assistance** without asking "what are you working on?"

## Counter-examples

### Bad: Requires Memory

```bash
# ❌ No automated status view
ls cip/
# Developer must manually read files to understand status
```

**Problem**: Forces developers to reconstruct state manually.

### Bad: Hidden State

```bash
# ❌ No way to see requirements coverage
cat requirements/req0005*.md
# Developer must manually track which CIPs implement this
```

**Problem**: Relationships between components are invisible without manual inspection.

### Bad: Complex Resumption

```bash
# ❌ Multi-step process to figure out status
git status
git log -5
grep -r "status:" cip/*.md
grep -r "status:" backlog/**/*.md
# ... manual analysis to determine what's next
```

**Problem**: Requires sustained focus and multiple commands to understand state.

### Bad: No Prioritization

```bash
# ❌ Overwhelming list without context
ls backlog/**/*.md

62 files found
```

**Problem**: No indication of what's ready, what's in progress, or what's priority.

### Bad: Stale Context

```bash
# ❌ Manual STATUS.md that's never updated
cat STATUS.md

Last updated: 2025-12-01
Current work:
  - CIP-0008 (but actually closed 3 weeks ago)
  - REQ-0003 (but new requirements added since then)
```

**Problem**: Manual tracking gets stale. Automated status stays current.

## Conflicts

### Effortless Context Restoration vs. User Autonomy

**Tension**: Reducing cognitive load might tempt us to "just do it for the user" and automate decisions.

**Resolution**: **Strict separation between information and action**:
- Status commands are *read-only* (`./whats-next` shows state, suggests actions)
- Action commands are *explicit* (developer types the actual commands)
- Never conflate "knowing what to do" with "doing it automatically"

Example:
```bash
# ❌ Bad: Auto-acts
./fix-everything     # Too magical, removes control

# ✅ Good: Informs, user acts
./whats-next         # Shows what needs doing
# Developer explicitly runs actions based on recommendations
```

### Effortless Context Restoration vs. Simplicity at All Levels

**Tension**: Status tracking adds complexity (scripts, YAML parsing, cross-references).

**Resolution**: Accept that **context restoration is core functionality**, not optional feature. The `whats-next` script is worth the maintenance burden because developers will create ad-hoc status scripts if we don't provide a reliable one, leading to inconsistent, unreliable approaches.

**Design principle**: Keep status script fast (<2 seconds) and maintain it as first-class VibeSafe component.

### Effortless Context Restoration vs. Detail/Precision

**Tension**: Summary views might hide important details that developers need.

**Resolution**: Provide **progressive disclosure**:
- Default: High-level summary (current status, next actions)
- `--detailed`: Full breakdown with all relationships
- Component-specific flags: `--cip-only`, `--requirements-only`, `--backlog-only`

## Related Requirements

This tenet directly informs several VibeSafe requirements:

- **REQ-0005**: Clear Understanding of Project Status (primary requirement)
  - Defines WHAT we need (quick status understanding)
  - This tenet explains WHY it matters (context switching, cognitive load)
  
- **REQ-0001**: Standardized Component Metadata
  - Enables automated status tracking through machine-readable frontmatter
  - Without this, context restoration would require manual file inspection

- **REQ-0002**: Simple and Accessible Requirements Framework
  - Reduces cognitive load in requirements management
  - Supports effortless context restoration through simplicity

- **REQ-000B**: AI Access to Project Tenets
  - AI assistants also benefit from effortless context restoration
  - Tenets as information landmarks help AI understand project quickly

## Implementation Notes

The `./whats-next` script is the primary implementation of this tenet. It:
- Parses YAML frontmatter to extract status
- Calculates relationships between components
- Provides prioritized recommendations
- Runs fast enough for frequent use
- Supports progressive disclosure with flags

Future improvements should maintain this tenet's principles:
- Always read-only (never mutates project state)
- Fast execution (<2 seconds ideal)
- Clear, actionable output
- Progressive disclosure for detail when needed

## Benefits

1. **Lower Cognitive Load**: Developers don't need to remember state across sessions
2. **Faster Resumption**: Minutes to context-restore, not hours of reading files
3. **Better Project Velocity**: Developers more likely to make progress if resumption is easy
4. **Reduced Anxiety**: Clear visibility reduces stress about "what am I forgetting?"
5. **Multi-tasking Friendly**: Developers can context-switch without losing place
6. **Work-Life Balance**: Development fits around life, not vice versa
7. **Better AI Collaboration**: AI assistants can quickly understand project state

## Real-World Scenarios This Enables

**Scenario 1: Context Switching Developer**
- Works on VibeSafe project Monday
- Switches to client work Tuesday-Thursday
- Returns Friday morning
- Runs `./whats-next` → immediately knows where to continue
- No time wasted reconstructing state

**Scenario 2: New AI Assistant Session**
- Developer starts new Cursor session
- AI assistant runs `./whats-next` to understand project
- AI sees: CIP-0012 in progress, 3 files need frontmatter
- AI can immediately provide relevant assistance

**Scenario 3: Multi-Project Juggling**
- Developer maintains 5 VibeSafe-based projects
- Can't remember status of each
- Runs `./whats-next` in each → instant status overview
- Decides which project needs attention most urgently

**Scenario 4: Team Collaboration**
- New team member joins project
- Runs `./whats-next` to understand current work
- Clear picture of active CIPs, requirements, and backlog
- Can contribute productively without extensive onboarding

## Measuring Success

How do we know if this tenet is working?

- **Time to Resumption**: Developer can understand current state in <30 seconds
- **Mental Model Match**: Developer's understanding of state matches actual state
- **Action Clarity**: Developer knows exactly what to do next without analysis
- **Tool Usage**: `./whats-next` is run frequently (indicating it's valuable)
- **AI Effectiveness**: AI assistants provide relevant suggestions after running status check
- **Developer Confidence**: Developers report feeling "in control" of project state

## Version

1.0 (2026-01-09)


