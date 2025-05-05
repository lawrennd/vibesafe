# VibeSafe

[![Installation Test](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml)
[![Test Coverage](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml)
[![codecov](https://codecov.io/gh/lawrennd/vibesafe/branch/main/graph/badge.svg)](https://codecov.io/gh/lawrennd/vibesafe)

VibeSafe is a collection of standardized project management practices designed to promote consistent, high-quality development across projects.

## Our Philosophy

VibeSafe's approach is rooted in a philosophy of creating shared understanding and structured collaboration between humans and AI systems. Our [philosophy document](philosophy.md) explores how VibeSafe relates to research on natural language requirements and human-LLM interactions.

We're currently exploring an evolution of this philosophy with [CIP-0008](cip/cip0008.md), which proposes unifying our philosophical foundations and introducing new tenets focused on human-AI collaboration.

## Our Tenets

VibeSafe is guided by a set of core [tenets](tenets/vibesafe-tenets.md) that shape our approach to project management:

1. **[User Autonomy Over Prescription](tenets/vibesafe/user-autonomy.md)**: *"We optimize for configurability over our own preferences."*
2. **[Simplicity at All Levels](tenets/vibesafe/simplicity-of-use.md)**: *"Simplicity matters everywhere - in usage, code, and dependencies."* We prioritize lightweight implementation with minimal dependencies.
3. **[Documentation as First-Class Citizen](tenets/vibesafe/documentation-first.md)**: *"If it's not documented, it doesn't exist."*
4
[View all tenets →](tenets/vibesafe-tenets.md)

## What's Inside

VibeSafe contains templates and configurations for three key project management systems:

1. **Code Improvement Plans (CIPs)**: A structured approach to proposing, documenting, and implementing meaningful improvements to codebases.

2. **Backlog System**: A systematic way to track tasks, issues, and improvements that need to be implemented.

3. **Tenet System**: A framework for defining, managing, and sharing project guiding principles.

## Quick Installation

VibeSafe is designed to be simple to install and use across all major platforms (Linux, macOS, and Windows). The quickest way to get started is with our one-line installation script:

```bash
# Create a new directory for your project (if needed)
mkdir my-project && cd my-project

# Install VibeSafe with the minimal installation script
bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"
```

This script will:
- Create the basic VibeSafe directory structure
- Copy template files for CIPs, backlog tasks, and tenets
- Add a starter README.md to your project

The installation requires only `bash` and `git`, with no additional dependencies. Our automated testing ensures the installation works reliably across Linux, macOS, and Windows environments.

### Customizing the Installation

The installation script supports several environment variables for customization:

```bash
# Use a custom repository URL
VIBESAFE_REPO_URL=https://github.com/your-fork/vibesafe.git bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"

# Use local templates directory
VIBESAFE_TEMPLATES_DIR=/path/to/your/templates bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"

# Skip repository cloning (use default templates)
VIBESAFE_SKIP_CLONE=true bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"

# Enable debug output
VIBESAFE_DEBUG=true bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)"
```

The script is designed to be self-documenting, with the template structure defined by the repository rather than hard-coded in the script itself. This approach makes it easy to customize and extend the template system.

## Repository Structure

This repository follows a "dogfooding" approach - VibeSafe follows its own practices while also providing templates for other projects:

```
vibesafe/
├── README.md                 # This file
├── philosophy.md             # VibeSafe's philosophical foundation
├── scripts/                  # Installation scripts
│   └── install-minimal.sh    # Minimal installation script
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
