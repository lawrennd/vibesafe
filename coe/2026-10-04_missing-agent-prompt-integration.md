---
id: "2026-10-04_missing-agent-prompt-integration"
title: "CoE process shipped without Cursor/Claude/Codex/Copilot agent prompts"
class: 1
owner: "Neil Lawrence"
status: "Closed"
created: "2026-10-04"
last_updated: "2026-10-17"
incident_date: "2026-10-04"
spawned_cips: ["0016"]
spawned_backlog: []
spawned_requirements: []
tags:
  - coe
  - governance
  - llm
  - prompts
---

# CoE: CoE process shipped without agent-prompt integration

> **Correction of Error** (CIP-0016). Blameless: focus on process and tooling.

## Summary

CIP-0016 implemented the Correction of Error directory, template, severity classes, and
`whats-next` scanning, but did not add CoE guidance to the shared AI prompt pipeline
(`templates/prompts/context-specific/`). As a result, Cursor rules, `CLAUDE.md`,
`AGENTS.md`, and Copilot instructions knew nothing about CoEs — so LLM collaborators
could not operate the process unless they happened to open the CIP. On 2026-10-04 this
was discovered in review; the fix adds `templates/prompts/context-specific/coe.md`,
wires install generation for all platforms, documents the requirement in CIP-0016, and
records this CoE as the dogfood case.

## Severity

**Class**: 1

- Class 0 — Internal only, easily reversible. No user-facing impact.
- Class 1 — Maintainer/contributor workflow impact (not yet externally impactful).
- Class 2+ — External impact: downstream users, deployed behaviour, customer/legal exposure.

**Blast radius**: AI-assisted contributors and maintainers using Cursor, Claude Code,
Codex, or Copilot on VibeSafe — the primary collaboration surface for this project.

## Impact

LLM agents following always-applied rules for CIPs/backlog/requirements/tenets had no
equivalent CoE guidance. Open CoEs would appear in `whats-next` if someone ran it, but
agents were not prompted to understand, create, or follow through on CoEs. No known
external user-project breakage (CoE was not yet dogfooded), so Class 1 rather than 2+.

## Timeline

- 2026-01-10 — CIP-0016 created (initially as Cause of Error framing)
- 2026-07-16 — CIP-0016 Accepted; backlog tasks created; `coe/` template + `whats-next` scan implemented; status → Implemented
- 2026-10-04 — Review: rename to Correction of Error; add 5 Whys + incident questions
- 2026-10-04 — Discovery: CoE absent from agent prompts (Cursor/Claude/Codex/Copilot)
- 2026-10-04 — Mitigation: add canonical prompt + install wiring + CIP documentation + this CoE

## Evidence / metrics

- `rg` over `.cursor/rules/`, `CLAUDE.md`, `AGENTS.md`, Copilot instructions: no CoE content before fix
- CIP-0016 implementation plan listed `whats-next` integration but not agent-prompt surfaces
- Contrast: `templates/prompts/context-specific/{cip,backlog,requirements,tenets}.md` all existed

## What happened

A first-class governance process (`coe/`) was marked Implemented with template +
`whats-next` support, but without the multi-platform LLM context that other first-class
components receive via `templates/prompts/`.

## Incident questions

### Detection

1. **When did you learn there was impact?**
   - 2026-10-04, during human review of CIP-0016 LLM compatibility
2. **How did you learn there was impact?**
   - Direct question: “Is CoE status integrated in the agent prompts?” — confirmed missing by search
3. **How can we reduce the time-to-detect in half?**
   - Treat “agent prompts on all platforms” as an explicit CIP acceptance criterion / checklist item for any new first-class component; optionally add a validator warning when `cip|backlog|requirements|tenets|coe` exists without a matching `templates/prompts/context-specific/<name>.md`

### Diagnosis

4. **What was the underlying cause of the impact?**
   - CIP-0016 scoped “LLM-facing” integration as `whats-next` output only, omitting the shared prompt generation pipeline used for other components
5. **Was an internal activity underway during the incident?**
   - Yes — implementing and later refining CIP-0016 (CoE process)
6. **How can we reduce the time-to-diagnose in half?**
   - Document the platform matrix (Cursor / Claude / Codex / Copilot ← `templates/prompts/`) in CIP-0016 and in the CoE agent prompt itself so the expected surfaces are greppable and reviewable

### Mitigation

7. **When did impact return to pre-incident levels (or when will it)?**
   - 2026-10-04 once `coe.md` prompt exists and platform files are regenerated/installed
8. **How does the owner know the system/process is properly restored?**
   - `templates/prompts/context-specific/coe.md` present; `.cursor/rules/coe.mdc` generated; `CLAUDE.md` / `AGENTS.md` / Copilot instructions contain “Correction of Error”; CIP-0016 documents the requirement; `./whats-next` still lists CoEs
9. **How did you determine where and how to mitigate?**
   - Followed the existing CIP-0012-era pattern: canonical markdown under `templates/prompts/context-specific/`, generated per platform by `install-minimal.sh`
10. **How can we reduce the time-to-mitigate in half?**
    - Keep the platform matrix and file paths in CIP-0016 so future components copy a known recipe instead of rediscovering it

## 5 Whys

1. **Why** did LLMs not know about the CoE process?
   - Because CoE guidance was absent from Cursor/Claude/Codex/Copilot context files.
2. **Why** was it absent from those files?
   - Because no `templates/prompts/context-specific/coe.md` was created, so install generation never emitted CoE sections.
3. **Why** wasn’t that prompt file created when CoE was implemented?
   - Because CIP-0016’s implementation plan treated `whats-next` integration as the LLM surface and did not list the multi-platform prompt pipeline.
4. **Why** did the plan omit the prompt pipeline?
   - Because “LLM compatible” was implicitly equated with “appears in `whats-next`,” while other components’ always-applied rules were an unstated parallel path from CIP-0012.
5. **Why** was that parallel path easy to miss?
   - Because there was no checklist or tripwire requiring every new first-class directory to ship `templates/prompts/context-specific/<component>.md` (and thus all generated platforms).
6. **Why** was there no such checklist/tripwire?
   - Because the CoE process itself — which should catch governance gaps like this — had not yet been dogfooded on VibeSafe’s own tooling omissions.

**Root cause(s)**: First-class component definition lacked an explicit, enforced
“agent-prompt completeness” criterion spanning Cursor, Claude, Codex, and Copilot.
`whats-next` visibility was mistaken for full LLM compatibility.

## Traceability artifacts missing or incorrect

- [ ] Missing tenet (WHY)
- [ ] Missing requirement (WHAT)
- [x] Missing CIP (HOW) — CIP-0016 incomplete relative to LLM surfaces (now amended)
- [ ] Missing backlog task (DO)
- [ ] Incorrect/forbidden link direction
- [x] Template/runtime drift — `coe/` existed in repo without `templates/coe/` + prompt install wiring
- [x] Other: missing agent-prompt integration for a first-class process

## Follow-up outputs

### CIPs

- [x] Amend CIP-0016 with agent-prompt section + implementation step 5 — owner: Neil Lawrence — `cip/cip0016.md`

### Validation tripwires

- [ ] (Optional / deferred) Validator warning: first-class dirs without matching `templates/prompts/context-specific/<name>.md` — owner: Neil Lawrence

### Process

- [x] Add canonical prompt `templates/prompts/context-specific/coe.md` and regenerate platform artifacts — owner: Neil Lawrence
- [x] Install `coe/` system templates + explicit `coe` case in `generate_cursor_rules` — owner: Neil Lawrence

## Checklist

- [x] Severity class assigned
- [x] Single-threaded owner named
- [x] Summary written (stand-alone)
- [x] Impact documented
- [x] Timeline documented (required Class 1+; optional Class 0)
- [x] Incident questions answered (Detect / Diagnose / Mitigate)
- [x] 5 Whys completed (abbreviated OK for Class 0; full for Class 1+)
- [x] Missing/incorrect traceability artifacts identified
- [x] Follow-up outputs listed with owners (and created)
- [x] CoE status updated to Analysed once outputs are created
- [x] CoE status updated to Closed once outputs are implemented
