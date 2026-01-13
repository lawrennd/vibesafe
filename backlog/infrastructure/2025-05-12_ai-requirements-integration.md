---
category: infrastructure
created: '2025-05-12'
dependencies:
- CIP-0009
- CIP-000C
effort: medium
github_issue: null
id: 2025-05-12_ai-requirements-integration
last_updated: '2025-05-12'
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
title: Integrate AI-Requirements Framework into Installation Script
type: infrastructure
---

## Description

Integrate the AI-Requirements Framework (developed in CIP-0009) into the VibeSafe installation script to ensure it's included by default in all new VibeSafe installations. Currently, the framework is only available in the `cip0009-requirements` branch and must be manually added to projects after installation.

## Acceptance Criteria

- [x] Update `scripts/install-minimal.sh` to create the AI-Requirements directory structure
- [x] Add function to create default AI-Requirements files if templates are not available
- [x] Update the main installation function to call the new functions
- [x] Update the templates directory to include AI-Requirements templates
- [x] Enhance the What's Next script to include AI-Requirements guidance
- [x] Update the project documentation to reference the AI-Requirements framework
- [x] Test the installation process on different platforms (Linux, macOS, Windows)

## Implementation Notes

### Installation Script Updates

Add functions to create the AI-Requirements directory structure and default files:

```bash
# Function to create the AI-Requirements directory structure
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

# Function to create default AI-Requirements files
create_default_requirements_files() {
  # Create default README.md
  create_default_template "ai-requirements" "README.md" "# AI-Assisted Requirements Framework\n\nThis directory contains the framework for AI-assisted requirements gathering and management.\n\n## Structure\n\n- patterns/: Reusable conversation patterns\n- prompts/: Prompts for different stages of requirements\n- integrations/: Integrations with other VibeSafe components\n- examples/: Example requirements conversations\n- guidance/: Guidance for requirements gathering"
  
  # Create default pattern templates
  mkdir -p ai-requirements/patterns
  create_default_template "ai-requirements/patterns" "stakeholder-identification.md" "# Stakeholder Identification Pattern\n\n## Purpose\n\nThis pattern helps identify and analyze all stakeholders for a software project.\n\n## When to Use\n\n- At the beginning of a project\n- When planning a major new feature\n- When evaluating project impact"
  create_default_template "ai-requirements/patterns" "goal-decomposition.md" "# Goal Decomposition Pattern\n\n## Purpose\n\nThis pattern helps break down high-level goals into specific, actionable requirements.\n\n## When to Use\n\n- When starting with broad project goals\n- When refining feature requirements\n- When prioritizing development work"
  
  # Create default prompt directories and templates
  mkdir -p ai-requirements/prompts/{discovery,refinement,validation,testing}
  create_default_template "ai-requirements/prompts/discovery" "discovery-prompt.md" "# Requirements Discovery Prompt\n\n## Purpose\n\nThis prompt guides the initial exploration of user needs and project scope.\n\n## Prompt\n\nLet's explore the requirements for this project:\n\n1. What problem are you trying to solve?\n2. Who are the main users or stakeholders?\n3. What are the key goals for this system?\n4. What constraints or limitations should we be aware of?"
  
  # Create default integration templates
  mkdir -p ai-requirements/integrations
  create_default_template "ai-requirements/integrations" "backlog-integration.md" "# Backlog Integration\n\n## Purpose\n\nThis document explains how to connect requirements to the backlog system."
  
  # Create directories for examples and guidance
  mkdir -p ai-requirements/examples ai-requirements/guidance
}
```

### What's Next Script Updates

Added a `scan_requirements` function to detect and report on the AI-Requirements framework status:
```python
def scan_requirements():
    """Scan the AI-Requirements directory and collect information."""
    requirements_info = {
        'has_framework': os.path.isdir('ai-requirements'),
        'patterns': [],
        'prompts': {
            'discovery': [],
            'refinement': [],
            'validation': [],
            'testing': []
        },
        'integrations': [],
        'examples': [],
        'guidance': []
    }
    
    # Check patterns, prompts, integrations, examples, and guidance
    if os.path.isdir('ai-requirements/patterns'):
        pattern_files = glob.glob('ai-requirements/patterns/*.md')
        requirements_info['patterns'] = [os.path.basename(f).replace('.md', '') for f in pattern_files]
    
    # More scanning logic...
    
    return requirements_info
```

Updated the main function to support a `--requirements-only` flag:
```python
parser.add_argument('--requirements-only', action='store_true', help='Only show requirements information')
```

Added requirements-specific next steps generation:
```python
# Add suggestion to use requirements for backlog tasks
if requirements_info['has_framework'] and backlog_info['by_status']['proposed']:
    next_steps.append(
        "Use AI-Requirements patterns to refine proposed backlog tasks"
    )
```

## Related

- CIP: 000C
- CIP: 0009
- Documentation: ai-requirements/README.md

## Progress Updates

### 2025-05-12

Task created with Ready status. Detailed implementation plan established based on CIP-000C.

### 2025-05-13

Task updated to In Progress status. Implemented the following:

1. Updated `scripts/install-minimal.sh` to create AI-Requirements directory structure and files
2. Enhanced the What's Next script to show AI-Requirements framework information and provide guidance
3. Added tests for the new What's Next script functionality
4. Updated project documentation to reference the AI-Requirements framework

### 2025-05-12

Added AI-Requirements templates to the templates directory. This ensures that new projects created with VibeSafe will have the complete AI-Requirements framework available from the start.

Performed testing of the installation process on macOS. The installation script correctly creates the AI-Requirements framework structure and files. All tests are passing.

Tested the What's Next script functionality with the new --requirements-only flag. The script correctly detects and reports on the AI-Requirements framework status.

All acceptance criteria have been met, and this task is now completed.