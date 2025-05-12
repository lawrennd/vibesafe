# VibeSafe AI-Assisted Requirements Framework

The AI-Assisted Requirements Framework helps users conduct effective requirements conversations when starting new software projects. This framework bridges the gap between natural language requirements and software implementation, making the requirements process more accessible for both technical and non-technical stakeholders.

## Core Principles

1. Natural Language First: Requirements should be expressed in natural language that all stakeholders can understand.
2. AI Augmentation: AI tools can help guide, structure, and validate requirements conversations.
3. User Autonomy: The framework provides guidance without prescribing rigid processes.
4. Integration: Requirements should seamlessly connect to other project components (CIPs, backlog tasks, etc.).
5. Evolution: Requirements naturally evolve; the framework supports tracking and managing this evolution.

## Components

The framework consists of these key components:

### Prompts

Carefully designed prompts for different stages of the requirements process:

- Discovery: Initial exploration of user needs and project scope
- Refinement: Detailed elaboration of specific requirements
- Validation: Checking for completeness, consistency, and clarity
- Testing: Creating validation criteria from requirements

### Patterns

Reusable conversation structures for common requirements scenarios:

- [Stakeholder Identification](patterns/stakeholder-identification.md): Systematically identify and analyze all relevant stakeholders for a project
- [Goal Decomposition](patterns/goal-decomposition.md): Break down high-level goals into specific, actionable requirements
- Constraint mapping (planned)
- Scenario exploration (planned)
- Priority setting (planned)

### Integrations

Connectors to other VibeSafe components:
- CIP integration: How requirements inform improvement proposals
- Backlog integration: Tracing tasks back to requirements
- Documentation integration: Including requirements in project documentation

### Examples

Sample requirements conversations showing the framework in action:

- [Web application requirements](examples/web-app-discovery.md): Example of requirements discovery for a project management web app
- [Goal decomposition example](examples/goal-decomposition-example.md): Demonstration of breaking down goals for a data analytics dashboard
- [Framework self-development](examples/framework-self-development.md): Using the framework to plan its own development
- Data analysis tool requirements (planned)
- Mobile app requirements (planned)
- API service requirements (planned)

## Getting Started

To start using the AI-Assisted Requirements Framework:

1. Initial Setup: 
   - Choose appropriate prompts from the `prompts/` directory
   - Review example conversations in `examples/`
   - Set up integrations with other VibeSafe components

2. Conducting Requirements Conversations:
   - Use the prompts as conversation starters
   - Follow the conversation patterns to ensure completeness
   - Document requirements decisions as you go
   - Validate requirements with stakeholders

3. Integration with Project Workflow:
   - Connect requirements to CIPs for major feature development
   - Create backlog tasks that trace back to specific requirements
   - Update requirements as the project evolves

## Contributing

To contribute to the AI-Assisted Requirements Framework:

1. Add new prompts for requirements scenarios
2. Share example conversations that were particularly effective
3. Improve integration with other VibeSafe components
4. Enhance documentation with lessons learned

## Background

This framework was inspired by research on requirements-driven end-user software engineering, particularly the paper "Requirements are All You Need: The Final Frontier for End-User Software Engineering" (Robinson et al., 2024). 