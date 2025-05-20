# Requirements Validation Prompt

## Purpose

This prompt helps validate that a set of requirements is complete, consistent, and ready for implementation. It guides the process of critically examining requirements to identify gaps, conflicts, and clarity issues before proceeding to development.

## For AI Assistants

When responding to this prompt, you should:
1. Systematically review each requirement for clarity and completeness
2. Identify potential conflicts between requirements
3. Look for missing requirements or edge cases
4. Analyze whether requirements are testable
5. Consider stakeholder perspectives that might be overlooked
6. Help prioritize requirements if needed
7. Document validation findings in an actionable format

## Template

```
# Requirements Validation: [Project/Feature Name]

## Requirements Summary

I've collected the following requirements for [project/feature name]:

### Functional Requirements

1. [Functional Requirement 1]
2. [Functional Requirement 2]
3. [Functional Requirement 3]
...

### Non-Functional Requirements

1. [Non-Functional Requirement 1, e.g., performance, security, usability]
2. [Non-Functional Requirement 2]
3. [Non-Functional Requirement 3]
...

### User Personas and Scenarios

**Persona 1**: [Brief description]
- Scenario: [Description of how this persona would use the system]

**Persona 2**: [Brief description]
- Scenario: [Description of how this persona would use the system]

## Acceptance Criteria

The following are the acceptance criteria I've defined:

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]
...

## Concerns and Uncertainties

Areas I'm particularly concerned about:

1. [Concern 1]
2. [Concern 2]
3. [Concern 3]

Can you validate these requirements by checking for:
- Completeness (missing requirements)
- Consistency (conflicting requirements)
- Clarity (ambiguous or vague requirements)
- Testability (whether requirements can be verified)
- Feasibility (whether requirements can reasonably be implemented)
- Prioritization (which requirements are essential vs. nice-to-have)
```

## Response Guidance

A good response to this prompt will:

1. **Systematically analyze each requirement** against validation criteria
2. **Identify specific issues** such as:
   - Ambiguous language or subjective terms
   - Conflicting requirements
   - Untestable requirements
   - Missing edge cases or scenarios
   - Unrealistic expectations
3. **Suggest improvements** to address identified issues
4. **Prioritize findings** based on their potential impact
5. **Recommend next steps** for refining the requirements
6. **Identify missing stakeholder perspectives** if applicable

## Integration with VibeSafe

Requirements validation integrates with VibeSafe by:
- Providing a quality gate before requirements become backlog items
- Ensuring CIPs are based on solid requirements
- Creating a record of requirement validation decisions
- Facilitating requirements traceability through the development process

## Example Usage

See `/ai-requirements/examples/e-commerce-validation.md` for a complete example of a requirements validation conversation. 