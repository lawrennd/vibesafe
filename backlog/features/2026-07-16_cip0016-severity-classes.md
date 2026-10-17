---
id: "2026-07-16_cip0016-severity-classes"
title: "CIP-0016: Finalise severity class definitions and CoE checklist"
status: "Completed"
priority: "High"
created: "2026-07-16"
last_updated: "2026-07-16"
category: "features"
related_cips: ["0016"]
owner: "Neil Lawrence"
dependencies:
  - "2026-07-16_cip0016-coe-template"
tags:
  - backlog
  - governance
  - coe
  - process
---

# Task: Finalise severity class definitions and CoE checklist

## Description

The severity classes (0, 1, 2+) are defined in CIP-0016 but need agreement
and finalisation before the template can be completed.

Specifically:
- Confirm the Class 0 / Class 1 / Class 2+ boundaries are right for VibeSafe's
  current scale (internal tool vs published project)
- Decide whether additional sub-classes are needed now or can stay deferred
- Finalise the 8-item CoE checklist (currently a draft in CIP-0016):
  - Severity class?
  - Single-threaded owner?
  - Impact (internal/workflow/user/deployed)?
  - Proximate failure?
  - Root cause?
  - Contributing factors?
  - Missing/incorrect traceability artifacts?
  - Follow-up outputs?
- Define "rule of thumb" for classifying borderline cases (classify upward is
  already stated; are there worked examples that help?)

## Acceptance Criteria

- [ ] Severity class definitions reviewed and confirmed (or updated)
- [ ] CoE checklist finalised (8 items or revised count)
- [ ] At least one worked example per class documented (can use CIP-0015 as Class 0 case)
- [ ] Updates reflected in CIP-0016

## Related

- CIP: 0016
