---
title: "Requirements to CIP Integration"
created: "2025-05-16"
last_updated: "2025-05-16"
tags:
- integration
- requirements
- cip
---

# Requirements to CIP Integration

This document outlines how requirements are connected to Code Improvement Plans (CIPs) in the VibeSafe framework.

## Integration Overview

Requirements and CIPs are complementary artifacts:
- **Requirements** define *what* needs to be built and *why*
- **CIPs** define *how* the implementation will be structured and *when* it will be done

Through proper integration, we ensure that:
1. Every CIP addresses specific requirements
2. All requirements are eventually implemented through CIPs
3. Implementation status is synchronized between requirements and CIPs

## Integration Mechanisms

### 1. Cross-Referencing

Requirements and CIPs reference each other explicitly:

- **In Requirements**: The `Related` section lists CIPs that implement the requirement
- **In CIPs**: The `Related Requirements` section lists requirements addressed by the CIP

Example in a requirement:
```markdown
## Related
- CIP: CIP-0012 (User Authentication Refactoring)
- Backlog Items: 2023-05-01_auth-api-implementation
```

Example in a CIP:
```markdown
## Related Requirements
This CIP addresses the following requirements:

- [REQ-007: User Authentication](../ai-requirements/user-authentication.md)
- [REQ-009: API Security](../ai-requirements/api-security.md)

Specifically, it implements solutions for:
- Secure token-based authentication
- Role-based access control
- API request validation
```

### 2. Status Synchronization

Status changes in requirements or CIPs should trigger updates to the related artifacts:

| Requirements Status | Expected CIP Status |
|--------------------|---------------------|
| Proposed/Refined    | Not created yet      |
| Ready              | Proposed             |
| In Progress        | Accepted/Implemented |
| Implemented        | Implemented          |
| Validated          | Closed               |

### 3. Implementation Traceability

The implementation should be traceable from requirement to CIP to actual code:

1. Requirement defines the need
2. CIP specifies the implementation approach
3. Code references the CIP in commit messages and comments
4. Tests verify the implementation against the requirements' acceptance criteria

## Practical Integration Workflow

### From Requirements to CIPs

1. Capture and refine requirements until they reach "Ready" status
2. Create a CIP that addresses one or more related requirements
3. Reference the requirements explicitly in the CIP
4. Update the requirements to reference the new CIP
5. Implement according to the CIP
6. Update status in both artifacts as progress is made

### From CIPs to Requirements

1. When creating a CIP, identify which requirements it addresses
2. If no matching requirements exist, create new requirement documents
3. Reference the requirements in the CIP
4. Reference the CIP in the requirements
5. Ensure implementation satisfies the requirements' acceptance criteria
6. Update status in both artifacts as progress is made

## What's Next Integration

The `whats_next.py` script checks for:

1. Requirements without associated CIPs
2. CIPs without referenced requirements
3. Status inconsistencies between requirements and CIPs
4. Implementation progress against requirements

This helps ensure that the integration between requirements and CIPs is maintained throughout the project. 