# VibeSafe Tenet System

This directory contains the VibeSafe tenet system, a framework for defining, managing, and sharing project guiding principles.

## What Are Tenets?

Tenets are guiding principles that inform decision-making in a project. Unlike rigid rules, tenets are principles to consider and balance when making decisions. When different tenets come into conflict, judgment is required to determine which principles should take precedence in a specific context.

*Key characteristics of effective tenets*:

1. *Limited in number*: Typically around 7 (±2) tenets are optimal - enough to cover key principles but few enough to remember and apply consistently
2. *Central to the project*: Tenets should be at the forefront of project thinking, not an afterthought
3. *Memorable and actionable*: Easy to recall and apply in practical situations
4. *Balanced and complementary*: Together provide a comprehensive decision framework

## The Tenet System

The VibeSafe tenet system provides:

1. *Standardised Format*: A consistent structure for documenting tenets
2. *Integration with Workflows*: Ways to reference tenets in CIPs and backlog tasks
3. *Versioning*: Tracking changes to tenets over time
4. *Tooling*: Validation and visualization for tenet management
5. *Prominence*: Methods to keep tenets visible and top-of-mind

## Directory Structure

```
tenets/
├── README.md                 # This file
├── tenet_template.md         # Template for creating new tenets
├── combine_tenets.py         # Script to combine individual tenets
├── vibesafe/                 # VibeSafe's own tenets as example
│   ├── user-autonomy.md      # Individual tenet files
│   ├── simplicity-of-use.md
│   └── ...
├── vibesafe-tenets.md        # Combined tenets document (generated)
└── vibesafe-tenets.yaml      # Machine-readable tenets (generated)
```

## How to Use Tenets

### Creating Tenets

1. Start with a small set of tenets (5-7 is ideal)
2. Create a directory for your project's tenets (e.g., `tenets/myproject/`)
3. Copy the `tenet_template.md` file for each tenet into your directory
4. Use clear, concise language
5. Include specific examples and counter-examples
6. Consider potential conflicts with other tenets
7. Run the combination script to generate the combined document

### Individual Tenet Files

Each tenet should be stored in its own file following the template format. This approach offers several benefits:

1. *Clear versioning*: Each tenet can be versioned independently
2. *Focused editing*: Easier to update a specific tenet
3. *Better collaboration*: Reduces merge conflicts when multiple people edit tenets
4. *Reusability*: Tenets can be easily shared and reused across projects

### Generating Combined Documents

Use the `combine_tenets.py` script to generate:

1. A combined Markdown document containing all tenets
2. A YAML representation for machine processing

Example:
```bash
python tenets/combine_tenets.py
```

### Placing Tenets at the Forefront

Tenets should be central to your project, not an afterthought:

1. Link to tenets from your main project README
2. Reference them in onboarding documentation
3. Include tenet discussions in project meetings
4. Use them actively in decision-making processes 
5. Consider displaying them prominently in project spaces
6. Introduce them early when explaining the project

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
5. Maintain the small, focused set - when adding a new tenet, consider if an existing one can be removed

## Example Tenet Usage

Here's how referencing tenets might look in a CIP:

```markdown
## Tenet Alignment

This proposal aligns with the following tenets:

- *User Autonomy* - Provides configuration options rather than a fixed approach
- *Simplicity of Use* - Offers simple defaults for common cases

It balances these tenets by starting with sensible defaults while allowing 
customization for advanced users.
```

## Implementing in Your Project

To implement the tenet system in your project:

1. Copy the `tenets` directory structure
2. Create a subdirectory for your project's tenets
3. Adapt the `tenet_template.md` to your needs
4. Define your own project tenets (remember: approximately 7)
5. Run the combination script to generate the combined documents
6. Add tenets to your main README and documentation
7. Update your CIP and backlog templates to reference tenets 