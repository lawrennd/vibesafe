# Requirements Refinement Prompt

## Purpose

This prompt helps refine and detail specific requirements after the initial discovery phase. It's designed to explore the details, acceptance criteria, and edge cases for individual features or components of a software system.

## For AI Assistants

When responding to this prompt, you should:
1. Focus on specific, actionable details
2. Help define clear acceptance criteria
3. Explore edge cases and potential issues
4. Capture both functional and non-functional aspects
5. Keep the discussion aligned with the overall project goals
6. Document detailed requirements in a structured format

## Template

```
# Requirements Refinement: [Feature/Component Name]

## Feature Overview

I want to refine the requirements for [feature/component name], which aims to [brief description of purpose].

This feature relates to these overall project goals:
- [Related goal 1]
- [Related goal 2]

## Current Understanding

My current understanding of this feature is:

[Description of the feature as currently understood]

The primary users of this feature will be:
- [User type 1] who need to [user need]
- [User type 2] who need to [user need]

## Specific Requirements

I think this feature should:

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Acceptance Criteria

I'd consider this feature complete when:

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Open Questions

I'm uncertain about:

1. [Question 1]
2. [Question 2]
3. [Question 3]

## Integration Points

This feature will need to interact with:

1. [Component/System 1]
2. [Component/System 2]
3. [Component/System 3]

Can you help me refine these requirements, suggest additional considerations, and develop comprehensive acceptance criteria?
```

## Response Guidance

A good response to this prompt will:

1. **Analyze the requirements** for completeness and clarity
2. **Suggest more detailed acceptance criteria** with measurable outcomes
3. **Identify potential issues or edge cases** the user may not have considered
4. **Explore technical and user experience implications**
5. **Raise questions about integrations** with other components
6. **Structure the requirements** in a format suitable for implementation
7. **Consider non-functional requirements** like performance, security, accessibility

## Integration with VibeSafe

Refined requirements can:
- Form the basis for specific backlog tasks
- Provide detailed context for CIP implementations
- Serve as acceptance criteria for testing
- Define clear interfaces between components

## Example Usage

See `/ai-requirements/examples/user-authentication-refinement.md` for a complete example of a requirements refinement conversation. 