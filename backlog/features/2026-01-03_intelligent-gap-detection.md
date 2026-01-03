---
id: "2026-01-03_intelligent-gap-detection"
title: "Phase 0d: Intelligent Gap Detection & AI-Assisted Suggestions"
status: "Ready"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
category: "features"
owner: ""
dependencies: ["2026-01-03_integrate-validator-whats-next"]
related_cips: ["0011"]
---

# Task: Phase 0d: Intelligent Gap Detection & AI-Assisted Suggestions

## Description

Enhance the `whats-next` script to detect missing VibeSafe components (tenets, requirements, CIPs, backlog) and provide intelligent, AI-assisted suggestions to help users bootstrap their project structure.

This builds on Phase 0c by adding proactive guidance: if components are missing, suggest creating them in the correct order (Tenets → Requirements → CIPs → Backlog) with AI prompts to help.

## Acceptance Criteria

- [ ] **Gap Detection**:
  - [ ] Detect missing tenets (no `tenets/` files)
  - [ ] Detect missing requirements (no `requirements/` files)
  - [ ] Detect missing CIPs (no `cip/` files beyond templates)
  - [ ] Detect missing backlog items (no `backlog/` files beyond templates)
  - [ ] Detect codebase presence (any source code files)

- [ ] **Intelligent Suggestions (Priority Order)**:
  - [ ] If codebase exists + no tenets: Suggest "Create 3-5 tenets from codebase"
  - [ ] If tenets exist + CIPs exist + no requirements: Suggest "Extract requirements from CIPs"
  - [ ] If requirements exist + no CIPs: Suggest "Create CIPs for high-priority requirements"
  - [ ] If CIPs exist + no backlog: Suggest "Break down CIPs into backlog tasks"

- [ ] **AI-Assisted Prompts**:
  - [ ] **For Tenets**: Provide prompt for AI agents to scan codebase and suggest tenets
    - Analyze code patterns, architecture decisions, design philosophy
    - Suggest 3-5 foundational tenets based on observed patterns
    - User edits and approves suggestions
  - [ ] **For Requirements**: Provide prompt to extract WHAT from CIPs
    - Scan existing CIPs for goals and motivations
    - Extract desired outcomes (WHAT) from implementation plans (HOW)
    - Link requirements to related tenets (WHY)
    - Update CIPs to reference the new requirements
  - [ ] **For CIPs**: Provide prompt to design HOW for requirements
    - For each high-priority requirement, suggest implementation approach
    - Link CIPs to requirements they address
  - [ ] **For Backlog**: Provide prompt to break down CIPs into tasks
    - For each CIP, identify concrete implementation steps
    - Create backlog tasks linked to CIPs

- [ ] **Interactive Mode** (optional enhancement):
  - [ ] Prompt user: "Would you like help creating [tenets/requirements/CIPs/backlog]? [y/N]"
  - [ ] If yes: Display AI prompt and offer to run it via AI agent
  - [ ] If no: Continue with normal next steps

- [ ] **Output Format**:
  - [ ] Show gap detection in "Next Steps" section
  - [ ] Provide clear, actionable prompts for AI agents
  - [ ] Show suggested creation order (Tenets → Requirements → CIPs → Backlog)

## Implementation Notes

**Gap Detection Logic**:

```python
def detect_gaps():
    """Detect missing VibeSafe components."""
    gaps = {
        'has_codebase': detect_codebase(),  # Any .py, .js, .ts, .go, etc.
        'has_tenets': detect_component('tenets'),
        'has_requirements': detect_component('requirements'),
        'has_cips': detect_component('cip'),
        'has_backlog': detect_component('backlog')
    }
    return gaps

def generate_ai_prompts(gaps):
    """Generate AI prompts based on detected gaps."""
    prompts = []
    
    # Priority 1: Tenets (foundation)
    if gaps['has_codebase'] and not gaps['has_tenets']:
        prompts.append({
            'type': 'create_tenets',
            'priority': 'high',
            'prompt': TENET_EXTRACTION_PROMPT
        })
    
    # Priority 2: Requirements (extracted from CIPs if they exist)
    if gaps['has_tenets'] and gaps['has_cips'] and not gaps['has_requirements']:
        prompts.append({
            'type': 'extract_requirements',
            'priority': 'high',
            'prompt': REQUIREMENT_EXTRACTION_PROMPT
        })
    
    # Priority 3: CIPs (implementation plans)
    if gaps['has_requirements'] and not gaps['has_cips']:
        prompts.append({
            'type': 'create_cips',
            'priority': 'medium',
            'prompt': CIP_CREATION_PROMPT
        })
    
    # Priority 4: Backlog (tasks)
    if gaps['has_cips'] and not gaps['has_backlog']:
        prompts.append({
            'type': 'create_backlog',
            'priority': 'medium',
            'prompt': BACKLOG_CREATION_PROMPT
        })
    
    return prompts
```

**AI Prompts Template**:

```
=== TENET EXTRACTION PROMPT ===
Analyze the codebase and identify 3-5 foundational tenets that guide this project's design and implementation.

Look for:
- Recurring patterns in code organization
- Architectural decisions (e.g., modularity, separation of concerns)
- Design philosophy evident in code structure
- Trade-offs made (e.g., simplicity vs. features)
- User experience priorities

For each tenet, provide:
1. Title (short, memorable)
2. Description (1-2 paragraphs)
3. Quote (one sentence that captures the essence)
4. Examples from the codebase
5. Counter-examples (what this tenet avoids)

Output format: tenets/[kebab-case-name].md with YAML frontmatter


=== REQUIREMENT EXTRACTION PROMPT ===
Extract requirements (WHAT) from existing CIPs (HOW).

For each CIP, identify:
- What problem does it solve?
- What outcome is desired?
- What should be true after implementation?
- Which tenets does this support? (WHY)

Output format: requirements/req[XXXX]_short-name.md with YAML frontmatter
Link requirements back to tenets (WHY → WHAT)
Update CIPs to reference the extracted requirements
```

**User Experience**:

```
Suggested Next Steps:
1. Fix 124 validation errors: ./scripts/validate_vibesafe_structure.py --fix --fix-links

📋 Gap Detection:
✅ Codebase detected
❌ No tenets found

💡 Suggested: Create 3-5 tenets to capture your project's guiding principles

   Use this AI prompt to get started:
   
   "Analyze this codebase and suggest 3-5 foundational tenets that capture
   the project's design philosophy, architecture decisions, and priorities.
   For each tenet, provide: title, description, quote, examples, counter-examples.
   Output in VibeSafe tenet format with YAML frontmatter."
   
   Once created, run ./whats-next again for next steps.
```

## Related

- CIP: 0011 (Component Management)
- Requirement: REQ-0005 (Project Summary Tool)
- Depends on: 2026-01-03_integrate-validator-whats-next (Phase 0c - COMPLETED)
- Enhances: whats-next script with proactive guidance

## Progress Updates

### 2026-01-03
Task created as Phase 0d. Medium priority for intelligent project guidance.

This feature makes VibeSafe more helpful by detecting gaps and providing actionable AI-assisted guidance to bootstrap missing components in the correct order.

