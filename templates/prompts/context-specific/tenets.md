# VibeSafe Project Tenet System

> **Note**: This file provides context to AI coding assistants (Cursor, Claude Code, GitHub Copilot, etc.).
> The content is standard markdown and works with any AI assistant that can read project files.

## What Are Tenets?

Tenets are guiding principles that inform decision-making in a project. Unlike rigid rules, tenets are principles to consider and balance when making decisions. When different tenets come into conflict, judgment is required to determine which principles should take precedence in a specific context.

**Key characteristics of effective tenets**:

1. **Limited in number**: Typically around 7 (±2) tenets are optimal - enough to cover key principles but few enough to remember and apply consistently
2. **Central to the project**: Tenets should be at the forefront of project thinking, not an afterthought
3. **Memorable and actionable**: Easy to recall and apply in practical situations
4. **Balanced and complementary**: Together provide a comprehensive decision framework

## Tenet Directory Structure

The `tenets/` directory contains project guiding principles:

```
tenets/
├── README.md                 # Tenet system overview
├── vibesafe/                 # VibeSafe's own tenets
│   ├── user-autonomy.md      # Individual tenet files
│   ├── simplicity-of-use.md
│   └── ...
└── [project]/                # User's project tenets
    ├── tenet1.md
    └── tenet2.md
```

## Tenet File Format

Each tenet file uses standard markdown with four required sections:

```markdown
# Project Tenet: [Title]

## Description
[1-2 paragraphs explaining the principle, its importance, and how it guides decisions]

## Quote
*"[Memorable phrase that captures the essence of the tenet]"*

## Examples
- [Concrete example of applying this tenet]
- [Another example in a different context]
- [A third example showing broader application]

## Counter-examples
- [Example of violating this tenet]
- [Another example of what not to do]
- [A third violation example]

## Conflicts
- [Potential conflict with another tenet]
- Resolution: [How to resolve the conflict]
- [Another potential conflict]
- Resolution: [Another resolution approach]
```

## Working with Tenets

### 1. Creating New Tenets

*Rule*: Start with a small set of tenets (5-7 is ideal). More than 9 becomes hard to remember and apply.

```
✅ Create 5-7 focused tenets that cover key principles
✅ Use the tenet template for consistency
✅ Include specific examples and counter-examples
✅ Consider conflicts with other tenets
❌ Create 15+ tenets (too many to remember)
❌ Make tenets too vague or abstract
```

**Process**:
1. Copy `templates/tenets/tenet_template.md` to `tenets/[project]/[tenet-id].md`
2. Fill out all four required sections (Description, Quote, Examples, Counter-examples, Conflicts)
3. Use clear, actionable language
4. Provide concrete examples from the project
5. Commit the individual tenet file

### 2. Referencing Tenets

*Rule*: Link requirements to tenets (bottom-up), not to CIPs or backlog.

```yaml
# In requirements/req0001_example.md
---
related_tenets: ["user-autonomy", "simplicity-of-use"]
---
```

**Hierarchy**:
```
Tenets (WHY) ──informs──> Requirements (WHAT) ──guides──> CIPs (HOW) ──breaks into──> Backlog (DO)
```

**Why?** Tenets are foundational principles. Requirements state what should be true based on those principles. CIPs describe how to achieve requirements. Backlog tasks execute CIPs.

### 3. Balancing Conflicting Tenets

*Rule*: When tenets conflict, explicitly document the trade-off and resolution.

```
✅ Document in CIP: "User Autonomy" vs "Simplicity" - prioritized Simplicity here
✅ Explain rationale: "For first-time users, simplicity reduces friction"
❌ Ignore the conflict
❌ Violate a tenet without acknowledging it
```

**Example from VibeSafe**:
- **Conflict**: "Simplicity at All Levels" vs "User Autonomy Over Prescription"
- **Resolution**: Provide sensible defaults while allowing configuration

### 4. Tenet File Naming

*Rule*: Use kebab-case IDs that are memorable and descriptive.

```
✅ user-autonomy.md
✅ simplicity-of-use.md  
✅ documentation-implementation-unified.md
❌ tenet1.md
❌ UserAutonomy.md
❌ my_tenet.md
```

### 5. Updating Tenets

*Rule*: Tenets should evolve, but changes should be intentional and documented.

```
✅ Update tenet content to reflect project learning
✅ Add examples based on real project decisions
✅ Refine wording for clarity
❌ Change fundamental meaning without discussion
❌ Delete tenets without understanding impact
```

**Process**:
1. Edit the individual tenet file
2. Document why the change was made (in commit message)
3. Consider impact on existing requirements/CIPs that reference this tenet
4. Commit the updated tenet

### 6. VibeSafe's Own Tenets

*Rule*: VibeSafe's tenets are examples and guidelines, not requirements for your project.

VibeSafe's tenets (in `tenets/vibesafe/`) demonstrate the tenet system and guide VibeSafe's own development. Your project should create its own tenets based on its unique principles and constraints.

```
✅ Read VibeSafe tenets for examples of format and depth
✅ Adapt principles that resonate with your project
✅ Create new tenets specific to your domain
❌ Copy all VibeSafe tenets without consideration
❌ Feel constrained by VibeSafe's specific principles
```

### 7. Tenets in Decision-Making

*Rule*: Use tenets actively in design discussions, not as post-hoc justification.

```
✅ CIP motivation: "This aligns with our 'user-autonomy' tenet by..."
✅ Design review: "Which tenets apply to this decision?"
✅ Requirement: "This requirement stems from 'simplicity-of-use' tenet"
❌ Retrofit tenet references after decisions are made
❌ Ignore tenets during actual design process
```

## Tenet Template Structure

Each tenet should include these sections:

1. **Title** - Clear, concise tenet title (e.g., `# Project Tenet: User Autonomy Over Prescription`)
2. **Description** - 1-2 paragraphs explaining the principle and how it guides decisions
3. **Quote** - Memorable phrase capturing the essence (formatted as italic quote)
4. **Examples** - 3+ concrete examples of applying this tenet successfully
5. **Counter-examples** - 3+ examples of violating this tenet
6. **Conflicts** - Potential conflicts with other tenets and how to resolve them

The template file (`templates/tenets/tenet_template.md`) contains placeholders for all these sections.

## Benefits of the Tenet System

- **Improved decision-making**: Clear principles guide design choices
- **Better communication**: Shared understanding of project values
- **Consistency**: Decisions align with project philosophy over time
- **Onboarding**: New contributors quickly understand project principles
- **Conflict resolution**: Framework for balancing competing concerns
- **Documentation**: Rationale for decisions is preserved

## Integration with VibeSafe Components

### Requirements (WHAT)
Requirements link to tenets via `related_tenets` field:
```yaml
related_tenets: ["user-autonomy", "simplicity-of-use"]
```

### CIPs (HOW)
CIPs reference tenets in motivation and design rationale:
```markdown
## Motivation
This change aligns with our "simplicity-of-use" tenet by reducing...
```

### Backlog (DO)
Backlog tasks indirectly benefit from tenets through requirements and CIPs.

## VibeSafe File Classification

### 🔧 VibeSafe System Files (Don't commit these unless updating VibeSafe itself)
- `templates/tenets/tenet_template.md` - Template file
- `templates/tenets/README.md` - System documentation
- `.cursor/rules/*` - Cursor AI rules (all files)

### 📝 User Content (Always commit these)
- `tenets/[project]/*.md` - Your actual project tenets
- Individual tenet files following the template structure

**Tip**: Focus on committing your actual tenets (the principles you create) rather than VibeSafe infrastructure files.

