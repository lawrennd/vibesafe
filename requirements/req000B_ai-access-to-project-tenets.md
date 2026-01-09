---
id: "000B"
title: "AI Access to Project Tenets"
status: "Implemented"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-09"
related_tenets:
  - shared-information-landmarks
  - effortless-context-restoration
stakeholders:
  - ai-assistants
  - developers
  - vibesafe-users
tags:
  - ai-collaboration
  - information-architecture
  - project-governance
---

# Requirement 000B: AI Access to Project Tenets

## Description

AI assistants (like Cursor, GitHub Copilot, etc.) should have automatic access to project-specific tenets and guiding principles. When AI systems help with code generation, refactoring, or decision-making, they need to understand the project's unique values and constraints to provide relevant, context-aware assistance.

Project tenets represent the "WHY" behind decisions - they should be available as information landmarks that AI can reference when assisting with development.

Users should not need to:
- Manually copy tenets into cursor rules
- Repeatedly explain project principles to AI
- Maintain separate documentation for AI vs humans
- Update cursor rules when tenets change

## Acceptance Criteria

- [x] Project tenets are automatically converted to AI-accessible format during installation
- [x] AI assistants can reference project-specific principles without manual setup
- [x] Tenet updates trigger cursor rule regeneration during reinstallation
- [x] Generated rules follow cursor rule format (.mdc with YAML frontmatter)
- [x] System distinguishes between VibeSafe tenets and project-specific tenets
- [x] No manual cursor rule creation required for existing tenets
- [x] Rules are generated idempotently (safe to regenerate)

## User Stories

**As a developer**, I want AI assistants to automatically understand my project's guiding principles, so they suggest code that aligns with our values.

**As a project lead**, I want our tenets to automatically inform AI assistance, so the entire team (human and AI) follows our governance model.

**As an AI assistant**, I want access to project-specific context (tenets), so I can provide suggestions that respect the project's unique constraints and values.

## Notes

**Why This Matters:**

1. **Shared Information Landmarks**: Tenets serve as reference points for both humans and AI
2. **Consistent Guidance**: AI suggestions align with project governance
3. **Reduced Repetition**: No need to repeatedly explain project principles
4. **Automatic Synchronization**: Tenet changes propagate to AI assistance

**Implementation:**

CIP-0010 (Automatic Tenets-to-Cursor-Rules Generation) implements this requirement through:
- Automatic cursor rule generation from tenet files
- Integration with installation script
- Idempotent regeneration on reinstall
- Smart detection of project vs VibeSafe tenets

**Example Flow:**

1. Project has `tenets/our-project/performance-first.md`
2. Run VibeSafe installation
3. System generates `.cursor/rules/project_tenet_performance-first.mdc`
4. AI assistant reads the rule and understands performance is a priority
5. When suggesting code, AI considers performance implications

**Related:**

- **Tenet**: shared-information-landmarks (WHY - reliable collaboration requires shared reference points)
- **CIP**: CIP-0010 (HOW - automatic cursor rule generation from tenets)
- **Also relates to**: documentation-as-code tenet (tenets as living documentation)

