# VibeSafe

[![Installation Test](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/installation-test.yml)
[![Test Coverage](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/lawrennd/vibesafe/actions/workflows/test-coverage.yml)
[![codecov](https://codecov.io/gh/lawrennd/vibesafe/branch/main/graph/badge.svg)](https://codecov.io/gh/lawrennd/vibesafe)

VibeSafe is a collection of standardized project management practices designed to promote consistent, high-quality development across projects.

## Our Philosophy

VibeSafe's approach is rooted in a philosophy of creating shared understanding and structured collaboration between humans and AI systems. Our [philosophy document](philosophy.md) explores how VibeSafe relates to research on natural language requirements and human-LLM interactions.

We're currently exploring an evolution of this philosophy with [CIP-0008](cip/cip0008.md), which proposes unifying our philosophical foundations and introducing new tenets focused on human-AI collaboration.

## Why the Process?

A natural reaction: "This looks like a lot of paperwork."

But the cost model is inverted when working with AI:
- **Generating documentation**: Cheap (AI does it)
- **Debugging misimplementation**: Expensive (human discovers it late)
- **Finding answers later**: Expensive (reading 50 closed CIPs to understand current state)

VibeSafe forces intent to be explicit *before* implementation—when correcting misunderstandings costs editing a markdown file, not unwinding code changes. The process isn't overhead; it's a checkpoint where humans can catch AI misinterpretation early.

After implementation, **compression** distills the development history (CIPs, backlog, commits) into streamlined formal documentation. Future developers (human and AI) understand *what* was built without reading the entire *how* it evolved. The workflow is: **WHY** (Tenets) → **WHAT** (Requirements) → **HOW** (CIPs) → **DO** (Backlog) → **DOCUMENT** (Compression).

## Emerging Patterns

Through the evolution of VibeSafe, we've observed emerging patterns that embody our philosophy in practice. Most notably, the [Breadcrumbs Pattern](patterns/breadcrumbs.md) describes how we leave explicit traces of our thinking processes through CIPs, tenets, and documentation – creating a navigable trail for both humans and AI systems.

## Our Tenets

VibeSafe is guided by a set of core [tenets](tenets/vibesafe-tenets.md) that shape our approach to project management:

1. *[User Autonomy Over Prescription](tenets/vibesafe/user-autonomy.md)*: *"We optimize for configurability over our own preferences."*
2. *[Simplicity at All Levels](tenets/vibesafe/simplicity-of-use.md)*: *"Simplicity matters everywhere - in usage, code, and dependencies."* We prioritize lightweight implementation with minimal dependencies.
3. *[Documentation and Implementation as a Unified Whole](tenets/vibesafe/documentation-as-code.md)*: *"Document to guide implementation; implement to validate documentation."*

[View all tenets →](tenets/vibesafe-tenets.md)

## Framework Independence

**VibeSafe works with any AI coding assistant** – whether you use Cursor, Claude Code, GitHub Copilot, Codex, Cody, or any other AI assistant, VibeSafe provides the same core functionality and benefits.

### Why Framework-Independent?

Following our core tenets of *User Autonomy* and *Simplicity*, VibeSafe:

- 📁 Uses **standard file formats** (Markdown + YAML) that any AI assistant can read
- 🌐 Relies on **file-based organization**, not platform-specific APIs
- 🔄 Provides **portable content** that works across different tools
- 🎯 Respects **your choice** of AI coding assistant

### How It Works

VibeSafe's components (CIPs, Backlog, Requirements, Tenets) are stored as standard markdown files with YAML frontmatter. Any AI assistant that can read project files will understand your VibeSafe structure and use it to provide context-aware suggestions.

During installation, VibeSafe generates platform-specific prompt files from a single source of truth:
- **Cursor**: `.cursor/rules/*.mdc` (multi-file with YAML frontmatter)
- **GitHub Copilot**: `.github/copilot-instructions.md` (single combined file)
- **Claude Code**: `CLAUDE.md` (project memory file)
- **Codex**: `AGENTS.md` (project documentation file)

By default, VibeSafe generates prompts for **all platforms** (respecting user autonomy). You can customize this using the `VIBESAFE_PLATFORM` environment variable (see Advanced Usage below).

See [REQ-000C](requirements/req000C_ai-assistant-framework-independence.md) and [CIP-0012](cip/cip0012.md) for our framework independence approach.

## What's Inside

VibeSafe contains templates and configurations for key project management systems:

1. An [emerging philosophy](philosophy.md) of human-AI collaboration for code and systems design.

2. *Code/Capability Improvement Plans (CIPs)*: A structured approach to proposing, documenting, and implementing meaningful improvements to codebases or other capabilities.

3. *Backlog System*: A systematic way to track tasks, issues, and improvements that need to be implemented.

4. *Tenet System*: A framework for defining, managing, and sharing project guiding principles.

5. *What's Next Script*: A project status summarizer that helps both humans and LLMs quickly understand the current state of the project and identify pending tasks.

6. *Documentation Compression*: A systematic workflow (WHY→WHAT→HOW→DO→DOCUMENT) that consolidates closed CIPs and completed implementations into permanent, accessible formal documentation. See [Compression Guide](docs/compression-guide.md), [CIP-0013](cip/cip0013.md), and [REQ-000E](requirements/req000E_documentation-synchronization.md).

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
- AI context files: `.cursor/rules/*` (and `.ai/context/*` in future releases)
- AI-Requirements framework templates

*🛡️ Always Preserved (Your Content):*
- Project README: `README.md` (root level)
- Your tasks: `backlog/features/your-task.md`, etc.
- Your CIPs: `cip0001.md`, `cip0002.md`, etc.
- Your tenets: Actual project tenet files
- Virtual environment: `.venv`
- Your requirements documents

*🔒 Automatic Version Control Protection:*
VibeSafe automatically adds system files to `.gitignore`, preventing accidental commits. This means you can safely use `git add .` without committing VibeSafe infrastructure. See [CIP-000F](cip/cip000F.md) for details.

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

# Choose AI assistant platform (CIP-0012: Framework Independence)
# Options: cursor, copilot, claude, codex, all (default: all)
VIBESAFE_PLATFORM=cursor bash install-script.sh    # Cursor only
VIBESAFE_PLATFORM=copilot bash install-script.sh   # GitHub Copilot only
VIBESAFE_PLATFORM=all bash install-script.sh       # All platforms (default)
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
├── .cursor/rules/            # AI context files for assistant integration
│   ├── backlog.mdc           # Context about the backlog system
│   └── cip.mdc               # Context about the CIP system
└── templates/                # Templates for other projects
    ├── tenets/               # Tenet system template
    ├── backlog/              # Backlog system template
    ├── cip/                  # CIP system template
    └── .cursor/rules/        # AI context files templates (works with all AI assistants)
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

# Copy AI context files (works with all AI coding assistants)
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
