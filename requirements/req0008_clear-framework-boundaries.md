---
created: '2026-01-03'
id: 0008
last_updated: '2026-01-03'
priority: High
related_backlog: []
related_tenets:
- user-autonomy
stakeholders:
- vibesafe-users
- developers
- ai-assistants
status: Ready
tags:
- user-experience
- clarity
- namespace
- autonomy
title: Clear Boundaries Between Framework and User Content
---

# Requirement 0008: Clear Boundaries Between Framework and User Content

## Description

Users should be able to clearly distinguish between VibeSafe framework internals and their own project content. While VibeSafe dogfoods its own framework (using CIPs, requirements, tenets), this should never confuse or impose on user projects. Clear boundaries enable users to maintain full control over their namespace and allow VibeSafe to evolve without breaking user projects.

Users should know:
- What files/directories belong to VibeSafe vs their project
- What naming patterns are framework vs user-controlled
- What concepts are VibeSafe-specific vs their own
- What gets updated by VibeSafe vs what they control

This clarity protects user autonomy and reduces cognitive load.

## Acceptance Criteria

- [ ] VibeSafe's internal resources use distinct names that don't collide with user conventions
- [ ] Framework concepts use different terminology than user concepts when deployed
- [ ] Documentation clearly explains what's VibeSafe framework vs user content
- [ ] Installation preserves user content while updating system files
- [ ] Users can easily identify which files are theirs vs VibeSafe's
- [ ] VibeSafe's dogfooding (its own CIPs, requirements) stays separate from user projects
- [ ] Namespace collisions are prevented through naming conventions

## Notes

**Examples of Clear Boundaries:**

1. **Virtual Environments**:
   - VibeSafe: `.venv-vibesafe/`
   - User: `.venv/` (their choice)
   - No collision, clear separation

2. **Tenets/Principles**:
   - In VibeSafe repo: `tenets/vibesafe/` (VibeSafe's tenets)
   - In user project cursor rules: `vibesafe-principles.mdc` (packaged as "principles")
   - User's own: `tenets/projectname/` (their tenets)
   - Clear distinction when deployed

3. **Tools**:
   - VibeSafe: `generate_vibesafe_principles.py` (framework tool)
   - User: `combine_tenets.py` (user tool, also used by VibeSafe)
   - Different purposes, clear separation

4. **File Classification**:
   - System files: Templates, scripts, generated files
   - User content: Their requirements, CIPs, backlog, code
   - Documented clearly in README, cursor rules

**Why This Matters:**
- **User Autonomy**: Users control their namespace
- **Simplicity**: Clear boundaries reduce confusion
- **Evolution**: VibeSafe can evolve without breaking user projects
- **Trust**: Users trust VibeSafe won't overwrite their work

**Related:**
- WHY: user-autonomy tenet (respect users' freedom)
- HOW: CIP-0011 implements through namespace separation, naming conventions