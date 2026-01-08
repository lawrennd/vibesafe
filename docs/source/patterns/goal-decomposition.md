# Goal Decomposition Pattern

> **Note**: This is a VibeSafe thinking tool, not a required process. Use it when you're stuck breaking down goals into requirements.

## Purpose

This pattern helps systematically break down high-level goals into specific, actionable requirements. Goal decomposition is a critical process for translating abstract project objectives into concrete, implementable features and tasks. This approach helps ensure that all aspects of a goal are considered and that the resulting requirements directly contribute to the project's overall objectives.

## When to Use This Pattern

✅ **Use when**:
- You have a broad goal but unclear how to achieve it
- Requirements seem vague or too high-level
- You need to ensure completeness (not missing important aspects)
- You want to trace requirements back to business objectives

❌ **Don't use when**:
- Requirements are already clear and specific
- You're defining HOW to implement (that's CIP territory)
- You're breaking down implementation tasks (that's backlog territory)

## Pattern Structure

The goal decomposition conversation follows this general pattern:

1. *Goal Clarification*: Understand and refine high-level goals
2. *User-Centered Decomposition*: Break goals down into user-centered outcomes
3. *Feature Identification*: Identify specific features needed to achieve outcomes
4. *Requirements Specification*: Specify detailed requirements for each feature
5. *Verification Mapping*: Map requirements back to original goals
6. *Gap Analysis*: Identify missing requirements or unexplored areas
7. *Priority Alignment*: Ensure requirements prioritization aligns with goal importance

## Example Questions

### Goal Clarification

* "What specific problem or opportunity does this goal address?"
* "How would you measure success for this goal?"
* "Who are the primary beneficiaries when this goal is achieved?"
* "Are there any constraints or boundaries that should limit the scope of this goal?"
* "How does this goal align with broader strategic objectives?"

### User-Centered Decomposition

* "What specific outcomes would users experience if this goal is achieved?"
* "What different user groups are affected by this goal?"
* "What user journeys would be improved or created by achieving this goal?"
* "What pain points would be eliminated for each user group?"
* "What new capabilities would users gain?"

### Feature Identification

* "What features or functions would enable each user outcome?"
* "Are there existing systems or components that could support these outcomes?"
* "What are the minimal features needed for a viable solution?"
* "What features would enhance the core solution but aren't essential?"
* "Are there technical capabilities that need to be developed to enable these features?"

### Requirements Specification

* "What specific behaviors should each feature exhibit?"
* "What inputs and outputs are expected for each feature?"
* "What quality attributes (performance, security, usability) are important?"
* "What edge cases or exception scenarios should be handled?"
* "What integration points with other systems are needed?"

### Verification Mapping

* "How will each requirement contribute to the original goal?"
* "Are there any requirements that don't clearly support the goal?"
* "Do the requirements collectively ensure the goal will be achieved?"
* "What metrics could verify that each requirement supports the goal?"
* "Are there any conflicting requirements that might hinder goal achievement?"

### Gap Analysis

* "Are there aspects of the goal not addressed by the current requirements?"
* "What assumptions have we made that might create gaps?"
* "Are there user groups or stakeholders whose needs aren't represented?"
* "What potential obstacles might prevent goal achievement despite meeting requirements?"
* "Are there dependencies on external factors not captured in requirements?"

### Priority Alignment

* "Which requirements are most critical to achieving the core goal?"
* "Are there requirements that could be deferred without compromising the goal?"
* "How should requirements be sequenced to deliver value incrementally?"
* "Are there quick wins that could demonstrate progress toward the goal?"
* "How do resource constraints affect requirement prioritization?"

## Goal Decomposition Approaches

There are multiple approaches to goal decomposition depending on the project context:

### 1. Top-Down Hierarchical Decomposition

Break the goal into progressively smaller, more specific sub-goals until you reach implementable requirements.

```
Goal
├── Sub-goal 1
│   ├── Requirement 1.1
│   └── Requirement 1.2
├── Sub-goal 2
│   ├── Requirement 2.1
│   └── Requirement 2.2
└── Sub-goal 3
    ├── Requirement 3.1
    └── Requirement 3.2
```

**Best for**: Well-defined goals with clear hierarchical structure

**Example**:
```
Improve user onboarding experience
├── Simplify registration process
│   ├── Reduce registration fields to essential information only
│   └── Add social login options (Google, GitHub)
├── Enhance first-time user guidance
│   ├── Create interactive tutorial for key features
│   └── Implement contextual help tooltips
└── Increase retention after signup
    ├── Send personalized welcome email with next steps
    └── Implement progress tracking for initial user actions
```

### 2. User Story Mapping

Organize requirements by user activities, backbone stories, and detailed stories.

```
User Activities
├── Activity 1
│   ├── Backbone Story 1.1
│   │   ├── Detailed Story 1.1.1
│   │   └── Detailed Story 1.1.2
│   └── Backbone Story 1.2
│       ├── Detailed Story 1.2.1
│       └── Detailed Story 1.2.2
└── Activity 2
    └── ...
```

**Best for**: User-centered projects where the user journey is paramount

**Example**:
```
Managing Tasks
├── Creating Tasks
│   ├── Create basic task with title and description
│   │   ├── Add due date to task
│   │   └── Set priority level for task
│   └── Create task from template
│       ├── Select from predefined templates
│       └── Customize template for current use
└── Organizing Tasks
    └── ...
```

### 3. Goal-Question-Metric (GQM) Approach

Structure decomposition around goals, questions that must be answered, and metrics that indicate success.

```
Goal
├── Question 1
│   ├── Metric 1.1 → Requirement 1.1
│   └── Metric 1.2 → Requirement 1.2
└── Question 2
    ├── Metric 2.1 → Requirement 2.1
    └── Metric 2.2 → Requirement 2.2
```

**Best for**: Goals where measurement and validation are critical

**Example**:
```
Improve system performance
├── How fast should pages load?
│   ├── Average page load time < 2s → Implement asset compression
│   └── 95th percentile page load < 3.5s → Optimize database queries
└── How well does the system handle high traffic?
    ├── Support 1000 concurrent users → Implement connection pooling
    └── Zero downtime during traffic spikes → Add auto-scaling capability
```

## Goal Decomposition Matrix

After decomposing goals, create a matrix to visualize the relationship between goals and requirements:

| Requirement | Primary Goal | Sub-goal | Priority | Complexity | Dependencies |
|-------------|--------------|----------|----------|------------|--------------|
| [Requirement ID] | [Goal it supports] | [Sub-goal] | High/Medium/Low | High/Medium/Low | [Dependencies] |

## Integration with VibeSafe

Use goal decomposition to create better requirements (WHAT):

```
Tenet (WHY) → Goal → [Goal Decomposition Pattern] → Requirements (WHAT) → CIPs (HOW) → Backlog (DO)
```

**Example Flow**:
1. **Tenet**: "Simplicity at All Levels" (WHY we care)
2. **Goal**: "Make VibeSafe easy to adopt"
3. **Pattern**: Apply Goal Decomposition
4. **Requirements** (WHAT):
   - REQ-007: "Users can install with a single command"
   - REQ-008: "Clear boundaries between system and user files"
5. **CIPs** (HOW):
   - CIP-000E: "Clean Installation Philosophy"
6. **Backlog** (DO):
   - Task: "Update install-minimal.sh"

## Integration with Requirements Process

Use goal decomposition to:

1. *Ensure requirements traceability* back to project goals and tenets
2. *Identify missing requirements* that may be needed for complete goal fulfillment
3. *Prioritize requirements* based on their contribution to goals
4. *Validate requirements* against original objectives
5. *Communicate the purpose* of requirements to stakeholders
6. *Distinguish WHAT from HOW*: Decompose to outcomes, not implementation details

## Common Pitfalls

* *Losing sight of the original goal*: Requirements drift away from supporting the goal
* *Decomposing too far*: Creating overly detailed requirements that restrict implementation flexibility
* *Incomplete decomposition*: Missing important aspects of the goal
* *Imbalanced decomposition*: Over-focusing on technical aspects while neglecting user experience
* *Failing to validate*: Not checking if requirements collectively achieve the goal
* *Ignoring constraints*: Creating requirements that can't be implemented within project constraints 