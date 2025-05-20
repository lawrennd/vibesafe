# Status Synchronization Between Requirements and Implementations

This document describes how to keep status information synchronized between requirements documents and their implementations (CIPs and backlog items).

## Why Status Synchronization Matters

Maintaining synchronized status across requirements and implementations:

1. *Provides Stakeholder Visibility*: Stakeholders see accurate implementation progress
2. *Reveals Inconsistencies*: Highlights misalignments between plans and reality
3. *Drives Accountability*: Makes clear what has been committed to and delivered
4. *Supports Reporting*: Enables accurate project status reporting
5. *Facilitates Decision Making*: Helps prioritize work based on actual progress

## Status Models

### Requirements Status Model

Requirements typically follow this status lifecycle:

1. *Proposed*: Initial requirement documented but not fully validated
2. *Refined*: Requirement clarified and validated with stakeholders
3. *Ready*: Requirement ready for implementation planning
4. *In Progress*: Implementation has started
5. *Implemented*: Implementation complete but not validated
6. *Validated*: Implementation verified to meet the requirement
7. *Deferred*: Implementation postponed to a future time
8. *Rejected*: Requirement will not be implemented (with rationale)

### CIP Status Model

CIPs follow this status lifecycle:

1. *Proposed*: Initial CIP documented
2. *Accepted*: CIP reviewed and approved for implementation
3. *Implemented*: Code changes complete
4. *Closed*: Implementation reviewed and merged

### Backlog Status Model

Backlog items follow this status lifecycle:

1. *Proposed*: Initial task documented
2. *Ready*: Task ready for implementation
3. *In Progress*: Task being actively worked on
4. *Completed*: Task successfully implemented
5. *Abandoned*: Task will not be implemented (with explanation)

## Status Mapping

When statuses change in one system, related statuses should be updated accordingly:

### Requirements → Implementations

| Requirements Status | CIP Status | Backlog Status |
|--------------------|------------|----------------|
| Proposed | Not Created | Not Created |
| Refined | Not Created | Not Created |
| Ready | Proposed | Proposed/Ready |
| In Progress | Accepted/Implemented | In Progress |
| Implemented | Implemented | Completed |
| Validated | Closed | Completed |
| Deferred | - | Abandoned (with explanation) |
| Rejected | - | Abandoned (with explanation) |

### Implementations → Requirements

| CIP Status | Backlog Status | Requirements Status |
|------------|----------------|---------------------|
| Proposed | Proposed | Ready |
| Accepted | Ready | In Progress |
| Implemented | In Progress | In Progress |
| Closed | Completed | Implemented/Validated |
| - | Abandoned | Deferred/Rejected |

## Status Synchronization Process

### 1. Initial Status Setting

When creating implementation items from requirements:

1. Set CIP status to "Proposed" when requirements reach "Ready" status
2. Set backlog item status to "Proposed" or "Ready" when requirements reach "Ready" status
3. Document the creation in the requirements document

### 2. Implementation Status Updates

As implementation progresses:

1. Update implementation status according to actual progress
2. Reflect changes in the requirements document
3. Document reasons for status changes, particularly for delays or issues

### 3. Requirement Status Updates

As requirements evolve:

1. Assess impact on related implementations
2. Update implementation statuses if needed
3. Document requirement changes and reasons

### 4. Periodic Status Reviews

Schedule regular status synchronization reviews:

1. Weekly or bi-weekly review of status alignment
2. Address any inconsistencies
3. Update documentation to reflect current reality

## Status Visualization

### Combined Status Dashboard

Create a dashboard showing requirements and implementation status side-by-side:

| Requirement | Req Status | CIP | CIP Status | Backlog Items | Backlog Status |
|-------------|------------|-----|------------|---------------|----------------|
| User Auth | In Progress | CIP-0005 | Accepted | 2025-05-01_login-ui | In Progress |
| Data Export | Ready | - | - | 2025-05-02_export | Ready |
| Reports | Implemented | CIP-0003 | Closed | 2025-04-15_reports | Completed |

### Status Change Log

Maintain a log of status changes to track progress over time:

```markdown
## Status Change Log

| Date | Item | Old Status | New Status | Reason |
|------|------|------------|------------|--------|
| 2025-05-01 | User Auth Requirement | Ready | In Progress | Implementation started |
| 2025-05-03 | CIP-0005 | Proposed | Accepted | Approved in review meeting |
| 2025-05-05 | 2025-05-01_login-ui | Ready | In Progress | Development started |
```

## Special Cases

### Partial Implementation

When a requirement is partially implemented:

1. Document which parts are implemented in the requirements status
2. Consider breaking the requirement into smaller, separately trackable items
3. Use a "Partially Implemented" tag with details on what's missing

### Changing Requirements

When requirements change after implementation has started:

1. Document the change and its impact on existing implementations
2. Update implementation items with new requirements information
3. Consider creating new implementation items if needed
4. Update status to reflect any setbacks or rework

### Blocked Implementation

When implementation is blocked:

1. Create a special "Blocked" status tag
2. Document the blocking factors
3. Create action items to resolve the blockers
4. Keep stakeholders informed of blocked items

## Best Practices for Status Synchronization

1. *Be Proactive*: Update statuses as soon as changes occur
2. *Be Transparent*: Document reasons for status changes
3. *Be Consistent*: Use the same status terminology across documents
4. *Be Detailed*: Include dates and rationale for status changes
5. *Be Traceable*: Link to evidence of status (e.g., merged PRs, completed tasks)
6. *Be Accessible*: Make status information easily available to all stakeholders 