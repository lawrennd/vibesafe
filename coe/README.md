# Cause of Error (CoE) Documents

## What is a CoE?

A **Cause of Error (CoE)** is a lightweight post-incident retrospective for governance
and traceability failures. It identifies *why* an error occurred, classifies its severity,
and produces the right-sized follow-up outputs — without bundling those fixes into the CoE
itself.

CoEs are defined in **CIP-0016**.

## Where CoEs sit in the VibeSafe hierarchy

CoEs are **orthogonal** to the WHY→WHAT→HOW→DO hierarchy. They don't live within it —
they *examine* it and *produce* items for it.

A CoE has two parts:

1. **"What went wrong"** — a diagnostic. Not a requirement, because the mistake might *be*
   a missing requirement. It identifies *where* the hierarchy broke down.

2. **"How do we fix it"** — outputs at the appropriate level: tenet, requirement, CIP,
   backlog task, or validation tripwire.

This is why a single CoE can spawn items at multiple levels of the hierarchy.

## When to write a CoE

Write a CoE when any of the following is discovered:

- A policy was implemented without the expected planning artifacts (missing CIP/backlog)
- A traceability break (forbidden downward links, missing required links)
- An enforcement/validator change that wasn't documented
- Template/runtime drift that could affect users on install/update
- Any workflow regression introduced by governance tooling

## Severity classes

| Class | Blast radius | Typical outputs |
|-------|-------------|-----------------|
| **0** | Internal only, easily reversible | Short retrospective note; optional backlog task |
| **1** | Maintainer/contributor workflow impact | Retrospective CIP + backlog tasks + tests |
| **2+** | External users, deployed behaviour, customer/legal impact | CIP + remediation plan + validation hooks + communication step |

**Rule of thumb**: when uncertain, classify upward.

## File naming and location

CoEs live in this `coe/` directory. Name files using the date of the incident discovery:

```
coe/YYYY-MM-DD_short-description.md
```

Examples:
```
coe/2026-01-10_missing-cip-for-governance-change.md
coe/2026-06-15_template-runtime-drift-in-validator.md
```

## Status workflow

```
Open → Analysed → Closed
```

- **Open**: CoE written, follow-up outputs not yet created
- **Analysed**: Follow-up outputs (CIPs, tasks, tripwires) created and linked
- **Closed**: All follow-up outputs implemented and verified

## Creating a CoE

```bash
cp coe/coe_template.md coe/YYYY-MM-DD_short-description.md
# Fill in the template
# Commit the CoE
# Create follow-up CIPs/tasks/requirements as indicated by the analysis
# Link them back in the CoE's 'spawned_*' frontmatter fields
```

## VibeSafe file classification

- `coe/README.md` — VibeSafe system file (this file)
- `coe/coe_template.md` — VibeSafe system file
- `coe/YYYY-MM-DD_*.md` — **user content** (your actual CoE documents; always commit these)
