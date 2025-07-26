---
id: "000B"
title: "VibeSafe Update Script"
status: "superseded"
created: "2025-05-11"
last_updated: "2025-07-26"
author: "Neil Lawrence"
tags:
  - "automation"
  - "tooling"
  - "installation"
  - "maintenance"
---

# CIP-000B: VibeSafe Update Script

## Status

- [x] Proposed: [2025-05-11]
- [x] Accepted: [2025-05-11]
- [x] Implemented: [2025-05-11]
- [x] Superseded by CIP-000E: [2025-07-26]

## Description

This CIP proposes the creation of an update script for VibeSafe that automatically checks for and adds missing components, keeping a VibeSafe installation up-to-date with the latest features and tools as they become available.

**⚠️ SUPERSEDED**: This CIP has been superseded by CIP-000E (Clean Installation Philosophy). With the "Install = Reinstall" approach, users can simply re-run `scripts/install-minimal.sh` to get the latest VibeSafe components, eliminating the need for a separate update script.

## Motivation

As the VibeSafe project evolves, new scripts, tools, and features are added that improve the functionality and user experience. Users who already have VibeSafe installed may not be aware of these new additions, or may find it tedious to manually update their installation. 

Currently, when a new tool like the "What's Next" script is added to VibeSafe, users with existing installations need to manually add these components. This creates friction and may lead to fragmented installations with inconsistent features.

The VibeSafe Update Script would solve this problem by providing an automated way to keep VibeSafe installations current with the latest additions.

## Implementation

The update script will:

1. Check for missing components in the VibeSafe installation
2. Add any missing scripts, tools, or features automatically
3. Preserve any local customizations while updating
4. Provide clear feedback on what has been updated

### Components to be Managed

The update script will initially manage the following components:

1. The "What's Next" script and its dependencies
2. YAML frontmatter formatting for CIPs and backlog items
3. Documentation tools and templates
4. Test frameworks and scripts

### Update Process

The update script will follow these steps:

1. Detect the current state of the VibeSafe installation
2. Compare against the latest reference version
3. Identify missing or outdated components
4. Download or create missing components
5. Update existing components if necessary
6. Run validation tests to ensure the installation is functional

### Technical Approach

The script will be implemented in Python, using the following modules:

- File system operations to check for and add missing files
- Git operations to check for updates from the remote repository
- YAML parsing for configuration and versioning
- Optional dependency on the requests library for downloading components

### User Experience

The update script will be designed with user experience in mind:

1. Simple invocation: `./vibesafe-update`
2. Clear output showing what is being updated
3. Non-destructive operation by default (with a `--force` option for overrides)
4. Ability to roll back changes if something goes wrong

## Implementation Status
- [x] Define version tracking mechanism
- [x] Create component registry of managed VibeSafe elements
- [x] Implement detection of missing components
- [x] Implement update functionality
- [x] Create tests for the update script
- [x] Document the update script usage

## References

- CIP-000A: Project Status Summarizer ("What's Next" Script)
- CIP-0006: Installation Script Redesign

## Author and Date

Author: Neil Lawrence  
Date: 2025-05-11 