# VibeSafe: A Framework for Human-AI Collaborative Software Development

> A collection of standardized project management practices designed to promote consistent, high-quality development across projects with special attention to human-AI collaboration.

[GitHub Repository](https://github.com/lawrennd/vibesafe) | [Installation Guide](https://github.com/lawrennd/vibesafe#quick-installation) | [Documentation](https://github.com/lawrennd/vibesafe/blob/main/philosophy.md)

## Overview

VibeSafe provides a lightweight yet powerful framework for structuring software projects in a way that creates explicit "information landmarks" that both humans and AI systems can reliably navigate. It combines philosophical foundations with practical tools to create shared understanding between development teams and AI assistants.

## Philosophical Foundation

The VibeSafe approach is grounded in two key research directions:

1. **[Requirements are All You Need](https://arxiv.org/abs/2405.13708)** - Exploring how end users might own the entire software development lifecycle using only natural language requirements
2. **[The Human Visual System as Metaphor for LLM Interaction](https://arxiv.org/abs/2504.10101)** - Drawing parallels between human visual perception (saccades and fixations) and how LLMs process information

These foundations inform VibeSafe's approach to creating explicit documentation patterns that make thinking visible and provide shared reference points for humans and AI systems.

[Read the full philosophy →](https://github.com/lawrennd/vibesafe/blob/main/philosophy.md)

## Core Components

VibeSafe consists of four integrated components:

### 1. Tenet System

A framework for defining and sharing project guiding principles. Tenets provide clear guidance on project values and priorities, serving as decision-making frameworks.

Key tenets include:
- [User Autonomy Over Prescription](https://github.com/lawrennd/vibesafe/blob/main/tenets/vibesafe/user-autonomy.md)
- [Simplicity at All Levels](https://github.com/lawrennd/vibesafe/blob/main/tenets/vibesafe/simplicity-of-use.md)
- [Documentation as First-Class Citizen](https://github.com/lawrennd/vibesafe/blob/main/tenets/vibesafe/documentation-first.md)
- [Self-Documentation Through Implementation](https://github.com/lawrennd/vibesafe/blob/main/tenets/vibesafe/self-documentation.md)

[View all tenets →](https://github.com/lawrennd/vibesafe/blob/main/tenets/vibesafe-tenets.md)

### 2. Code Improvement Plans (CIPs)

A structured approach to proposing, documenting, and implementing meaningful improvements to codebases. CIPs capture not just what changes will be made, but why they're needed and how they relate to the project's goals.

Recent examples:
- [CIP-0007: Self-Documentation Through Implementation](https://github.com/lawrennd/vibesafe/blob/main/cip/cip0007.md)
- [CIP-0008: Unified Philosophy and Human-LLM Collaboration Tenets](https://github.com/lawrennd/vibesafe/blob/main/cip/cip0008.md)

[View all CIPs →](https://github.com/lawrennd/vibesafe/blob/main/cip/README.md)

### 3. Backlog System

A systematic way to track tasks, issues, and improvements, organized by category (documentation, infrastructure, features, bugs) and status (proposed, ready, in progress, completed, abandoned).

[View backlog →](https://github.com/lawrennd/vibesafe/blob/main/backlog/index.md)

### 4. Emerging Patterns

Documented patterns that emerge from VibeSafe practices, such as the "Breadcrumbs Pattern" which describes how developers leave explicit traces of their thinking processes through CIPs, tenets, and documentation.

[Read about the Breadcrumbs Pattern →](https://github.com/lawrennd/vibesafe/blob/main/patterns/breadcrumbs.md)

## The Breadcrumbs Pattern: A Deeper Look

The Breadcrumbs Pattern, an emergent practice in VibeSafe, represents a fundamental approach to creating navigable trails of thought processes throughout development. Like the fairy tale where characters leave breadcrumbs to mark their path, this pattern involves:

1. **Explicit Documentation of Thought Processes** - Capturing reasoning as it unfolds
2. **Creating Persistent Artifacts** - Using CIPs, tenets, and backlog items to record decision rationales
3. **Building Shared Context** - Creating reference points that both humans and AI can follow

This pattern manifests in several ways:

- **CIP Evolution**: Documenting not just the final solution but the journey to it
- **Tenet Formation**: Capturing how principles emerge from practice
- **Philosophy Development**: Connecting implementation decisions to theoretical foundations

The Breadcrumbs Pattern directly addresses challenges in human-AI collaboration by providing what the Human Visual System metaphor paper calls "information landmarks" - fixed reference points that enable reliable exploration of complex information spaces.

[Explore the complete Breadcrumbs Pattern documentation →](https://github.com/lawrennd/vibesafe/blob/main/patterns/breadcrumbs.md)

## Comparison with Traditional Development Approaches

| Aspect | Traditional Approach | VibeSafe Approach |
|--------|---------------------|-------------------|
| **Documentation** | Often created after code is written | Documentation is a first-class citizen, created alongside or before code |
| **Decision Records** | Ad-hoc or non-existent | Structured through CIPs with clear reasoning |
| **Principles** | Implicit or undocumented | Explicit through formal tenets |
| **Development Artifacts** | Focus on code and deliverables | Equal focus on thought processes and reasoning |
| **Knowledge Transfer** | Relies on individuals and tribal knowledge | Embedded in structured documentation patterns |
| **AI Collaboration** | Challenging due to context gaps | Enhanced through shared information landmarks |

## Implementation Examples

VibeSafe principles have been applied to several project contexts:

### 1. Installation Script Redesign

When VibeSafe needed to improve its own installation script, the process was documented in:
- [CIP-0006: Installation Script Redesign](https://github.com/lawrennd/vibesafe/blob/main/cip/cip0006.md)
- [Backlog task for implementation](https://github.com/lawrennd/vibesafe/blob/main/backlog/documentation/2025-05-05_improved-installation-script.md)

The redesign made the script more testable and maintainable by:
- Adding environment variable configuration
- Making templates self-documenting
- Improving error handling and debugging capabilities

### 2. Philosophy Integration

As VibeSafe's philosophical foundations evolved to incorporate new research, the process was documented in:
- [CIP-0008: Unified Philosophy Document and Human-LLM Collaboration Tenets](https://github.com/lawrennd/vibesafe/blob/main/cip/cip0008.md)
- [The Breadcrumbs Pattern documentation](https://github.com/lawrennd/vibesafe/blob/main/patterns/breadcrumbs.md)

This systematic approach to evolving the project's philosophical foundations demonstrates VibeSafe's practices in action.

## Key Benefits

- **Enhanced Human-AI Collaboration**: Creates explicit "information landmarks" that both humans and AI can use to orient themselves
- **Improved Documentation**: Makes tacit knowledge explicit through structured documentation patterns
- **Better Decision-Making**: Provides clear frameworks for making consistent decisions aligned with project values
- **Reduced Onboarding Time**: Makes project philosophy and practices immediately clear to new team members
- **Self-Documenting History**: Preserves the reasoning behind decisions for future reference

## Getting Started

The easiest way to integrate VibeSafe into your project is with the one-line installation script:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"
```

This adds the core VibeSafe components to your project, ready to be customized for your specific needs.

[View installation options →](https://github.com/lawrennd/vibesafe#customizing-the-installation)

## Use Cases

VibeSafe is particularly valuable for:

1. **Projects with AI Collaboration**: Teams working extensively with AI assistants to develop software
2. **Open Source Projects**: Communities needing clear documentation of decisions and principles
3. **Knowledge-Intensive Development**: Projects where preserving context and reasoning is crucial
4. **Teams with Changing Membership**: Where knowledge continuity must be maintained despite personnel changes

## Repository Structure

```
vibesafe/
├── README.md                 # Main documentation
├── philosophy.md             # Philosophical foundation
├── patterns/                 # Emerging patterns documentation
├── tenets/                   # Tenet system 
├── backlog/                  # Backlog system
├── cip/                      # Code Improvement Plans
└── templates/                # Templates for other projects
```

[View complete structure →](https://github.com/lawrennd/vibesafe#repository-structure)

## Future Directions

VibeSafe continues to evolve as both a practical tool and a philosophical framework. Current areas of exploration include:

1. **Elevating the Breadcrumbs Pattern** - Considering whether to formalize this emergent pattern as a core tenet
2. **Expanding Human-AI Collaboration Principles** - Developing more specific guidance for effective human-AI teamwork
3. **Integration with LLM-Based Development Tools** - Ensuring VibeSafe practices enhance the capabilities of AI coding assistants

## Related Research

VibeSafe builds on research into end-user software engineering, human-AI collaboration, and improved interaction paradigms for LLMs. It represents a practical implementation of ideas from academic research, creating a bridge between theory and practice.

[Learn more about the research foundations →](https://github.com/lawrennd/vibesafe/blob/main/philosophy.md)

## Contributing to VibeSafe

VibeSafe welcomes contributions from the community. Following the project's own principles, the contribution process itself is structured to maintain clarity and shared understanding.

### Ways to Contribute

1. **Use VibeSafe in Your Projects**: The most direct way to contribute is to use VibeSafe and provide feedback on what works and what doesn't.

2. **Propose Improvements Through CIPs**: If you have ideas for enhancing VibeSafe, the best approach is to create a Code Improvement Plan (CIP) that follows the [CIP template](https://github.com/lawrennd/vibesafe/blob/main/cip/cip_template.md).

3. **Add to the Backlog**: For smaller improvements or bug fixes, you can create backlog items using the [task template](https://github.com/lawrennd/vibesafe/blob/main/backlog/task_template.md).

4. **Document Emerging Patterns**: If you observe new patterns in how VibeSafe is being used, consider documenting them in the patterns directory.

5. **Suggest New Tenets**: As principles emerge from practice, they may warrant formalization as tenets following the [tenet template](https://github.com/lawrennd/vibesafe/blob/main/tenets/tenet_template.md).

### Contribution Process

1. **Fork the Repository**: Start by forking the [VibeSafe repository](https://github.com/lawrennd/vibesafe).

2. **Create a Branch**: Make your changes in a focused branch named after the improvement (e.g., `cip-new-feature` or `backlog-documentation-fix`).

3. **Follow VibeSafe Principles**: Adhere to the project's tenets, particularly "Documentation as First-Class Citizen" and "Self-Documentation Through Implementation."

4. **Submit a Pull Request**: When your changes are ready, submit a pull request with a clear description that references any relevant CIPs or backlog items.

5. **Participate in Review**: Engage constructively in the review process, which itself follows the Breadcrumbs Pattern of explicitly documenting thinking.

### Documentation Guidelines

When contributing documentation to VibeSafe:

- **Make Reasoning Explicit**: Explain not just what you're changing but why
- **Link Related Concepts**: Connect your contributions to existing tenets, CIPs, and patterns
- **Follow Markdown Standards**: Use consistent formatting to enhance readability
- **Include Examples**: Provide concrete examples of principles and patterns in action

[View detailed contribution guidelines →](https://github.com/lawrennd/vibesafe/blob/main/README.md#contributing-to-vibesafe)

## License

MIT - VibeSafe is designed to be freely adopted and adapted to fit different project needs. 