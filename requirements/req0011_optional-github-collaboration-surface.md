---
id: "0011"
title: "Optional GitHub Collaboration Surface in Project Status"
status: "In Progress"
priority: "Medium"
created: "2026-10-17"
last_updated: "2026-10-17"
related_tenets:
  - effortless-context-restoration
  - simplicity-of-use
  - user-autonomy
stakeholders:
  - developers
  - project-maintainers
  - ai-assistants
tags:
  - github
  - visibility
  - status
  - collaboration
---

# REQ-0011: Optional GitHub Collaboration Surface in Project Status

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

When a VibeSafe project uses GitHub and authenticated access to the GitHub CLI (`gh`) is available, humans and AI assistants should be able to see relevant Issues, Pull Requests, and Discussions alongside local VibeSafe status — without leaving the usual project-status workflow.

GitHub must remain optional. Projects that do not use GitHub, lack `gh`, or cannot authenticate must continue to get a complete, useful local status view with no errors or pressure to adopt GitHub. VibeSafe artifacts remain the source of truth for planning status (requirements, CIPs, backlog, CoEs); GitHub is a collaboration surface that can be linked and surfaced, not a replacement for those artifacts.

VibeSafe documents that correspond to GitHub work should be able to declare those links in machine-readable metadata so status tooling and assistants can resolve titles and states without scraping prose.

**Why this matters**: Effortless context restoration needs one place to see “what is going on.” Simplicity requires graceful degradation. User autonomy forbids forcing Issues for every backlog item.

**Who benefits**: Maintainers who already use GitHub for review and discussion; contributors and AI assistants who need linked external state when restoring context.

## Acceptance Criteria

- [ ] When GitHub + authenticated `gh` are available, project status can include linked Issues, PRs, and Discussions for VibeSafe artifacts that declare those links
- [ ] When GitHub/`gh`/auth is unavailable, project status works unchanged with no hard failure
- [ ] Users are not required to create GitHub Issues, PRs, or Discussions for VibeSafe to function
- [ ] Linked GitHub identifiers live in artifact metadata (not only free-text body sections)
- [ ] Closing or merging a GitHub item does not automatically change VibeSafe artifact status (no silent bidirectional sync)
- [ ] Status output remains readable by both humans and AI assistants
- [ ] Projects without a GitHub remote are not prompted to adopt GitHub

## Notes (Optional)

**Out of scope for this requirement**:
- Replacing backlog/CIPs with GitHub Issues as the planning system
- Mandatory mirroring of every task to an Issue
- Bidirectional status sync or write-back from `whats-next` into GitHub

**Relationship to REQ-0005**: This extends “clear understanding of project status” with an optional external collaboration layer when the project already uses GitHub.

## References

- **Related Tenets**: effortless-context-restoration, simplicity-of-use, user-autonomy
- **Related**: REQ-0005 (Clear Understanding of Project Status); CIP-0011 Alternative 3 (rejected replacing VibeSafe with external trackers)

## Progress Updates

### 2026-10-17
Requirement created at Ready status from design discussion of optional GitHub Issues/PRs/Discussions integration.

CIP-001A accepted; backlog tasks created for Phases 0–4. Status → In Progress.
