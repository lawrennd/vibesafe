# VibeSafe

VibeSafe is a collection of standardized project management practices designed to promote consistent, high-quality development across projects.

## What's Inside

VibeSafe contains templates and configurations for two key project management systems:

1. **Code Improvement Plans (CIPs)**: A structured approach to proposing, documenting, and implementing meaningful improvements to codebases.

2. **Backlog System**: A systematic way to track tasks, issues, and improvements that need to be implemented.

## Repository Structure

This repository follows a "dogfooding" approach - VibeSafe follows its own practices while also providing templates for other projects:

```
vibesafe/
├── README.md                 # This file
├── backlog/                  # Backlog system for VibeSafe itself
│   ├── README.md             # Overview of the backlog system
│   ├── task_template.md      # Template for creating new tasks
│   ├── update_index.py       # Script to maintain the index
│   ├── index.md              # Auto-generated index of all tasks
│   ├── documentation/        # Documentation-related tasks
│   ├── infrastructure/       # Infrastructure-related tasks
│   ├── features/             # Feature-related tasks
│   └── bugs/                 # Bug-related tasks
├── cip/                      # Code Improvement Plans for VibeSafe itself
│   ├── README.md             # Overview of the CIP process
│   ├── cip_template.md       # Template for creating new CIPs
│   └── cip0001.md, etc.      # Actual CIPs for VibeSafe
├── .cursor/rules/            # Cursor rules for IDE integration
│   ├── backlog.mdc           # Rule describing the backlog system
│   └── cip.mdc               # Rule describing the CIP system
└── templates/                # Templates for other projects
    ├── backlog/              # Backlog system template
    ├── cip/                  # CIP system template
    └── .cursor/rules/        # Cursor rules templates
```

## How to Use VibeSafe in Your Project

You can integrate VibeSafe practices into your project in two main ways:

### 1. Copy the Templates

When starting a new project, copy the templates from the `templates` directory:

```bash
# Create CIP system in your project
cp -r /path/to/vibesafe/templates/cip /path/to/your/project/

# Create Backlog system in your project
cp -r /path/to/vibesafe/templates/backlog /path/to/your/project/

# Copy Cursor rules
mkdir -p /path/to/your/project/.cursor/rules
cp /path/to/vibesafe/templates/.cursor/rules/{backlog.mdc,cip.mdc} /path/to/your/project/.cursor/rules/
```

### 2. Reference Implementation

You can also look at the root level directories (outside of templates/) for examples of how VibeSafe uses its own practices.

## Benefits of Using VibeSafe

- **Consistency**: Standardized approaches to project management across different projects
- **Quality**: Structured processes leading to higher quality code and documentation
- **Efficiency**: Reduce time spent on project management setup
- **Collaboration**: Clear communication formats for team members
- **Onboarding**: Easier for new team members to understand project practices
- **Dogfooding**: VibeSafe itself uses these practices, demonstrating their effectiveness

## Customizing for Your Project

While VibeSafe provides a standardized set of practices, you can and should adapt them to your project's specific needs:

1. Copy the relevant templates to your project
2. Adjust the README files to reflect your project's specifics
3. Modify templates if needed
4. Commit these changes to your project repository

## Contributing to VibeSafe

1. Use the CIP system (in the root `/cip` directory) to propose improvements
2. Use the backlog system (in the root `/backlog` directory) to track tasks
3. Submit pull requests that follow VibeSafe practices

## License

MIT
