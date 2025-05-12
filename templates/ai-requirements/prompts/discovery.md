# Requirements Discovery Prompt

## Purpose

This prompt is designed to help initiate a requirements conversation when starting a new software project. It guides the exploration of user needs, project scope, and high-level requirements before diving into specific features.

## For AI Assistants

When responding to this prompt, you should:
1. Ask open-ended questions that encourage detailed responses
2. Help identify stakeholders and their specific needs
3. Explore both functional and non-functional requirements
4. Document assumptions and constraints
5. Avoid jumping to implementation details too quickly
6. Focus on understanding "why" before "how"

## Template

```
# Requirements Discovery Conversation

## Project Context

I'm looking to create [brief description of the software project].

The main goals of this project are:
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

I anticipate this software will be used by [description of users/stakeholders].

## Current Situation

Currently, [description of how things work without the software].

The main challenges or pain points are:
1. [Challenge 1]
2. [Challenge 2]
3. [Challenge 3]

## Initial Requirements

I think the software should:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Constraints and Assumptions

Some important constraints to consider:
1. [Constraint 1, e.g., timeline, budget, technical limitations]
2. [Constraint 2]
3. [Constraint 3]

I'm making these assumptions:
1. [Assumption 1]
2. [Assumption 2]
3. [Assumption 3]

## Questions

I'm particularly unsure about:
1. [Question 1]
2. [Question 2]
3. [Question 3]

Can you help me explore these requirements further and identify what I might be missing?
```

## Response Guidance

A good response to this prompt will:

1. **Acknowledge the stated goals and requirements**
2. **Ask clarifying questions** about ambiguous points
3. **Suggest additional considerations** the user may not have thought of
4. **Identify potential conflicts or challenges** in the requirements
5. **Help structure and categorize** the requirements into logical groups
6. **Document the conversation** in a format that can be referenced later
7. **Guide the next steps** in the requirements process

## Integration with VibeSafe

This discovery conversation can lead to:
- Creation of backlog items for specific requirements
- Development of a CIP for major features or architectural decisions
- Documentation of key requirements for future reference

## Example Usage

See `/ai-requirements/examples/web-app-discovery.md` for a complete example of a requirements discovery conversation. 