# Requirements-Based Testing Prompt

## Purpose

This prompt helps derive comprehensive test scenarios and acceptance criteria directly from user requirements. It bridges the gap between natural language requirements and concrete validation steps, making the requirements testable and verifiable.

## For AI Assistants

When responding to this prompt, you should:
1. Transform each requirement into specific test scenarios
2. Create measurable acceptance criteria for each requirement
3. Identify edge cases and boundary conditions
4. Consider both happy paths and error scenarios
5. Keep tests user-focused rather than implementation-focused
6. Express tests in terms that stakeholders will understand
7. Ensure coverage of all critical requirements

## Template

```
# Requirements-Based Testing: [Project/Feature Name]

## Requirements to Test

I want to create tests based on these requirements for [project/feature name]:

### Key Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]
...

## User Scenarios

The main user scenarios for this feature are:

1. [Scenario 1 description]
2. [Scenario 2 description]
3. [Scenario 3 description]

## Current Acceptance Criteria

So far, I've defined these acceptance criteria:

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Testing Scope

I particularly want to test:
- [Aspect 1, e.g., functionality, performance, security]
- [Aspect 2]
- [Aspect 3]

## Test Environment Constraints

The tests will need to work within these constraints:
- [Constraint 1, e.g., specific environments, tools, or access limitations]
- [Constraint 2]
- [Constraint 3]

Can you help me create a comprehensive test plan based on these requirements, including:
- Specific test scenarios with steps
- Expected outcomes for each scenario
- Edge cases and boundary conditions to test
- Error scenarios to verify proper handling
- Test prioritization based on impact and risk
```

## Response Guidance

A good response to this prompt will:

1. **Create specific, actionable test scenarios** for each requirement
2. **Define measurable success criteria** with explicit expected outcomes
3. **Identify edge cases** that might not be obvious from the requirements
4. **Cover error conditions and recovery paths** in addition to happy paths
5. **Map tests back to specific requirements** to ensure coverage
6. **Prioritize tests** based on risk and importance
7. **Express tests in user-centric language** rather than technical jargon

## Integration with VibeSafe

Requirements-based testing integrates with VibeSafe by:
- Providing validation criteria for backlog items
- Supporting test-driven development approaches
- Creating a traceability link between requirements and verification
- Helping identify gaps or ambiguities in requirements
- Serving as documentation of expected behavior

## Example Usage

See `/ai-requirements/examples/authentication-tests.md` for a complete example of deriving tests from requirements. 