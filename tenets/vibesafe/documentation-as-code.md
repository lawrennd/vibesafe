## Tenet: documentation-as-code

**Title**: Documentation and Implementation as a Unified Whole

**Description**: Documentation and implementation should be treated as a unified, interdependent system rather than separate concerns. Documentation guides implementation by establishing clear goals and expectations, while implementation embodies and validates that documentation through self-documenting design. This bidirectional relationship ensures that our systems remain understandable, accurate, and maintainable.

**Quote**: *"Document to guide implementation; implement to validate documentation."*

**Examples**:
- Writing CIPs that define expected behaviors, then implementing systems that inherently demonstrate those behaviors
- API documentation that defines interfaces, paired with code that uses clear naming and structure matching the documentation
- Directory structures that follow the same organization described in documentation
- Configuration options with names that directly reflect their documented purpose
- Environment variables that document their purpose through their naming
- Tests that serve as working examples of documented behaviors

**Counter-examples**:
- Documentation that describes one behavior while code implements another
- Hard-coded magic values that require separate explanation
- Systems that can only be understood by reading extensive external documentation
- Adding features without updating both implementation and documentation
- Implementation that requires documentation to be understandable

**Practices**:
- Begin with documentation to establish design intent
- Structure implementation to mirror and embody that documentation
- When changing code, update documentation simultaneously
- When changing documentation, ensure implementation reflects the changes
- Use self-explanatory names, structures, and organization in code
- Test against documented behaviors rather than implementation details

**Conflicts**:
- May appear to slow initial development by requiring both clear documentation and self-documenting code
- Resolution: The investment pays off through reduced maintenance burden and fewer misunderstandings

**Version**: 1.0 (2025-05-05) 