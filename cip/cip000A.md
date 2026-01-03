---
author: Neil Lawrence
created: '2025-05-11'
id: 000A
last_updated: '2025-05-11'
status: Implemented
tags:
- project-management
- automation
- tooling
title: Project Status Summarizer ("What's Next" Script)
---

# CIP-000A: Project Status Summarizer ("What's Next" Script)

## Status

- [ ] Proposed: [2025-05-11]
- [ ] Accepted
- [x] Implemented: [2025-05-11]
- [ ] Closed

## Summary
Create a "what's next" script that summarizes the current project status and identifies pending tasks for an LLM, enabling it to quickly understand project context and prioritize future work.

## Motivation
LLMs working on the project need a comprehensive way to:
1. Understand the current project state
2. Identify high-priority tasks
3. See open CIPs and backlog items
4. Track overall project progress

This script will reduce onboarding time for LLMs, ensure consistent awareness of project status, and help maintain forward momentum by clearly identifying next steps.

## Detailed Description
The "what's next" script will be a comprehensive tool that:

1. Summarizes git status (current branch, recent commits)
2. Lists open CIPs and their current implementation status
3. Shows pending backlog items by priority
4. Highlights missing metadata in CIPs and backlog items
5. Provides recommended next actions based on project priorities

The script will standardize CIP and backlog item formats by identifying files lacking YAML frontmatter that includes required metadata fields, making it easier to programmatically parse and analyze these documents. Rather than automatically migrating existing files to include YAML frontmatter, the script will flag files that need updates, allowing LLM assistance to handle these updates on a case-by-case basis.

## Implementation Options

### Option 1: Python Script

A Python script that parses markdown files, Git status, and generates a comprehensive summary.

#### Pros
- Python's markdown and YAML libraries make parsing straightforward
- Python is widely used and maintainable
- Can be extended easily with additional features

#### Cons
- Requires Python installation
- More complex to develop initially

### Option 2: Shell Script

A shell script using tools like grep, sed, and awk to extract information.

#### Pros
- No dependencies beyond standard Unix tools
- Simpler initial implementation
- Native integration with Git commands

#### Cons
- More challenging to parse structured data like YAML frontmatter
- Less maintainable for complex operations
- Limited cross-platform compatibility

### Option Comparison

| Feature | Python Script | Shell Script |
|---------|---------------|--------------|
| Ease of Development | ★★ | ★★★ |
| Maintainability | ★★★ | ★ |
| Parsing Capabilities | ★★★ | ★ |
| Extensibility | ★★★ | ★★ |
| Dependency Requirements | ★★ | ★★★ |

## Selected Approach

Based on the above analysis, the Python Script (Option 1) has been selected because:

1. It offers superior parsing capabilities for structured data like YAML and markdown
2. It provides better maintainability for future extensions
3. The project likely already has Python available in its environment
4. The complexity advantages outweigh the dependency requirements

## Implementation Plan

1. **Define YAML Frontmatter Standards**:
   - Design standardized YAML frontmatter for CIPs
   - Design standardized YAML frontmatter for backlog items
   - Document these standards

2. **Create Python Script Components**:
   - Git status and log parser
   - CIP document parser with YAML frontmatter support
   - Backlog item parser with YAML frontmatter support
   - Project status summarizer
   - "Next steps" recommendation engine

3. **Documentation and Integration**:
   - Add documentation for the "what's next" script
   - Document YAML frontmatter standards
   - Integrate with project workflow
   - Create usage examples

## Backward Compatibility
This change will require updating existing CIPs and backlog items to include YAML frontmatter. Instead of automated migration, the script will identify documents without proper frontmatter and list them as action items. LLM assistance will be used to add frontmatter to individual files as needed, allowing for contextual understanding and appropriate metadata extraction.

## Testing Strategy
- Unit tests for each parser component
- Integration tests using sample CIPs and backlog items
- End-to-end tests verifying script output against expected project status

## Documentation Plan

1. **User documentation**:
   - Instructions for running the "what's next" script
   - How to interpret the output
   - YAML frontmatter standards documentation
   - Procedure for ensuring CIPs and backlog items have correct metadata

2. **Developer documentation**:
   - YAML frontmatter schema specifications
   - How to extend the script functionality
   - How the recommendation system works

3. **Integration documentation**:
   - How this script fits into the overall project workflow
   - Best practices for using the script with LLMs

## Implementation Status
- [x] Define YAML frontmatter standards for CIPs and backlog items
- [x] Create Python script for parsing Git status/logs
- [x] Create Python script for parsing CIPs with YAML support
- [x] Create Python script for parsing backlog items with YAML support
- [x] Implement project status summarizer
- [x] Implement "next steps" recommendation engine
- [x] Document the "what's next" script usage
- [x] Write tests for all components

## References
- [Backlog System Documentation](../backlog/README.md)
- [CIP Process Documentation](./README.md)

## Author
Neil Lawrence

## Date
2025-05-11