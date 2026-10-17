---
author: "Neil Lawrence"
created: "2026-10-17"
id: "001A"
last_updated: "2026-10-17"
status: "In Progress"
compressed: false
related_requirements:
  - "0011"  # Optional GitHub Collaboration Surface in Project Status
  - "0005"  # Clear Understanding of Project Status
related_cips:
  - "000A"  # Project Status Summarizer ("What's Next")
  - "0011"  # Framework simplification (rejected full replace-by-GitHub)
  - "0017"  # Local function hooks for whats-next
tags:
  - cip
  - github
  - whats-next
  - frontmatter
  - collaboration
title: "Optional GitHub Issues, PRs, and Discussions Integration"
---

# CIP-001A: Optional GitHub Issues, PRs, and Discussions Integration

> **Note**: CIPs describe HOW to achieve requirements (WHAT).
> Use `related_requirements` to link to the requirements this CIP implements.

> **Compression Metadata**: The `compressed` field tracks whether this CIP's key decisions have been compressed into formal documentation. Set to `false` by default. After closing a CIP and updating formal documentation with its essential outcomes, set `compressed: true`.

## Status

- [x] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work (2026-10-17)
- [x] In Progress - Actively being implemented (2026-10-17)
- [ ] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Add an optional bridge from VibeSafe planning artifacts to GitHub Issues, Pull Requests, and Discussions: declare links in YAML frontmatter, and when `gh` is available and authenticated against a GitHub remote, enrich `whats-next` with resolved titles/states. GitHub remains optional; VibeSafe remains the planning source of truth.

**Which requirements does this CIP address?** REQ-0011 (primary), REQ-0005 (status clarity).

## Motivation

Many VibeSafe projects already live on GitHub. Review, CI, and external collaboration happen in Issues, PRs, and Discussions, while planning lives in CIPs, backlog, requirements, and CoEs. Today those worlds barely connect:

1. Backlog docs mention optional `github_issue`, but templates are inconsistent and CIP/CoE frontmatter has no parallel fields.
2. Body “Related → PRs” prose is invisible to `whats-next` and validators.
3. Restoring context requires manually checking GitHub after reading local status.

CIP-0011 correctly rejected *replacing* VibeSafe with GitHub Issues. This CIP does the complementary thing: **link and surface**, never require or sync status bidirectionally.

## Detailed Description

### Design Principles

1. **Bridge, not replacement** — VibeSafe owns WHY→WHAT→HOW→DO status; GitHub is a collaboration surface.
2. **Zero cost when absent** — no GitHub remote, no `gh`, or failed auth → skip GitHub sections with no error (same spirit as CIP-0017 hooks).
3. **Frontmatter is canonical** — machine-readable IDs in YAML; body “Related” sections may mirror for humans.
4. **Read-only from `whats-next`** — resolve and display; do not create/close GitHub items or rewrite VibeSafe status from GitHub state.
5. **Flat fields, lists preferred** — extend the existing `github_issue` convention rather than inventing a nested schema that breaks old files.
6. **No new Python dependencies** — shell out to `gh` only; mock `gh` in tests.

### Frontmatter Schema

Optional on **CIP**, **backlog**, and **CoE** templates (requirements: optional discussion links only if useful; not required by this CIP’s v1 templates):

```yaml
github_issues: [42]          # preferred
github_issue: 42             # legacy alias; treat as github_issues: [42]
github_prs: [101, 102]
github_discussions: [7]
```

**Normalization rules**:
- Accept int or list of ints for each field.
- Empty string / null / `N/A` → treat as absent (compat with existing backlog noise).
- Validators warn on non-integer values; do not fail the whole project for optional fields.

**Typical usage**:

| Artifact | Typical links |
|----------|----------------|
| Backlog | `github_issues` (external work tracking) |
| CIP | `github_discussions` (design), `github_prs` (implementation) |
| CoE | `github_issues` or `github_discussions` (incident thread) |
| Requirements | usually none |

### Eligibility Probe

`whats-next` enables GitHub enrichment only when all hold:

1. `gh` is on `PATH`
2. `git remote get-url origin` (or configured remote) looks like GitHub (`github.com` or GitHub Enterprise host if detectable)
3. `gh auth status` exits successfully

CLI flag: `--no-github` (parallel to `--no-git`).

### `whats-next` Behaviour

**Layer 1 — Linked enrichment (v1, required for this CIP)**  
For each scanned CIP/backlog/CoE with GitHub IDs, call `gh` (e.g. `gh issue view`, `gh pr view`, `gh api` for discussions) and show compact state next to the artifact (number, title, open/closed/merged). Soft next-steps only, for example:

- In Progress CIP with open PR → note PR readiness / review
- Open issue linked from Completed backlog → suggest closing the issue or clearing the link (hint, not auto-action)

**Layer 2 — Repo glance (v1 optional / v1.1)**  
Compact list of open PRs for the repo; optionally open issues with a conventional label (e.g. `vibesafe`) if that label exists. Do **not** dump the full issue tracker.

**Performance**: Cap concurrent/`gh` calls; cache within a single `whats-next` run; skip Layer 2 if Layer 1 already used a generous budget. Prefer staying near REQ-0005’s “fast enough” spirit; network may exceed 2s — document that GitHub enrichment can be slower and is skippable via `--no-github`.

### Template and Docs Updates

- `templates/backlog/task_template.md` (+ installed `backlog/task_template.md` via install path): add optional frontmatter fields; keep body Related as human mirror.
- `templates/cip/cip_template.md` / `cip/cip_template.md`: same.
- `templates/coe/coe_template.md` / `coe/coe_template.md`: same.
- Docs: `docs/source/yaml_frontmatter_examples.md` — document lists + legacy `github_issue`.
- Agent prompts (`templates/prompts/context-specific/` for backlog, cip, coe, whats_next): note “when linking GitHub work, put IDs in frontmatter.”

### Relationship to CIP-0017

Project-specific GitHub policies (extra labels, enterprise quirks) can still live in `.vibesafe/whats_next_local.py`. Core VibeSafe only implements the common probe + frontmatter enrichment + optional glance.

### Alternatives Considered

1. **Nested `github:` object** — cleaner long-term, worse compat with existing `github_issue`. Rejected for v1.
2. **Body-only links** — insufficient for tooling. Rejected.
3. **Bidirectional sync** — high complexity, fights human authorship of VibeSafe status. Rejected.
4. **GitHub as sole tracker** — already rejected in CIP-0011 Alternative 3.

## Implementation Plan

1. **Phase 0 — Spec in validators (validation-led)**  
   - Document optional fields in structure validator / frontmatter examples  
   - Normalize/accept legacy `github_issue`  
   - Tests for normalization helpers (no live network)

2. **Phase 1 — Templates and prompts**  
   - Update CIP / backlog / CoE templates  
   - Update agent prompt sources for link-in-frontmatter guidance  

3. **Phase 2 — `whats-next` probe + Layer 1**  
   - Eligibility helpers  
   - Enrichment display for linked IDs  
   - `--no-github`  
   - Mocked `gh` unit/integration tests  

4. **Phase 3 — Soft next-steps + Layer 2 glance**  
   - Mismatch hints  
   - Optional open-PR (and labeled-issue) glance  

5. **Phase 4 — Dogfood**  
   - Link a few real VibeSafe CIP/backlog items to existing GitHub PRs/issues where useful  
   - Confirm graceful skip when auth fails  

## Backward Compatibility

- Fully additive and optional.
- Existing empty/`N/A` `github_issue` values remain harmless.
- No install migration required beyond normal template/system file updates.
- Projects without GitHub see no behaviour change.

## Testing Strategy

- Unit tests for field normalization and eligibility detection (fake PATH / fake remote / fake auth exit codes).
- Integration tests that mock `gh` stdout/stderr; no live GitHub required in CI.
- Manual dogfood: `./whats-next` with and without `gh auth`, and with `--no-github`.
- Install/template tests if template paths are covered by existing bats suite.

## Related Requirements

- [REQ-0011](../requirements/req0011_optional-github-collaboration-surface.md) — Optional GitHub collaboration surface
- [REQ-0005](../requirements/req0005_project-summary-tool.md) — Clear understanding of project status

Specifically:
- Optional enrichment when GitHub + `gh` available
- Graceful degradation otherwise
- Metadata-declared links; no forced Issues; no bidirectional sync

## Implementation Status

- [x] Design documented (this CIP, Proposed → Accepted)
- [x] Phase 0: Validator / normalization + tests — `backlog/features/2026-10-17_cip001A-phase0-normalization.md`
- [ ] Phase 1: Templates and agent prompts — `backlog/features/2026-10-17_cip001A-phase1-templates-prompts.md`
- [ ] Phase 2: `whats-next` Layer 1 + `--no-github` — `backlog/features/2026-10-17_cip001A-phase2-whats-next-layer1.md`
- [ ] Phase 3: Soft next-steps + Layer 2 glance — `backlog/features/2026-10-17_cip001A-phase3-next-steps-glance.md`
- [ ] Phase 4: Dogfood on VibeSafe itself — `backlog/features/2026-10-17_cip001A-phase4-dogfood.md`

## References

- REQ-0011, REQ-0005
- CIP-000A (`whats-next`), CIP-0017 (local hooks pattern)
- CIP-0011 Alternatives — rejection of external trackers as replacement
- Existing optional field docs: `docs/source/yaml_frontmatter_examples.md` (`github_issue`)
- GitHub CLI: https://cli.github.com/
