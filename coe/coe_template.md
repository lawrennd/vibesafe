---
id: "YYYY-MM-DD_short-description"
title: "[Brief description of the incident]"
class: 0          # Severity class: 0 (internal), 1 (workflow-impacting), 2+ (external-impacting)
owner: "[Name]"   # Single-threaded owner responsible for follow-through
status: "Open"    # Open → Analysed → Closed
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
incident_date: "YYYY-MM-DD"
spawned_cips: []          # IDs of CIPs created as follow-ups (e.g. ["001A"])
spawned_backlog: []       # IDs of backlog tasks created as follow-ups
spawned_requirements: []  # IDs of requirements created as follow-ups
tags:
  - coe
---

# CoE: [Brief description of the incident]

> **Correction of Error** (CIP-0016). CoEs are orthogonal to the WHY→WHAT→HOW→DO
> hierarchy. They examine where the hierarchy broke and produce items at the appropriate
> level to fix it. The CoE itself does not implement fixes — it produces outputs (CIPs,
> backlog tasks, requirements, tripwires) that are implemented separately.
>
> Blameless: focus on process, tooling, and design — not people.
>
> Analysis depth: Class 0 may abbreviate Timeline, Incident questions, and 5 Whys.
> Class 1+ should complete them in full.

## Summary

[Write last. Stand-alone: who/what was impacted, when, how discovered, how mitigated,
and how recurrence will be prevented. Readable without the other sections.]

## Severity

**Class**: [0 / 1 / 2+]

- Class 0 — Internal only, easily reversible. No user-facing impact.
- Class 1 — Maintainer/contributor workflow impact (not yet externally impactful).
- Class 2+ — External impact: downstream users, deployed behaviour, customer/legal exposure.

**Blast radius**: [Describe who/what was affected]

## Impact

[Who was affected and how? Internal team / contributors / downstream users / deployed systems?
Include approximate duration if known.]

## Timeline

[Bullet list of what happened and when. Required for Class 1+; optional for Class 0.]

- YYYY-MM-DD HH:MM — [event]
- YYYY-MM-DD HH:MM — [event]

## Evidence / metrics

[Optional. Validator output, git commits, install logs, screenshots, or other evidence
that supports the impact and diagnosis.]

## What happened

[1–3 sentences. Observable symptom or discovery — the proximate failure.]

## Incident questions

Adapted from Amazon’s Detect / Diagnose / Mitigate set. “Impact” means contributors,
downstream projects, installs, or external users — depending on Class.

### Detection

1. **When did you learn there was impact?**
   - [answer]
2. **How did you learn there was impact?** (validator, `whats-next`, human review, user report, …)
   - [answer]
3. **How can we reduce the time-to-detect in half?**
   - [answer]

### Diagnosis

4. **What was the underlying cause of the impact?**
   - [answer]
5. **Was an internal activity underway during the incident?** (install/update, CIP work, rule change, refactor, …)
   - [answer]
6. **How can we reduce the time-to-diagnose in half?**
   - [answer]

### Mitigation

7. **When did impact return to pre-incident levels (or when will it)?**
   - [answer]
8. **How does the owner know the system/process is properly restored?**
   - [answer]
9. **How did you determine where and how to mitigate?**
   - [answer]
10. **How can we reduce the time-to-mitigate in half?**
    - [answer]

## 5 Whys

Ask why at least five times (more if needed). Do not stop at “human error” — ask why
that error was possible. Each gap should feed a follow-up output.

1. **Why** [problem statement]?
   - Because …
2. **Why** …?
   - Because …
3. **Why** …?
   - Because …
4. **Why** …?
   - Because …
5. **Why** …?
   - Because …
6. *(optional)* **Why** …?
   - Because …

**Root cause(s)**: [1–3 sentences synthesising the chain]

## Traceability artifacts missing or incorrect

[Which parts of the WHY→WHAT→HOW→DO chain were absent or wrong?]

- [ ] Missing tenet (WHY)
- [ ] Missing requirement (WHAT)
- [ ] Missing CIP (HOW)
- [ ] Missing backlog task (DO)
- [ ] Incorrect/forbidden link direction
- [ ] Template/runtime drift
- [ ] Other: [describe]

## Follow-up outputs

[Action items: improve prevention, detection, or mitigation. Implement separately;
link via frontmatter `spawned_*` fields. Each item needs an owner.]

### Backlog tasks

- [ ] [Task description] — owner: [Name] — `backlog/features/YYYY-MM-DD_task.md`

### CIPs

- [ ] [CIP description] — owner: [Name] — `cip/cipXXXX.md`

### Requirements

- [ ] [Requirement description] — owner: [Name] — `requirements/reqXXXX_name.md`

### Validation tripwires

- [ ] [Tripwire description] — owner: [Name] — `validate_vibesafe_structure.py` or `whats-next`

## Checklist

- [ ] Severity class assigned
- [ ] Single-threaded owner named
- [ ] Summary written (stand-alone)
- [ ] Impact documented
- [ ] Timeline documented (required Class 1+; optional Class 0)
- [ ] Incident questions answered (Detect / Diagnose / Mitigate)
- [ ] 5 Whys completed (abbreviated OK for Class 0; full for Class 1+)
- [ ] Missing/incorrect traceability artifacts identified
- [ ] Follow-up outputs listed with owners (and created)
- [ ] CoE status updated to Analysed once outputs are created
- [ ] CoE status updated to Closed once outputs are implemented
