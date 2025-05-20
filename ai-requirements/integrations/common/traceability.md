# Common Traceability Patterns

This document describes common traceability patterns that can be used across both CIP and backlog integrations with the AI-Requirements framework.

## What is Traceability?

Traceability is the ability to track requirements from their origin through their implementation. Good traceability enables:

1. **Verification**: Confirm all requirements are implemented
2. **Change Impact Analysis**: Understand which implementations are affected by changing requirements
3. **Audit Support**: Document why specific implementations exist
4. **Coverage Analysis**: Identify requirements without implementation plans
5. **Status Tracking**: Monitor implementation progress across the project

## Bi-Directional Tracing

The most effective traceability is bi-directional:

1. **Forward Tracing**: From requirements to implementation (CIPs and backlog items)
2. **Backward Tracing**: From implementation back to source requirements

### Example: Forward Tracing

In a requirements document:

```markdown
## Implementation Status

The requirements in this document are being addressed as follows:

| Requirement | Implementation Type | Reference | Status |
|-------------|---------------------|-----------|--------|
| User Authentication | CIP | [CIP-0005](../../cip/cip0005.md) | In Progress |
| Password Reset | Backlog Task | [Task 2025-05-01_password-reset](../../backlog/features/2025-05-01_password-reset.md) | Ready |
| Account Deletion | Backlog Task | [Task 2025-05-02_account-deletion](../../backlog/features/2025-05-02_account-deletion.md) | Completed |
```

### Example: Backward Tracing

In a CIP:

```markdown
## Related Requirements

This CIP addresses the following requirements:

- [User Authentication Requirements](../../ai-requirements/examples/auth-requirements.md)

Specifically, it implements solutions for:
- Single sign-on integration
- Multi-factor authentication
- Session management
```

In a backlog item:

```markdown
## Requirements Reference

This task implements the following requirements:
- [User Authentication Requirements](../../ai-requirements/examples/auth-requirements.md)

Specifically, it addresses:
- Password reset functionality
```

## Traceability Identifiers

To facilitate tracing, we recommend consistent identifiers:

1. **Requirements Identifiers**: 
   - Format: `REQ-[category]-[number]` (e.g., `REQ-AUTH-001`)
   - Usage: Reference these in CIPs and backlog items

2. **CIP Identifiers**:
   - Format: Standard CIP numbering (e.g., `CIP-0005`)
   - Usage: Reference these in requirements and backlog items

3. **Backlog Identifiers**:
   - Format: Date-based ID (e.g., `2025-05-01_password-reset`)
   - Usage: Reference these in requirements and related CIPs

## Traceability Matrices

Traceability matrices provide a visual way to track relationships:

### Requirements-to-Implementation Matrix

| Requirement ID | Description | CIP | Backlog Tasks | Status |
|----------------|-------------|-----|---------------|--------|
| REQ-AUTH-001 | User login | CIP-0005 | 2025-05-01_login-ui | In Progress |
| REQ-AUTH-002 | Password reset | - | 2025-05-01_password-reset | Ready |
| REQ-AUTH-003 | Account deletion | - | 2025-05-02_account-deletion | Completed |

### Implementation-to-Requirements Matrix

| Implementation | Type | Requirements Addressed | Status |
|----------------|------|------------------------|--------|
| CIP-0005 | CIP | REQ-AUTH-001, REQ-AUTH-004 | In Progress |
| 2025-05-01_login-ui | Backlog | REQ-AUTH-001 | In Progress |
| 2025-05-01_password-reset | Backlog | REQ-AUTH-002 | Ready |

## Maintaining Traceability

To maintain effective traceability:

1. **Update Consistently**: When requirements or implementations change, update all related documents
2. **Review Regularly**: Schedule regular reviews of traceability to identify gaps
3. **Automate Where Possible**: Consider tools to help maintain traceability links
4. **Train Team Members**: Ensure all team members understand the importance of maintaining traceability

## Traceability Best Practices

1. **Be Specific**: Link to specific requirements, not just documents
2. **Keep Links Updated**: Update links when documents move or rename
3. **Capture Rationale**: Document why specific implementations address specific requirements
4. **Mind the Gaps**: Regularly check for requirements without implementations
5. **Visualize Relationships**: Use matrices or diagrams to visualize complex relationships
6. **Version Together**: Try to version requirements and implementations together when possible 