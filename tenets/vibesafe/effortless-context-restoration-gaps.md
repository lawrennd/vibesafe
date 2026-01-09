---
id: "effortless-context-restoration-gaps"
title: "Missing Requirements Analysis: Effortless Context Restoration Tenet"
status: "Active"
type: "analysis"
created: "2026-01-09"
last_reviewed: "2026-01-09"
review_frequency: "As-Needed"
related_tenet: "effortless-context-restoration"
author: "Neil Lawrence"
tags: ["analysis", "requirements", "gaps"]
---

# Missing Requirements Analysis: Effortless Context Restoration Tenet

**Date**: 2026-01-09  
**Tenet**: effortless-context-restoration  

## Purpose

This document identifies potential gaps in VibeSafe requirements coverage related to the "Effortless Context Restoration" tenet. While several requirements support this tenet, some aspects mentioned in the tenet are not explicitly captured as requirements.

## Existing Requirements (Already Linked)

✅ **REQ-0005**: Clear Understanding of Project Status
- Covers the core "what's next" functionality
- Status: Ready
- Primary requirement for this tenet

✅ **REQ-0001**: Standardized Component Metadata
- Enables automated status tracking
- Status: Ready
- Foundation for context restoration

✅ **REQ-0002**: Simple and Accessible Requirements Framework
- Reduces cognitive load
- Status: Ready
- Supports simplicity aspect

✅ **REQ-000B**: AI Access to Project Tenets
- AI context restoration
- Status: Implemented
- Covers AI assistant needs

## Potential Missing Requirements

### 1. Git Workflow Integration (HIGH PRIORITY)

**Gap**: The tenet emphasizes Git status integration ("What branch am I on? What did I last commit?"), but no requirement explicitly states that VibeSafe should integrate Git workflow information into status tools.

**Evidence from tenet**:
- "Remember what branch they're on or what they last committed"
- Examples show Git status in `whats-next` output
- "Where am I? (Git status, current branch, recent commits)"

**Suggested Requirement**: REQ-0010 (next available ID)
```yaml
id: "0010"
title: "Git Workflow Context Integration"
status: "Proposed"
priority: "Medium"
related_tenets:
  - effortless-context-restoration
description: >
  VibeSafe status tools should integrate Git workflow information 
  (current branch, recent commits, uncommitted changes) to help 
  developers understand not just project status but also their 
  working tree state.
```

**Current Implementation**: `whats-next.py` already does this (lines 400-500), but it's not formally required.

### 2. Performance Requirements for Status Tools (MEDIUM PRIORITY)

**Gap**: The tenet mentions "<2 seconds ideal" for status checks, and "fast enough for frequent use," but no requirement specifies performance targets.

**Evidence from tenet**:
- "Keep status script fast (<2 seconds)"
- "Tool is fast (< 2 seconds for typical project)" in REQ-0005 acceptance criteria
- "Fast execution (<2 seconds ideal)" in Implementation Notes

**Suggested Requirement**: REQ-0011 (next available ID)
```yaml
id: "0011"
title: "Status Tool Performance Standards"
status: "Proposed"
priority: "Medium"
related_tenets:
  - effortless-context-restoration
  - simplicity-of-use
acceptance_criteria:
  - Status checks complete in <2 seconds for typical projects
  - Status checks scale to projects with 100+ CIPs, 500+ backlog items
  - Performance degrades gracefully for large projects
  - --quick flag available for sub-second results on large projects
```

**Rationale**: If status tools are slow, developers won't run them frequently, defeating the purpose.

### 3. Progressive Disclosure Pattern (LOW PRIORITY)

**Gap**: The tenet emphasizes progressive disclosure (--quiet, --detailed, --cip-only flags), but this pattern isn't captured as a requirement.

**Evidence from tenet**:
- Multiple examples showing flag usage
- "Progressive disclosure" mentioned in Conflicts resolution
- Counter-example: "Overwhelming list without context"

**Suggested Requirement**: REQ-0012 (next available ID)
```yaml
id: "0012"
title: "Progressive Disclosure in Status Tools"
status: "Proposed"
priority: "Low"
related_tenets:
  - effortless-context-restoration
  - user-autonomy
description: >
  Status tools should support progressive disclosure, allowing users
  to control the level of detail shown (quick summary vs. deep analysis)
  and focus on specific components (CIPs only, backlog only, etc.)
```

**Current Implementation**: Already implemented in `whats-next.py` with --quiet, --cip-only, --backlog-only, --requirements-only flags.

**Note**: This is LOW priority because it's already implemented and working well. Documenting as a requirement is mainly for completeness.

### 4. Status Tool Output Format Standards (LOW PRIORITY)

**Gap**: The tenet shows specific output formats (emoji, sections, clear hierarchy), but no requirement specifies output format standards.

**Evidence from tenet**:
- Examples show consistent emoji usage (📋, 🎯, 📝, 🔄)
- Clear sectioning and hierarchy
- "Output is readable by both humans and AI assistants" in REQ-0005

**Suggested Requirement**: REQ-0013 (next available ID)
```yaml
id: "0013"
title: "Human and Machine Readable Status Output"
status: "Proposed"
priority: "Low"
related_tenets:
  - effortless-context-restoration
  - shared-information-landmarks
description: >
  Status tool output should be optimized for both human readability
  (clear hierarchy, visual markers, concise) and machine parsing
  (structured format, consistent patterns).
```

**Current Implementation**: Already implemented with colored output, emoji, structured sections.

**Note**: LOW priority because it's working well. Mainly documentation value.

## Non-Requirements (Explicitly Out of Scope)

These aspects from the tenet do NOT need requirements:

❌ **Specific Script Implementation Details**
- How `whats-next.py` is structured internally
- YAML parsing approach
- Caching strategies
These are implementation choices, not requirements (WHAT vs HOW).

❌ **Specific Output Text**
- Exact wording of recommendations
- Specific emoji choices
These are UX details that should evolve, not be locked in requirements.

❌ **Read-Only Nature of Status Commands**
- This is a design principle (mentioned in tenet conflicts), not a requirement
- Covered implicitly by REQ-0005 ("status" = read-only by definition)

## Recommendations

### Immediate Actions (High Priority)

1. **Create REQ-0010: Git Workflow Context Integration**
   - Formalizes existing `whats-next` Git integration
   - Documents why Git status matters for context restoration
   - Priority: HIGH (core functionality not explicitly required)

### Near-Term Actions (Medium Priority)

2. **Create REQ-0011: Status Tool Performance Standards**
   - Sets performance expectations
   - Guides future optimization work
   - Priority: MEDIUM (important but not urgent, already fast enough)

### Optional (Low Priority)

3. **Consider REQ-0012 and REQ-0013**
   - Only if documenting existing patterns has value
   - Both already implemented and working
   - Priority: LOW (documentation value only)

## Summary

The "Effortless Context Restoration" tenet is **reasonably well covered** by existing requirements:
- Core functionality: ✅ REQ-0005
- Foundation (YAML): ✅ REQ-0001
- Simplicity: ✅ REQ-0002
- AI support: ✅ REQ-000B

**Primary gap**: Git workflow integration is implemented but not formally required (REQ-0010 suggested).

**Secondary gap**: Performance standards mentioned in tenet but not captured as requirements (REQ-0011 suggested).

## Next Steps

1. Review this analysis with VibeSafe maintainers
2. Decide which missing requirements to create
3. If creating REQ-0010, link it to this tenet and CIP-0009 (whats-next implementation)
4. Consider whether performance standards (REQ-0011) should be documented now or later

