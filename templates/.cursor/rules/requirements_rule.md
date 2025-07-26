# Requirements Process Rule

alwaysApply: true
---

# AI-Assisted Requirements Process

## What is the AI-Assisted Requirements Process?

The AI-Assisted Requirements Process is a structured approach to gathering, documenting, and managing software requirements with AI assistance. This process helps bridge the gap between natural language requirements and software implementation.

## When to Use This Rule

Apply this rule when:
- Starting a new project or feature
- Determining what to build next
- Checking the status of existing requirements
- Connecting requirements to implementation tasks
- Validating that implemented code meets requirements

## Requirements Directory Structure

The `ai-requirements/` directory follows this structure:

```
ai-requirements/
├── README.md                    # Framework overview
├── requirement_template.md      # Template for new requirements
├── prompts/                     # Conversation prompts
│   ├── discovery/               # Initial requirements discovery
│   ├── refinement/              # Detailed requirements refinement
│   ├── validation/              # Requirements validation
│   └── testing/                 # Test criteria generation
├── patterns/                    # Reusable conversation patterns
├── integrations/                # Connectors to other components
├── examples/                    # Sample requirements conversations
└── guidance/                    # Best practices and tips
```

## VibeSafe File Classification

**⚠️ IMPORTANT: VibeSafe System vs User Files**

When working with AI-Requirements, distinguish between framework files and your actual requirements:

### 🔧 VibeSafe System Files (Don't commit these unless updating VibeSafe itself)
- `ai-requirements/README.md` - Framework documentation
- `ai-requirements/requirement_template.md` - Template file
- All files in `prompts/`, `patterns/`, `integrations/`, `examples/`, `guidance/` - Framework templates
- `.cursor/rules/*` - Cursor AI rules

### 📝 User Content (Always commit these - your actual requirements)
- **Your Requirements**: Actual requirement documents you create
- **Project-Specific**: Requirements following your project's naming convention
- **Requirements Analysis**: Your analysis and refinement of requirements

**Tip**: Focus on committing your actual requirements documents, not the AI-Requirements framework files.

## Requirements Status

Requirements can have the following statuses:

- **Proposed**: Initial requirement identified but not fully defined
- **Refined**: Requirement fully described with acceptance criteria
- **Ready**: Requirement validated and ready for implementation
- **In Progress**: Currently being implemented
- **Implemented**: Implementation complete but not validated
- **Validated**: Implementation verified against acceptance criteria
- **Deferred**: Postponed to a future iteration
- **Rejected**: Will not be implemented (with explanation)

## Using the Requirements Process

### 1. Check Project Requirements Status

*Rule*: Begin by checking the overall status of project requirements.

```
✅ Use scripts/whats_next.py --requirements-only to check requirements status
✅ Review AI-Requirements directory structure for completeness
✅ Identify which requirements patterns and prompts are available
```

### 2. Requirements Discovery

*Rule*: Use discovery prompts to identify new requirements.

```
✅ Start with prompts/discovery/general.md for initial requirements gathering
✅ Use the stakeholder-identification pattern to identify all relevant users
✅ Document discovered requirements using the requirement_template.md
```

### 3. Requirements Refinement

*Rule*: Refine requirements with specific prompts.

```
✅ Use prompts/refinement/*.md to develop detailed requirements
✅ Apply the goal-decomposition pattern to break high-level goals into actionable requirements
✅ Ensure each requirement has clear acceptance criteria
```

### 4. Requirements Validation

*Rule*: Validate requirements for consistency and completeness.

```
✅ Use prompts/validation/*.md to validate requirements
✅ Check for conflicts between requirements
✅ Verify requirements are testable
```

### 5. Integration with Implementation

*Rule*: Connect requirements to implementation tasks.

```
✅ Create CIPs for major features based on requirements
✅ Create backlog items for individual requirements
✅ Reference requirements in CIPs and backlog items
```

### 6. Status Synchronization

*Rule*: Keep requirements status in sync with implementation status.

| Requirements Status | CIP Status | Backlog Status |
|--------------------|------------|----------------|
| Proposed | Not Created | Not Created |
| Refined | Not Created | Not Created |
| Ready | Proposed | Proposed/Ready |
| In Progress | Accepted/Implemented | In Progress |
| Implemented | Implemented | Completed |
| Validated | Closed | Completed |
| Deferred | - | Abandoned (with explanation) |
| Rejected | - | Abandoned (with explanation) |

### 7. Requirements Template Usage

*Rule*: Follow the standard template for requirement documentation.

```
✅ Use YAML frontmatter for metadata
✅ Include detailed description and acceptance criteria
✅ Document relationships to other project components
✅ Keep implementation status up to date
```

## Benefits of Following the Requirements Process

- *Improved understanding* of what needs to be built
- *Better traceability* between requirements and implementation
- *Reduced rework* by validating requirements before implementation
- *Higher quality* through clear acceptance criteria
- *Better communication* among technical and non-technical stakeholders 