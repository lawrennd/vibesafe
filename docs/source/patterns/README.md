# VibeSafe Thinking Patterns

This directory contains optional thinking patterns for requirements discovery and analysis. These are **VibeSafe guidance documents**, not required project structure.

## What Are Patterns?

Patterns are structured approaches to common requirements challenges. They're thinking tools to consult when you're stuck, not mandatory processes to follow.

## Available Patterns

### Goal Decomposition
**Purpose**: Break down high-level goals into specific, actionable requirements

**When to use**:
- You have a broad goal but unclear how to achieve it
- You need to translate abstract objectives into concrete features
- You want to ensure requirements trace back to project goals

**File**: [`goal-decomposition.md`](./goal-decomposition.md)

### Stakeholder Identification
**Purpose**: Identify all relevant stakeholders and understand their needs

**When to use**:
- Starting a new project or feature
- Requirements seem incomplete or one-sided
- You need to understand different user perspectives
- Conflicts arise between different user groups

**File**: [`stakeholder-identification.md`](./stakeholder-identification.md)

## How to Use Patterns

### 1. Consult When Stuck

Patterns are reference materials, not mandatory steps:

```
✅ "I'm not sure how to break down this goal" → Check Goal Decomposition pattern
✅ "Who else might be affected by this?" → Check Stakeholder Identification pattern
❌ "I must follow all 7 steps of Goal Decomposition for every requirement"
```

### 2. Adapt to Your Context

Patterns provide structure, not rigid rules:

- Use the parts that help
- Skip the parts that don't apply
- Combine patterns as needed
- Create your own variations

### 3. Focus on Outcomes

Patterns help you think, not create documentation:

- **Goal**: Better requirements
- **Not the goal**: Completed pattern worksheets

## Integration with VibeSafe

Patterns support the requirements process:

```
Tenets (WHY) → Requirements (WHAT) → CIPs (HOW) → Backlog (DO)
                     ↑
              Patterns help here
```

**Patterns help you**:
- Discover what requirements you need (WHAT)
- Understand why those requirements matter (WHY - link to tenets)
- Avoid confusing requirements (WHAT) with implementation (HOW)

## Pattern vs Process

| Aspect | Pattern (This Directory) | Process (VibeSafe System) |
|--------|-------------------------|---------------------------|
| **Purpose** | Thinking tool | Workflow structure |
| **Usage** | Optional reference | Required for organization |
| **Location** | `docs/patterns/` | `requirements/`, `cip/`, `backlog/` |
| **Audience** | When you're stuck | Always |
| **Example** | "How to decompose goals" | "Requirements use YAML frontmatter" |

## Adding New Patterns

If you discover a useful thinking pattern:

1. Document it in this directory
2. Follow the existing pattern structure:
   - Purpose
   - When to use
   - Pattern structure
   - Example questions
   - Common pitfalls
3. Add it to this README

## References

- **Requirements Process**: See `requirements/README.md`
- **WHAT vs HOW Guide**: See `.cursor/rules/requirements_rule.mdc`
- **VibeSafe Documentation**: See main `README.md`


