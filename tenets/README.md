# VibeSafe Tenet System

This directory contains the VibeSafe tenet system, a framework for defining, managing, and sharing project guiding principles.

## What Are Tenets?

Tenets are guiding principles that inform decision-making in a project. Unlike rigid rules, tenets are principles to consider and balance when making decisions. When different tenets come into conflict, judgment is required to determine which principles should take precedence in a specific context.

## The Tenet System

The VibeSafe tenet system provides:

1. **Standardized Format**: A consistent structure for documenting tenets
2. **Integration with Workflows**: Ways to reference tenets in CIPs and backlog tasks
3. **Versioning**: Tracking changes to tenets over time
4. **Tooling**: Validation and visualization for tenet management

## Directory Contents

- `README.md` - This overview file
- `tenet_template.md` - Template for creating new tenets
- `vibesafe-tenets.md` - VibeSafe's own tenets as an example
- *Future*: `tenets.yaml` - Machine-readable tenet definitions
- *Future*: Tooling for tenet validation and visualization

## How to Use Tenets

### Creating Tenets

1. Copy the `tenet_template.md` file
2. Fill in the sections for each tenet
3. Use clear, concise language
4. Include specific examples and counter-examples
5. Consider potential conflicts with other tenets

### Referencing Tenets

When making decisions or documenting work:

1. Consider which tenets apply to the situation
2. Explicitly reference relevant tenets in documentation
3. Explain how you balanced conflicting tenets
4. Use tenet IDs for machine-readable references (e.g., `user-autonomy`)

### Evolving Tenets

Tenets should evolve as the project grows and learns:

1. Update the version number when changing a tenet
2. Document the rationale for significant changes
3. Consider backward compatibility with existing references
4. Periodically review tenets for relevance and clarity

## Example Tenet Usage

Here's how referencing tenets might look in a CIP:

```markdown
## Tenet Alignment

This proposal aligns with the following tenets:

- **User Autonomy** - Provides configuration options rather than a fixed approach
- **Simplicity of Use** - Offers simple defaults for common cases

It balances these tenets by starting with sensible defaults while allowing 
customization for advanced users.
```

Or in a backlog task:

```markdown
## Implementation Notes

Implementation should prioritize the **Documentation First** tenet, ensuring 
thorough documentation before implementation begins.
```

## Implementing in Your Project

To implement the tenet system in your project:

1. Copy the `tenets` directory structure
2. Adapt the `tenet_template.md` to your needs
3. Define your own project tenets
4. Update your CIP and backlog templates to reference tenets
5. Create a tenet visualization if useful for your team 