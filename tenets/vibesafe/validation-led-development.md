---
id: "validation-led-development"
title: "Build Verification Before Implementation"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
  - testing
  - quality
  - development-practice
  - dogfooding
---

## Tenet: validation-led-development

**Title**: Build Verification Before Implementation

**Description**: For significant changes, build validation and testing infrastructure before implementing the feature itself. This ensures we can verify conformance to specifications as we build, catch errors early, and provide confidence that the implementation matches the design. This doesn't mean exhaustive testing for trivial changes, but for substantial work (like CIP-0011), build the "gold standard" checker first.

**Quote**: *"Validate the spec, then build to the spec."*

**Examples**:
- Creating `validate_vibesafe_structure.py` (Phase 0a) before implementing YAML changes (Phase 0)
- Writing test cases based on CIP acceptance criteria before implementation begins
- Building schema validators before migrating data formats
- Creating property-based tests that encode specifications
- The validation script itself serves as executable specification
- Test suite that validates backlog/CIP YAML frontmatter structure

**Counter-examples**:
- Building entire feature first, then trying to retrofit tests
- No way to verify conformance except manual inspection
- "Testing is optional" mindset
- Over-testing trivial changes (adding a comment doesn't need validation infrastructure)
- Validation so complex it's harder to maintain than the feature
- Creating validators that test implementation details instead of specifications

**Practices**:
- For CIPs: Create validation script if changing system structure
- For features: Write tests encoding acceptance criteria first
- For migrations: Build validators for old and new formats
- Skip for: Documentation fixes, simple bug fixes, trivial changes
- Validators should be simple, fast, and focused on specifications

**Conflicts**:
- Can conflict with "Simplicity at All Levels" when validation infrastructure becomes complex
- Resolution: Apply validation-led approach to significant changes only. Trivial changes don't need validation infrastructure. Keep validators simple and focused on specs, not implementation details.

**Synergies**:
- **Documentation-as-Code**: Validation scripts are executable documentation of specifications
- **Information Landmarks**: Validators serve as fixed reference points defining "correct" structure
- **Dogfooding**: Phase 0a demonstrates this tenet - we validate VibeSafe follows its own specs

**Version**: 1.0 (2026-01-03)

