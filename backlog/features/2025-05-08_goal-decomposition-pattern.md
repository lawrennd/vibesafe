---
category: features
created: '2025-05-08'
dependencies:
- CIP-0009
- ai-requirements foundation
effort: medium
id: 2025-05-08_goal-decomposition-pattern
last_updated: '2025-05-12'
owner: Neil Lawrence
priority: High
related_cips: []
status: In Progress
title: Implement Goal Decomposition Pattern
type: feature
---

# Task: Implement Goal Decomposition Pattern

## Metadata
- **ID**: 2025-05-08_goal-decomposition-pattern
- **Type**: Feature
- **Status**: In Progress
- **Priority**: High
- **Estimated Effort**: Medium
- **Owner**: lawrennd
- **Dependencies**: CIP-0009, ai-requirements foundation

## Requirements Reference

This task implements the following requirements:
- [AI-Requirements Framework Self-Development](../../ai-requirements/examples/framework-self-development.md)

Specifically, it addresses:
- "Implement additional conversation patterns beyond stakeholder identification"
- "Goal Decomposition Pattern: Techniques for breaking high-level goals into specific, actionable requirements"

## Description

Create a Goal Decomposition Pattern for the AI-Requirements framework to help users systematically break down high-level goals into specific, actionable requirements. This pattern will be added to the existing patterns collection and will serve as one of the core conversation patterns for requirements gathering.

## Detailed Tasks

1. Research best practices for goal decomposition in requirements engineering
2. Create `ai-requirements/patterns/goal-decomposition.md` with:
   - Clear explanation of the pattern and its purpose
   - Step-by-step process for decomposing goals into requirements
   - Examples showing the pattern in use
   - Templates for different goal decomposition approaches
   - Common pitfalls and how to avoid them
3. Update `ai-requirements/examples/` with a demonstration of the pattern in use
4. Integrate the pattern with existing prompts and templates

## Acceptance Criteria

This task will be considered complete when:

1. The Goal Decomposition Pattern document is complete and follows the same format as existing patterns
2. The pattern includes at least three different approaches to goal decomposition
3. The pattern is demonstrated with a real example
4. The pattern integrates with existing stakeholder identification pattern
5. Documentation references are updated to include the new pattern

## Estimation Rationale

This task is estimated as Medium effort because:
- It requires research into goal decomposition best practices
- Creating quality examples will take significant time
- Integration with existing patterns requires careful consideration
- The pattern needs to be general enough to apply to various project types

## Prioritization Rationale

This task is High priority because:
- It was identified in the framework self-development requirements as a key next pattern
- Goal decomposition is fundamental to effective requirements engineering
- It provides a logical next step after stakeholder identification
- It enables the creation of more focused, specific requirements

## Progress Updates

### 2025-05-08
Task created with Proposed status based on framework self-development requirements.

### 2025-05-12
Updated status to In Progress. Created the initial Goal Decomposition Pattern document in `ai-requirements/patterns/goal-decomposition.md` with a comprehensive structure including:
- Detailed pattern structure with 7 key steps
- Example questions for each step of the process
- Three different approaches to goal decomposition with examples
- Goal decomposition matrix template
- Integration guidance with the requirements process
- Common pitfalls to avoid

Also created a complete example in `ai-requirements/examples/goal-decomposition-example.md` showing the pattern applied to a data analytics dashboard project.