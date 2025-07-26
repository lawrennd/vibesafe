# VibeSafe

[![Installation Test](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml)
[![Test Coverage](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml)
[![codecov](https://codecov.io/gh/lawrennd/vibesafe/branch/main/graph/badge.svg)](https://codecov.io/gh/lawrennd/vibesafe)

VibeSafe is a collection of standardized project management practices designed to promote consistent, high-quality development across projects.

## Our Philosophy

VibeSafe's approach is rooted in a philosophy of creating shared understanding and structured collaboration between humans and AI systems. Our [philosophy document](philosophy.md) explores how VibeSafe relates to research on natural language requirements and human-LLM interactions.

We're currently exploring an evolution of this philosophy with [CIP-0008](cip/cip0008.md), which proposes unifying our philosophical foundations and introducing new tenets focused on human-AI collaboration.

## Emerging Patterns

Through the evolution of VibeSafe, we've observed emerging patterns that embody our philosophy in practice. Most notably, the [Breadcrumbs Pattern](patterns/breadcrumbs.md) describes how we leave explicit traces of our thinking processes through CIPs, tenets, and documentation – creating a navigable trail for both humans and AI systems.

## Our Tenets

VibeSafe is guided by a set of core [tenets](tenets/vibesafe-tenets.md) that shape our approach to project management:

1. *[User Autonomy Over Prescription](tenets/vibesafe/user-autonomy.md)*: *"We optimize for configurability over our own preferences."*
2. *[Simplicity at All Levels](tenets/vibesafe/simplicity-of-use.md)*: *"Simplicity matters everywhere - in usage, code, and dependencies."* We prioritize lightweight implementation with minimal dependencies.
3. *[Documentation and Implementation as a Unified Whole](tenets/vibesafe/documentation-as-code.md)*: *"Document to guide implementation; implement to validate documentation."*

[View all tenets →](tenets/vibesafe-tenets.md)

## What's Inside

VibeSafe contains templates and configurations for three key project management systems:

1. An [emerging philosophy](philosophy.md) of human-AI collaboration for code and systems design.

2. *Code/Capability Improvement Plans (CIPs)*: A structured approach to proposing, documenting, and implementing meaningful improvements to codebases or other capabilities.

3. *Backlog System*: A systematic way to track tasks, issues, and improvements that need to be implemented.

4. *Tenet System*: A framework for defining, managing, and sharing project guiding principles.

5. *What's Next Script*: A project status summarizer that helps both humans and LLMs quickly understand the current state of the project and identify pending tasks.

## Simple Installation

VibeSafe follows the *Clean Installation Philosophy* (CIP-000E): simple, predictable installation that always works the same way.

### One-Line Installation

```bash
# Install VibeSafe in your project directory
bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"
```

### What Happens During Installation

*🔄 Install = Reinstall*  
Every installation is treated as a clean reinstall with predictable behavior:

*✅ Always Updated (VibeSafe System Files):*
- Templates: `task_template.md`, `cip_template.md`, `tenet_template.md`
- System documentation: `backlog/README.md`, `cip/README.md`, etc.
- Scripts: `whats-next`, `update_index.py`, installation scripts
- Cursor rules: `.cursor/rules/*`
- AI-Requirements framework templates

*🛡️ Always Preserved (Your Content):*
- Project README: `README.md` (root level)
- Your tasks: `backlog/features/your-task.md`, etc.
- Your CIPs: `cip0001.md`, `cip0002.md`, etc.
- Your tenets: Actual project tenet files
- Virtual environment: `.venv`
- Your requirements documents

### Requirements

- *Required*: `bash` and `git`
- *Optional*: Python 3 (for What's Next script)
- *Platforms*: Linux, macOS, Windows (Git Bash/WSL)

### Advanced Usage

```bash
# Use custom templates from your fork
VIBESAFE_REPO_URL=https://github.com/your-fork/vibesafe.git bash install-script.sh

# Use local templates directory
VIBESAFE_TEMPLATES_DIR=/path/to/templates bash install-script.sh

# Skip What's Next script installation
VIBESAFE_INSTALL_WHATS_NEXT=false bash install-script.sh
```

### Why This Approach?

- *Predictable*: You always know exactly what will happen
- *Safe*: Your content is never touched
- *Simple*: No complex options or modes
- *Always Current*: System files stay up-to-date with latest VibeSafe

## Repository Structure

This repository follows a "dogfooding" approach - VibeSafe follows its own practices while also providing templates for other projects:

```
vibesafe/
├── README.md                 # This file
├── philosophy.md             # VibeSafe's philosophical foundation
├── patterns/                 # Emerging patterns in VibeSafe practices
│   └── breadcrumbs.md        # The Breadcrumbs Pattern documentation
├── scripts/                  # Installation scripts
│   ├── install-minimal.sh    # Minimal installation script
│   └── whats_next.py         # Project status summarizer script
├── docs/                     # Documentation files
│   └── whats_next_script.md  # Documentation for the What's Next script
├── tenets/                   # Tenet system for VibeSafe itself
│   ├── README.md             # Overview of the tenet system
│   ├── tenet_template.md     # Template for creating new tenets
│   ├── combine_tenets.py     # Script to combine individual tenets
│   ├── vibesafe/             # Directory of individual tenets
│   ├── vibesafe-tenets.md    # Combined tenets document
│   └── vibesafe-tenets.yaml  # Machine-readable tenets
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
    ├── tenets/               # Tenet system template
    ├── backlog/              # Backlog system template
    ├── cip/                  # CIP system template
    └── .cursor/rules/        # Cursor rules templates
```

## Alternative Ways to Use VibeSafe

If you prefer not to use the installation script, you can integrate VibeSafe practices into your project in these ways:

### 1. Copy the Templates Manually

```bash
# Create CIP system in your project
cp -r /path/to/vibesafe/templates/cip /path/to/your/project/

# Create Backlog system in your project
cp -r /path/to/vibesafe/templates/backlog /path/to/your/project/

# Create Tenet system in your project
cp -r /path/to/vibesafe/templates/tenets /path/to/your/project/

# Copy Cursor rules
mkdir -p /path/to/your/project/.cursor/rules
cp /path/to/vibesafe/templates/.cursor/rules/{backlog.mdc,cip.mdc} /path/to/your/project/.cursor/rules/
```

### 2. Reference Implementation

You can also look at the root level directories (outside of templates/) for examples of how VibeSafe uses its own practices.

## Benefits of Using VibeSafe

- *Consistency*: Standardized approaches to project management across different projects
- *Quality*: Structured processes leading to higher quality code and documentation
- *Efficiency*: Reduce time spent on project management setup
- *Collaboration*: Clear communication formats for team members
- *Onboarding*: Easier for new team members to understand project practices
- *Dogfooding*: VibeSafe itself uses these practices, demonstrating their effectiveness

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

## Testing

VibeSafe includes a comprehensive test suite to ensure reliability across platforms:

```bash
# Run all tests
bats scripts/test/*.bats

# Run tests with coverage reporting
./scripts/run-tests-with-coverage.sh
```

For more information about testing, see [scripts/test/README.md](scripts/test/README.md).

## License

MIT

## Productivity Tools

VibeSafe includes several productivity tools to enhance your development workflow:

### What's Next Script

The [What's Next Script](docs/whats_next_script.md) helps you quickly understand the current state of your project and identify pending tasks. It provides a comprehensive overview of:

- Git repository status
- CIP (Code Improvement Proposal) status
- Backlog item status
- Recommended next steps
- Files needing YAML frontmatter

To install and use the script:

```bash
# Install the script and its dependencies (creates a virtual environment)
./install-whats-next.sh

# Run the script
./whats-next

# Show just the next steps
./whats-next --quiet
```

The script is particularly useful for LLMs working on the VibeSafe project, as it provides quick context about the project's current state and priorities.

For more information, see [docs/whats_next_script.md](docs/whats_next_script.md).

### Updating VibeSafe

With VibeSafe's Clean Installation Philosophy, updating is simple - just reinstall:

```bash
# Get the latest VibeSafe components (preserves your content)
bash <(curl -s https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)
```

This automatically updates all VibeSafe system files while preserving your project content (tasks, CIPs, project README, etc.).
