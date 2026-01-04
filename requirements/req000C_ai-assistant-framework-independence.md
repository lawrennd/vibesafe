---
id: "000C"
title: "AI Assistant Framework Independence"
status: "Proposed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
related_tenets: ["user-autonomy", "simplicity-of-use"]
stakeholders: ["developers", "ai-assistants", "vibesafe-users"]
tags: ["compatibility", "ai-assistants", "portability", "framework-independence"]
---

# REQ-000C: AI Assistant Framework Independence

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.
> 
> ✅ Good: "VibeSafe works across different AI coding assistants"  
> ❌ Bad: "Use standard markdown files instead of Cursor-specific formats" (that's HOW)

## Description

VibeSafe should work seamlessly across different AI coding assistant platforms without being tied to any specific framework or tool. Users should be able to use VibeSafe with Cursor, Claude Code, GitHub Copilot, Codex, or any other AI coding assistant, and get the same core functionality and benefits.

The system should rely on standard, portable approaches (like file-based organization, markdown documentation, and YAML frontmatter) that any AI assistant can read and understand, rather than platform-specific features or APIs.

**Why this matters**: This requirement stems from two core tenets:
- **User Autonomy Over Prescription**: Users should choose their own tools and workflows. VibeSafe shouldn't force them to use a specific AI assistant.
- **Simplicity at All Levels**: Using standard file formats and conventions makes VibeSafe more accessible and reduces dependencies on specific platforms.

**Who benefits**: 
- **Developers**: Can use their preferred AI coding assistant without losing VibeSafe functionality
- **Organizations**: Can adopt VibeSafe regardless of their AI tooling choices
- **VibeSafe project**: Broader adoption and community growth by not limiting the user base

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] VibeSafe core functionality (CIPs, backlog, requirements, tenets) works with Cursor AI
- [ ] VibeSafe core functionality works with Claude Code (Anthropic's coding assistant)
- [ ] VibeSafe core functionality works with GitHub Copilot
- [ ] VibeSafe core functionality works with other AI coding assistants (Codex, Cody, etc.)
- [ ] No VibeSafe features require platform-specific APIs or extensions
- [ ] Documentation clearly states framework independence as a design principle
- [ ] Installation and setup work identically across different AI assistants
- [ ] AI assistants can read and understand VibeSafe's file-based organization (tenets, CIPs, backlog, requirements)

## Notes (Optional)

**Current State**: VibeSafe currently uses `.cursor/rules/` directory for AI assistant rules, which is Cursor-specific naming. However, the content (markdown files with YAML frontmatter) is standard and portable.

**Constraints**:
- Some AI assistants may have different ways of discovering project context (e.g., Cursor uses `.cursor/rules/`, others might use different directories)
- We should support platform-specific discovery mechanisms while keeping content portable
- The core VibeSafe content (CIPs, backlog, requirements, tenets) is already framework-independent (standard markdown + YAML)

**Trade-offs**:
- May need to support multiple directory structures for different platforms
- Documentation may need platform-specific setup instructions
- Some platform-specific optimizations might not be possible

## References

- **Related Tenets**: 
  - User Autonomy Over Prescription (`tenets/vibesafe/user-autonomy.md`)
  - Simplicity at All Levels (`tenets/vibesafe/simplicity-of-use.md`)
- **Related Requirements**: 
  - REQ-000B (AI Access to Project Tenets) - ensures AI assistants can access tenets
  - REQ-0008 (Clear Framework Boundaries) - distinguishes VibeSafe from platform-specific features
- **External Links**: 
  - Cursor AI documentation
  - Claude Code documentation
  - GitHub Copilot documentation

## Progress Updates

### 2026-01-04
Requirement created based on user request to ensure VibeSafe works across Claude Code, Codex, and other AI coding assistants, not just Cursor. Status: Proposed, needs review and refinement before moving to Ready.

