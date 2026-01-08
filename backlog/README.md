# Lynguine Project Backlog

## Overview

This directory contains the project backlog - tasks and improvements that are planned but not yet implemented. The backlog is organized into different categories to help prioritize and track work items.

## Structure

The backlog is structured as follows:

1. Each task is stored in a separate Markdown file with a unique identifier
2. Files follow one of these naming conventions:
   - `YYYY-MM-DD_short-description.md` (e.g., `2025-05-05_readthedocs-setup.md`)
   - `YYYYMMDD-short-description.md` (e.g., `20250505-readthedocs-setup.md`)
3. Task statuses are tracked within each file
4. Tasks can be linked to GitHub issues or CIPs

## Task Status Workflow

Tasks follow this workflow:

```
Proposed → Ready → In Progress → Completed/Abandoned
```

## Task Template

Each task file should include:

- **ID**: A unique identifier (date + short name)
- **Title**: A descriptive title
- **Status**: Current status (Proposed, Ready, In Progress, Completed, Abandoned)
- **Priority**: High, Medium, Low
- **Dependencies**: Other tasks this depends on
- **Description**: Detailed description of the task
- **Acceptance Criteria**: Clear criteria for when the task is complete
- **Related**: Links to CIPs, GitHub issues, or other related items
- **Notes**: Additional information, progress updates, etc.

## Backlog Maintenance

The backlog should be regularly maintained:

1. New tasks should be added as they are identified
2. Statuses should be updated as tasks progress
3. Completed or abandoned tasks should be marked accordingly
4. The backlog should be reviewed periodically to ensure it remains relevant
5. Run `./update_index.py` after any changes to update the index file

## Integration with GitHub Issues

Tasks can be synchronized with GitHub issues:

- For tasks that have corresponding GitHub issues, include the issue number in the task file
- When creating a new GitHub issue for an existing backlog item, update the task file with the issue number
- Include backlog ID in GitHub issue descriptions for cross-reference

## Advantage Over GitHub Issues Only

This local backlog system provides:

1. Easy offline access to the project roadmap
2. Better organization of tasks into categories
3. More detailed status tracking than GitHub issues alone
4. Integration with the CIP system
5. A historical record of all planned work, whether implemented or not 