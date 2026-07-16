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

> **Note**: CoEs are orthogonal to the WHY→WHAT→HOW→DO hierarchy. They examine where
> the hierarchy broke and produce items at the appropriate level to fix it. The CoE itself
> does not implement fixes — it produces outputs (CIPs, backlog tasks, requirements,
> tripwires) that are implemented separately.

## Severity

**Class**: [0 / 1 / 2+]

- Class 0 — Internal only, easily reversible. No user-facing impact.
- Class 1 — Maintainer/contributor workflow impact (not yet externally impactful).
- Class 2+ — External impact: downstream users, deployed behaviour, customer/legal exposure.

**Blast radius**: [Describe who/what was affected]

## What happened

[1–3 sentences. What was the observable symptom or discovery?]

## Impact

[Who was affected and how? Internal team / contributors / downstream users / deployed systems?]

## Proximate failure

[What specifically broke or was missing? E.g. "Validator rule implemented without a CIP."]

## Root cause(s)

[Why did it happen? E.g. "No check existed to catch governance-sensitive changes without planning artifacts."]

## Contributing factors

[Process, tooling, or assumption gaps that made this easier to miss. E.g. "The commit hook only checked file naming, not cross-component coverage."]

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

[List what this CoE produces. Implement these separately; link them back via frontmatter fields.]

### Backlog tasks

- [ ] [Task description] — `backlog/features/YYYY-MM-DD_task.md`

### CIPs

- [ ] [CIP description] — `cip/cipXXXX.md`

### Requirements

- [ ] [Requirement description] — `requirements/reqXXXX_name.md`

### Validation tripwires

- [ ] [Tripwire description] — implement in `validate_vibesafe_structure.py` or `whats-next`

## Checklist

- [ ] Severity class assigned
- [ ] Single-threaded owner named
- [ ] Impact documented
- [ ] Proximate failure identified
- [ ] Root cause(s) identified
- [ ] Contributing factors identified
- [ ] Missing/incorrect traceability artifacts identified
- [ ] Follow-up outputs listed (and created)
- [ ] CoE status updated to Analysed once outputs are created
- [ ] CoE status updated to Closed once outputs are implemented
