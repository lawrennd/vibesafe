# VibeSafe Principles

**These are VibeSafe's framework-level guiding principles**, not project-specific tenets.

## Terminology Distinction

| Term | Scope | Purpose | Location | Deployment |
|------|-------|---------|----------|------------|
| **VibeSafe Principles** | Framework | Guidance for how VibeSafe projects work | `tenets/vibesafe/` | `vibesafe-principles.mdc` → all projects |
| **Project Tenets** | Project-specific | User's own project values | `tenets/projectname/` | `project_tenet_*.mdc` per tenet |

## VibeSafe Principles

These principles guide how VibeSafe itself works and provide guidance to all projects using VibeSafe:

1. **validation-led-development**: Build verification before implementation (for significant changes)
2. **simplicity-of-use**: Prioritize ease of adoption and daily use
3. **documentation-as-code**: Documentation and implementation as unified whole
4. **user-autonomy**: Respect users' freedom to make their own choices
5. **shared-information-landmarks**: Create explicit reference points for collaboration
6. **information-exploration-patterns**: Support different patterns of information exploration

## How They're Deployed

When users install VibeSafe:
1. `combine_tenets.py` generates `vibesafe-principles.md` (combined markdown)
2. `combine_tenets.py` generates `templates/.cursor/rules/vibesafe-principles.mdc` (combined cursor rule)
3. `install-minimal.sh` deploys to user projects → `.cursor/rules/vibesafe-principles.mdc`
4. AI assistants in user projects follow VibeSafe Principles automatically

This is different from project tenets (CIP-0010), which are user-created and deployed individually.

## Maintenance

These principles are reviewed annually (see `review_frequency` in each principle's YAML frontmatter).

When adding a new principle:
1. Create file in `tenets/vibesafe/`
2. Run `combine_tenets.py` to regenerate combined files
3. Commit both the new principle AND the generated files
4. Next `install-minimal.sh` will deploy to user projects

