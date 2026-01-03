---
created: '2025-05-12'
id: 000C
last_updated: '2025-05-14'
status: Implemented
title: Integrate AI-Requirements Framework into Installation Script
---

# CIP-000C: Integrate AI-Requirements Framework into Installation Script

## Summary

This CIP proposes integrating the AI-Requirements Framework (from CIP-0009) into the VibeSafe installation script to ensure it's included by default in all new VibeSafe installations. 

## Status

- [ ] Proposed
- [ ] Accepted
- [x] Implemented
- [ ] Closed

## Implementation

This CIP has been implemented with the following changes:

1. Updated `scripts/install-minimal.sh` to:
   - Add function `create_default_requirements_files()` to generate default AI-Requirements files
   - Add AI-Requirements directories to the default directory structure creation
   - Update the README.md template to include AI-Requirements in the project structure

2. Enhanced the What's Next script (`scripts/whats_next.py`) to:
   - Add a `scan_requirements()` function to detect and report on the AI-Requirements framework
   - Add a `--requirements-only` flag to focus on requirements-related tasks
   - Update the next steps generation to suggest appropriate requirements-related work
   - Added comprehensive test cases for the new functionality

3. Added AI-Requirements templates to the templates directory:
   - Copied patterns, prompts, integrations, examples, and guidance files
   - Organized according to the framework structure

4. Updated documentation:
   - Updated the default README.md template to include the AI-Requirements framework
   - Updated the What's Next help text to include the `--requirements-only` flag

5. Testing:
   - Added tests for the What's Next script functionality
   - Tested the installation script on macOS
   - Verified that the AI-Requirements framework is correctly created in new projects

All implementation tasks have been completed successfully. The implementation follows the originally proposed approach with minimal changes to the existing system, ensuring backward compatibility.

## Next Steps

1. Merge the changes into the main branch
2. Create a new release that includes the AI-Requirements framework
3. Update online documentation to reflect the addition of the framework

## Context and Problem

The AI-Requirements Framework, developed under CIP-0009, provides a structured approach to gathering and managing requirements. While this framework has been implemented and tested in the `cip0009-requirements` branch, it is not included in the default VibeSafe installation. This means that new users do not automatically get the benefits of this framework unless they manually add it after installation.

Currently, the installation script creates the core project structure with CIPs, backlog, and tenets, but without the requirements framework. This creates an incomplete implementation of the VibeSafe project management approach.

## Proposal

### 1. Update Installation Script

We will update the `scripts/install-minimal.sh` installation script to include the creation of the AI-Requirements framework directory structure and templates:

```bash
create_requirements_directory_structure() {
  echo "Setting up AI-Requirements framework..."
  mkdir -p ai-requirements/{patterns,prompts/{discovery,refinement,validation,testing},integrations,examples,guidance}
  
  # Copy templates from repository if available, otherwise create defaults
  if [ -d "$templates_dir/templates/ai-requirements" ]; then
    # Copy from templates
    cp -r "$templates_dir/templates/ai-requirements/"* ai-requirements/
  else
    # Create defaults
    create_default_requirements_files
  fi
  
  echo "AI-Requirements framework set up successfully!"
}
```

The installation script will need corresponding functions to create default requirements files, similar to how it handles CIPs, backlog, and tenets.

### 2. Add Template Files to Repository

Add the AI-Requirements templates to the templates directory in the repository:

```
templates/
└── ai-requirements/
    ├── README.md
    ├── patterns/
    │   ├── stakeholder-identification.md
    │   └── goal-decomposition.md
    ├── prompts/
    │   ├── discovery/
    │   │   └── discovery-prompt.md
    │   ├── refinement/
    │   │   └── refinement-prompt.md
    │   ├── validation/
    │   │   └── validation-prompt.md
    │   └── testing/
    │       └── testing-prompt.md
    ├── integrations/
    │   ├── cip-integration.md
    │   └── backlog-integration.md
    └── examples/
        └── example-conversation.md
```

### 3. Update Documentation

Update the project documentation to reference the AI-Requirements framework:
- Add a section in the main README.md
- Update the "What's Inside" section to include the Requirements Framework
- Add documentation for how to use the Requirements Framework

### 4. Enhance What's Next Script

Enhance the What's Next script to provide guidance on using the Requirements Framework:
- Detect when requirements are needed
- Suggest using particular patterns for requirements gathering
- Remind users to check for requirements drift during implementation 
- Add a `--requirements-only` flag to focus specifically on requirements-related tasks

## Benefits

- Ensures consistent requirements gathering across projects from initial setup
- Improves alignment between requirements and implementation
- Reduces requirements drift during development
- Creates a more comprehensive project management solution
- Streamlines the installation process by including all components by default

## Alternatives Considered

### 1. Leave as a Separate Optional Installation

We could leave the Requirements Framework as a separate, optional component that users must add manually. This would allow for a more minimal core installation but would result in fragmented adoption and inconsistent practices.

### 2. Create a Separate Script for Requirements Framework

We could create a separate installation script just for the Requirements Framework. This would keep the minimal installation small, but would require an extra step and might lead to users skipping this important component.

### 3. Include in a "Full" Installation But Not in "Minimal"

We could create a "full" installation script that includes the Requirements Framework, while keeping it out of the "minimal" installation. This would offer flexibility but might confuse users about which installation to choose.

## Implementation Plan

1. Create template files for the AI-Requirements framework
2. Update the installation script with functions to create the requirements structure
3. Modify the what's next script to support the requirements workflow
4. Update documentation to reference the requirements framework
5. Test the installation process on different platforms

## Open Questions

- Should we include sample requirements documents in the templates, or just the structure?
- Should we refactor the installation script to make it more modular as part of this change?
- How much guidance should we include in the README about when and how to use the requirements framework?

## References

- [CIP-0009: Requirements Conversation Framework](cip0009.md)
- [AI-Requirements Framework Documentation](../ai-requirements/README.md)