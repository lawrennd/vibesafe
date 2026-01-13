---
id: "human-authorship"
title: "Human Authorship and Accountability"
status: "Active"
created: "2026-01-10"
last_reviewed: "2026-01-10"
review_frequency: "Annual"
conflicts_with: ["simplicity-of-use"]
tags:
  - ai-human-interaction
  - governance
  - accountability
---

## Tenet: human-authorship

**Title**: Human Authorship and Accountability

**Description**: In VibeSafe, humans are the authors of decisions and bear ultimate accountability for outcomes. AI assistants can propose, draft, and automate, but their outputs are never authoritative by default. VibeSafe’s workflows exist to create explicit moments where a human reviews, decides, and takes responsibility for what enters the system. When responsibility is declared in metadata, it must be **single-threaded**: one primary accountable human per artifact.

**Quote**: *"AIs advise; humans decide."*

**Examples**:
- An AI assistant drafts a CIP, but a human reviews it and marks it **Accepted** before implementation begins
- Natural breakpoints where the assistant pauses for explicit human go/no-go at high-leverage decision points
- CIPs and commit messages record the human intent and rationale even when code/text was AI-generated
- Backlog tasks always name a human owner responsible for driving the task to completion or explicitly closing it
- Validation errors are treated as prompts for human judgment, not “paperwork” to be bypassed

**Counter-examples**:
- Merging AI-generated changes without a human understanding the intent, risks, and blast radius
- Treating “the AI said so” as sufficient rationale for a design decision
- Allowing “team”, “AI”, or empty placeholders to stand in for responsibility-bearing ownership
- Skipping checkpoints to move faster, thereby accumulating unowned risk

**Conflicts**:
- Can conflict with **simplicity-of-use** by adding friction
- Resolution: Keep human decision points minimal, predictable, and high-leverage; automate everything else

**Version**: 1.0 (2026-01-10)


