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

- [CIP-0001](./cip0001.md): 

## Creating a Good CIP

A good CIP should:

1. Clearly state the problem being solved
2. Explain the proposed solution in detail
3. Consider alternative approaches
4. Address backward compatibility
5. Include a testing strategy
6. Provide a clear implementation plan
7. Consider potential drawbacks or risks 
