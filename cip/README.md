# Code Improvement Proposals (CIPs)

## Overview

Code Improvement Proposals (CIPs) are documents that describe proposed changes to the referia codebase. They serve as a way to document design decisions, track progress on implementation, and provide context for code changes.

## Process

1. **Create a New CIP**:
   - Copy the `cip_template.md` file
   - Name it `cipXXXX.md` where XXXX is the next number in sequence
   - Fill in the details of your proposal

2. **Review**:
   - Share the CIP with other developers for feedback
   - Update the CIP based on feedback

3. **Implementation**:
   - Update the CIP with implementation details
   - Mark tasks as complete in the Implementation Status section as you make progress

4. **Completion**:
   - Once all tasks are complete, mark the CIP as completed
   - Add a summary of the changes made

## CIP Status

Each CIP can have one of the following statuses:

- **Draft**: Initial proposal, subject to change
- **Accepted**: Proposal has been accepted and is ready for implementation
- **In Progress**: Implementation is underway
- **Completed**: Implementation is complete
- **Rejected**: Proposal has been rejected

## Documentation Compression

After a CIP is closed (implementation complete and verified), its key decisions should be compressed into formal documentation (README, Sphinx, architecture docs). The `compressed` metadata field tracks this:

- **`compressed: false`** (default): CIP closed but not yet compressed into formal docs
- **`compressed: true`**: CIP's key decisions reflected in formal documentation

**Why compression matters**: CIPs document the development journey (WHY, HOW, alternatives considered). Formal documentation should capture the final outcome (WHAT was built, essential WHY). Users shouldn't need to read 50+ closed CIPs to understand current architecture.

**Compression workflow**:
1. Close CIP after implementation verified
2. Extract key decisions: WHAT was built, WHY, architecture patterns
3. Update formal documentation (README, Sphinx, `docs/architecture.md`)
4. Add traceability: reference CIP number in formal docs
5. Set `compressed: true` in CIP YAML frontmatter
6. Commit: "Compress CIP-XXXX into formal documentation"

The `whats-next` script detects uncompressed closed CIPs and prompts for compression. See [REQ-000E](../requirements/req000E_documentation-synchronization.md) and [CIP-0013](./cip0013.md) for details.

**Example**:
- **Before**: CIP-0012 (15 pages of implementation details, 4 phases, 50+ commits)
- **After**: README section "Multi-platform AI assistant support" + architecture doc entry (2 paragraphs) + reference to CIP-0012 for detailed rationale

## Current CIPs

- [CIP-0001](./cip0001.md): VibeSafe Project Management Templates
- [CIP-0002](./cip0002.md): VibeSafe Local Installation Method
- [CIP-0003](./cip0003.md): Gist Integration for VibeSafe
- [CIP-0004](./cip0004.md): Tenet System for Project Governance
- [CIP-0005](./cip0005.md): Enhanced Documentation-First Practices
- [CIP-0006](./cip0006.md): Installation Script Redesign
- [CIP-0007](./cip0007.md): New Tenet - Documentation and Implementation as a Unified Whole
- [CIP-0008](./cip0008.md): Unified Philosophy Document and New Tenets for Human-LLM Collaboration
- [CIP-0009](./cip0009.md): Requirements Conversation Framework
- [CIP-000A](./cip000A.md): Project Status Summarizer ("What's Next" Script)
- [CIP-000B](./cip000B.md): VibeSafe Update Script
- [CIP-000C](./cip000C.md): Integrate AI-Requirements Framework into Installation Script
- [CIP-000D](./cip000D.md): Backlog Module Refactor
- [CIP-000E](./cip000E.md): Clean Installation Philosophy for VibeSafe
- [CIP-000F](./cip000F.md): VibeSafe Auto-Gitignore Protection
- [CIP-0010](./cip0010.md): Automatic Tenets-to-Cursor-Rules Generation
- [CIP-0011](./cip0011.md): Simplify VibeSafe Component Management
- [CIP-0012](./cip0012.md): AI Assistant Framework Independence Implementation
- [CIP-0013](./cip0013.md): Documentation Compression Stage
- [CIP-0014](./cip0014.md): Traceability Analysis and Reporting in whats-next

## Creating a Good CIP

A good CIP should:

1. Clearly state the problem being solved
2. Explain the proposed solution in detail
3. Consider alternative approaches
4. Address backward compatibility
5. Include a testing strategy
6. Provide a clear implementation plan
7. Consider potential drawbacks or risks 
