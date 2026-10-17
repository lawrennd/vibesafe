# VibeSafe Correction of Error (CoE) System

> **Note**: This file provides context to AI coding assistants (Cursor, Claude Code, GitHub Copilot, Codex, etc.).
> The content is standard markdown and works with any AI assistant that can read project files.

## What is a CoE?

A **Correction of Error (CoE)** is a lightweight, blameless post-incident retrospective for governance and traceability failures. It identifies *why* an error occurred, classifies severity, and produces right-sized corrective outputs — without bundling those fixes into the CoE itself.

The name follows Amazon’s **Correction of Error** practice: correction is the goal; cause analysis (5 Whys and structured incident questions) is the method.

CoEs are defined in **CIP-0016**.

## Where CoEs sit in the VibeSafe hierarchy

CoEs are **orthogonal** to the WHY→WHAT→HOW→DO hierarchy. They don't live within it — they *examine* it and *produce* items for it.

```
Tenets (WHY) → Requirements (WHAT) → CIPs (HOW) → Backlog (DO)
```

A CoE has two parts:

1. **"What went wrong"** — a diagnostic. Not a requirement, because the mistake might *be* a missing requirement. It identifies *where* the hierarchy broke down.
2. **"How do we correct it"** — outputs at the appropriate level: tenet, requirement, CIP, backlog task, or validation tripwire.

## When to Write a CoE

Write a CoE when any of the following is discovered:

- A policy was implemented without the expected planning artifacts (missing CIP/backlog)
- A traceability break (forbidden downward links, missing required links)
- An enforcement/validator change that wasn't documented
- Template/runtime drift that could affect users on install/update
- Any workflow regression introduced by governance tooling
- A new first-class VibeSafe component shipped without agent-prompt integration (Cursor / Claude / Codex / Copilot)

## Severity Classes

| Class | Blast radius | Analysis depth | Typical outputs |
|-------|--------------|----------------|-----------------|
| **0** | Internal only, easily reversible | Abbreviated 5 Whys / light questions OK | Short retrospective; optional backlog task |
| **1** | Maintainer/contributor workflow impact | Full incident questions + 5 Whys | CIP + backlog tasks + tests |
| **2+** | External users, deployed behaviour, customer/legal impact | Full analysis + timeline; metrics if available | CIP + remediation + tripwires + communication |

**Rule of thumb**: when uncertain, classify upward.

## Document Structure

Aligned with Amazon’s COE anatomy, adapted for VibeSafe:

1. Summary (write last; stand-alone)
2. Severity (Class 0 / 1 / 2+)
3. Impact
4. Timeline (required Class 1+)
5. Evidence / metrics (optional)
6. What happened (proximate failure)
7. Incident questions (10 — Detect / Diagnose / Mitigate)
8. 5 Whys (or more; never stop at “human error”)
9. Traceability artifacts missing or incorrect
10. Follow-up outputs (action items with owners)
11. Checklist

### Incident Questions (the “10”)

**Detection**
1. When did you learn there was impact?
2. How did you learn there was impact? (validator, `whats-next`, human review, user report, …)
3. How can we reduce the time-to-detect in half?

**Diagnosis**
4. What was the underlying cause of the impact?
5. Was an internal activity underway during the incident? (install/update, CIP work, rule change, refactor, …)
6. How can we reduce the time-to-diagnose in half?

**Mitigation**
7. When did impact return to pre-incident levels (or when will it)?
8. How does the owner know the system/process is properly restored?
9. How did you determine where and how to mitigate?
10. How can we reduce the time-to-mitigate in half?

### 5 Whys

Ask why at least five times (more if needed). Do not stop at “human error” — ask why that error was possible. Each gap should feed a follow-up output (prevention, detection, or faster mitigation).

## Directory Structure and Naming

```
coe/
├── README.md              # System overview
├── coe_template.md        # Template
└── YYYY-MM-DD_*.md        # User CoE documents
```

Name files by incident discovery date:

```
coe/YYYY-MM-DD_short-description.md
```

## Status Workflow

```
Open → Analysed → Closed
```

- **Open**: CoE written, follow-up outputs not yet created
- **Analysed**: Follow-up outputs (CIPs, tasks, tripwires) created and linked
- **Closed**: All follow-up outputs implemented and verified

## Creating a CoE

```bash
cp coe/coe_template.md coe/YYYY-MM-DD_short-description.md
# Fill in the template (Summary last)
# Create follow-up CIPs/tasks/requirements as indicated
# Link them in the CoE's spawned_* frontmatter fields
```

## For AI Assistants

When working in a VibeSafe project:

1. Run `./whats-next` — open/analysed CoEs appear alongside CIPs and backlog
2. Treat open CoEs as high-priority follow-through (create spawned outputs; move to Analysed)
3. Do not implement fixes inside the CoE document — spawn backlog/CIP/requirement/tripwire items
4. Keep CoEs blameless: critique process and tooling, not people
5. Scale ceremony by class: abbreviated Class 0; full questions + 5 Whys for Class 1+
6. Pause for human ownership: every CoE needs a single-threaded human `owner`

### Natural Breakpoints

1. After drafting a CoE (status: Open) → pause for human review of severity and ownership
2. After creating follow-up outputs (Open → Analysed) → pause before implementing them
3. After follow-ups are done (Analysed → Closed) → pause; ask whether related CIPs need compression

## Agent-Prompt Integration Requirement

Any new **first-class** VibeSafe component (directory + process like `cip/`, `backlog/`, `requirements/`, `tenets/`, `coe/`) must ship LLM context on **all** supported platforms via the shared prompt source:

| Platform | Generated artifact |
|----------|-------------------|
| Cursor | `.cursor/rules/<component>.mdc` |
| Claude Code | section in `CLAUDE.md` |
| Codex | section in `AGENTS.md` |
| GitHub Copilot | section in `.github/copilot-instructions.md` |

**Canonical source**: `templates/prompts/context-specific/<component>.md`  
(Install generates the platform files via `generate_prompts_for_platform` in `scripts/install-minimal.sh`.)

Shipping the directory/template/`whats-next` scan without this prompt layer is itself a CoE-worthy process gap.

## VibeSafe File Classification

### 🔧 VibeSafe System Files (Don't commit unless updating VibeSafe)
- `coe/README.md` - System documentation
- `coe/coe_template.md` - Template file
- `templates/prompts/context-specific/coe.md` - Canonical agent prompt
- `.cursor/rules/coe.mdc`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md` - Generated AI context

### 📝 User Content (Always commit)
- `coe/YYYY-MM-DD_*.md` - Actual CoE documents

## References

- CIP-0016: `cip/cip0016.md`
- Template: `coe/coe_template.md`
- [AWS: Creating a correction of errors document](https://aws.amazon.com/blogs/mt/creating-a-correction-of-errors-document/)
