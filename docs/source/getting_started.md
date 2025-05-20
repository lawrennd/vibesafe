# Getting Started with VibeSafe

VibeSafe is designed to help teams maintain consistent development practices through a set of well-defined tenets, patterns, and tools. This guide will help you get started with VibeSafe in your project.

## Installation

The simplest way to get started with VibeSafe is to use the installation script:

```bash
curl -sSL https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh | bash
```

This will set up the basic VibeSafe structure in your project.

## Project Structure

After installation, your project will have the following structure:

```
.
├── backlog/          # Project backlog items
├── cip/             # Change Implementation Proposals
├── tenets/          # Project tenets
└── templates/       # Templates for various documents
```

## Key Concepts

### Tenets

Tenets are the fundamental principles that guide your project's development. They are stored in the `tenets/` directory and should be few in number (around 7) and placed at the forefront of your project.

### CIPs (Change Implementation Proposals)

CIPs are used to propose and track significant changes to your project. They are stored in the `cip/` directory and follow a standardized format.

### Backlog

The backlog contains all planned work items for your project. It's organized in the `backlog/` directory and can be managed using the provided tools.

## Next Steps

1. Review the :doc:`tenets` to understand the core principles
2. Explore the :doc:`patterns` for common development practices
3. Check out the :doc:`cips` to see how changes are proposed and implemented
4. Read the :doc:`api` documentation for technical details 