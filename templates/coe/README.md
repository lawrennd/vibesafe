# Correction of Error (CoE) Documents

## What is a CoE?

A **Correction of Error (CoE)** is a lightweight, blameless post-incident retrospective
for governance and traceability failures. It identifies *why* an error occurred, classifies
its severity, and produces the right-sized corrective outputs — without bundling those
fixes into the CoE itself.

The name follows Amazon’s **Correction of Error** practice: correction is the goal;
cause analysis (5 Whys and structured incident questions) is the method.

CoEs are defined in **CIP-0016**.

## Where CoEs sit in the VibeSafe hierarchy

CoEs are **orthogonal** to the WHY→WHAT→HOW→DO hierarchy. They don't live within it —
they *examine* it and *produce* items for it.

A CoE has two parts:

1. **"What went wrong"** — a diagnostic. Not a requirement, because the mistake might *be*
   a missing requirement. It identifies *where* the hierarchy broke down.

2. **"How do we correct it"** — outputs at the appropriate level: tenet, requirement, CIP,
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

| Class | Blast radius | Analysis depth | Typical outputs |
|-------|--------------|----------------|-----------------|
| **0** | Internal only, easily reversible | Abbreviated 5 Whys / light questions OK | Short retrospective; optional backlog task |
| **1** | Maintainer/contributor workflow impact | Full incident questions + 5 Whys | CIP + backlog tasks + tests |
| **2+** | External users, deployed behaviour, customer/legal impact | Full analysis + timeline; metrics if available | CIP + remediation plan + tripwires + communication |

**Rule of thumb**: when uncertain, classify upward.

## Document structure

Aligned with Amazon’s COE anatomy, adapted for VibeSafe:

1. **Summary** (write last; stand-alone)
2. **Severity** (Class 0 / 1 / 2+)
3. **Impact**
4. **Timeline** (required Class 1+)
5. **Evidence / metrics** (optional)
6. **What happened** (proximate failure)
7. **Incident questions** (10 — Detect / Diagnose / Mitigate)
8. **5 Whys** (or more; never stop at “human error”)
9. **Traceability artifacts** missing or incorrect
10. **Follow-up outputs** (action items with owners)
11. **Checklist**

### Incident questions (the “10”)

**Detection:** When did you learn there was impact? How? How cut time-to-detect in half?

**Diagnosis:** Underlying cause? Internal activity underway? How cut time-to-diagnose in half?

**Mitigation:** When did impact return to normal? How do you know it’s restored? How was mitigation chosen? How cut time-to-mitigate in half?

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
# Fill in the template (Summary last)
# Commit the CoE
# Create follow-up CIPs/tasks/requirements as indicated by the analysis
# Link them back in the CoE's 'spawned_*' frontmatter fields
```

## VibeSafe file classification

- `coe/README.md` — VibeSafe system file (this file)
- `coe/coe_template.md` — VibeSafe system file
- `coe/YYYY-MM-DD_*.md` — **user content** (your actual CoE documents; always commit these)

## Agent prompts (LLM compatibility)

CoE guidance is installed for all supported AI assistants from one canonical source:

| Source | `templates/prompts/context-specific/coe.md` |
|--------|-----------------------------------------------|
| Cursor | `.cursor/rules/coe.mdc` |
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |

See CIP-0016 § “Agent-prompt / LLM compatibility”.

## References

- CIP-0016: `cip/cip0016.md`
- [AWS: Creating a correction of errors document](https://aws.amazon.com/blogs/mt/creating-a-correction-of-errors-document/)
- [AWS: Why you should develop a COE](https://aws.amazon.com/blogs/mt/why-you-should-develop-a-correction-of-error-coe/)
