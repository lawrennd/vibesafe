# AI-Requirements Framework - DEPRECATED

**Status**: This framework has been replaced by the simplified `requirements/` directory (CIP-0011 Phase 1).

**Deprecated**: 2026-01-03

**Replaced By**: `requirements/` directory with YAML frontmatter

## Why Was This Deprecated?

The AI-Requirements framework was initially designed to provide structured prompts, patterns, and integrations for requirements gathering. However, it introduced unnecessary complexity:

1. **Too prescriptive**: Required specific directory structures, prompts, and patterns
2. **Overly complex**: Many files and concepts for what should be simple requirements
3. **Confusion between WHAT and HOW**: Framework mixed requirements (WHAT) with process (HOW)
4. **Violated simplicity tenet**: Added cognitive overhead without proportional value

## What Replaced It?

The new `requirements/` directory provides:

- **Simple YAML frontmatter**: Consistent metadata without complex structure
- **Clear WHAT vs HOW distinction**: Requirements focus on outcomes, not implementation
- **Bottom-up linking**: Requirements link to tenets (WHY), CIPs link to requirements (HOW)
- **Optional patterns**: Moved to `docs/patterns/` as VibeSafe-level guidance, not required structure

## Migration Path

If you have an existing project using ai-requirements:

1. **Identify your actual requirements**: Files you created (not framework files)
2. **Convert to new format**: Use `templates/requirements/requirement_template.md`
3. **Update YAML frontmatter**: Remove `related_cips`, `related_backlog` (bottom-up pattern)
4. **Add `related_tenets`**: Link requirements to the principles that inform them
5. **Run validation**: `./scripts/validate_vibesafe_structure.py`

## What to Keep?

The patterns (goal-decomposition, stakeholder-identification, constraint-mapping) are still valuable as thinking tools. They've been moved to `docs/patterns/` as optional VibeSafe guidance.

## References

- **CIP-0011**: Simplify VibeSafe Component Management (Phase 1)
- **REQ-0002**: Simplify Requirements Framework
- **New requirements documentation**: `requirements/README.md`
- **WHAT vs HOW guide**: `.cursor/rules/requirements_rule.mdc`

## Questions?

Consult the VibeSafe documentation or create an issue if you need help migrating from ai-requirements to the new requirements/ format.

