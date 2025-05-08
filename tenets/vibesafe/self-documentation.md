## Tenet: self-documentation

**Title**: Self-Documentation Through Implementation

**Description**: Systems should document themselves through their implementation rather than requiring separate documentation. When the system itself demonstrates how it works, it reduces duplication and the risk of documentation becoming outdated. This principle encourages designing systems where the structure, behavior, and configuration are intrinsically evident from the implementation.

**Quote**: *"The best documentation is the system itself."*

**Examples**:
- Directory structures that reflect their purpose without needing explanation
- Configuration options with clear, self-explanatory names
- Environment variables that document their purpose through naming
- Scripts that explain their behavior through clear function names and organization
- Tests that serve as examples of expected behavior

**Counter-examples**:
- Hard-coded structures that differ from what's documented
- Magic values that require separate explanation
- Configuration options that need extensive documentation to understand
- Implementation that duplicates information stored elsewhere

**Conflicts**:
- May conflict with simplicity when making behavior self-documenting requires more verbose code
- Resolution: Balance clarity with brevity; use good naming conventions and structure
- Has a close relationship with the "Documentation as First-Class Citizen" tenet - see CIP-0007 for discussion of how these tenets interact

**Version**: 1.0 (2025-05-05) 