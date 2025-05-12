# Backlog Integration

This document describes how to integrate the AI-Requirements framework with the VibeSafe backlog system to ensure traceability between requirements and implementation tasks.

## Overview

The backlog integration connects high-level requirements from the AI-Requirements framework to specific implementation tasks in the backlog system. This connection ensures that:

1. Every requirement is traceable to specific implementation tasks
2. Implementation tasks maintain context about their purpose
3. Status changes are synchronized between requirements and tasks
4. Nothing falls through the cracks during implementation

## Integration Workflow

### 1. Requirements Documentation

Start by documenting requirements using the AI-Requirements framework:

- Use appropriate prompts from `prompts/` directory
- Apply relevant patterns like stakeholder identification and goal decomposition
- Document the requirements in a structured format
- Store the requirements in project documentation

### 2. Backlog Creation

Once requirements are documented, create corresponding backlog items:

- Break down requirements into specific tasks
- Create backlog items with explicit requirements references
- Apply consistent prioritization and estimation
- Update requirements with backlog item references

### 3. Implementation

During implementation:

- Implement backlog items according to their priority
- Update both backlog and requirements status as progress occurs
- Address any requirement changes through formal updates

### 4. Validation and Closure

After implementation:

- Validate implementation against original requirements
- Update both requirements and backlog status to "Completed"
- Document any deviations or future enhancements

## Template for Requirement-Derived Backlog Items

When creating backlog items from requirements, use this template addition:

```markdown
## Requirements Reference

This task implements the following requirements:
- [Link to requirements document]

Specifically, it addresses:
- [Specific requirement text]

## Acceptance Criteria

Based on the source requirements, this task will be considered complete when:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Estimation Rationale

This task is estimated as [Small/Medium/Large] effort because:
- [Reason 1]
- [Reason 2]
- [Reason 3]

## Prioritization Rationale

This task is [High/Medium/Low] priority because:
- [Reason 1]
- [Reason 2]
- [Reason 3]
```

## Example

See the file `ai-requirements/examples/backlog-creation-example.md` for a complete example of creating backlog items from requirements.

## Best Practices

1. *Right-Size Tasks*: Break requirements into tasks that can be completed in a reasonable timeframe
2. *Be Explicit About Dependencies*: Clearly document how tasks depend on each other
3. *Balance Detail*: Requirements focus on "what" and "why", backlog items on "how" and "when"
4. *Keep Both Systems Updated*: When status changes in one system, update the other
5. *Include Acceptance Criteria*: Derived from requirements in every backlog item
6. *Check for Requirements Drift*: Regularly verify that implementation aligns with requirements
7. *Review Closed Items*: Periodically review completed items to ensure requirements were met 