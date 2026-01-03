# VibeSafe Tenets

**These are VibeSafe's own tenets** - the guiding principles for how VibeSafe itself works.

## Naming: "Tenets" Here, "Principles" When Deployed

In this repo, these are **tenets** (like any project's tenets). When deployed to user projects, they're packaged as **"VibeSafe Principles"** to avoid confusion with the user's own "Project Tenets".

| Perspective | Name | Location | Why |
|-------------|------|----------|-----|
| **In VibeSafe repo** | VibeSafe Tenets | `tenets/vibesafe/` | VibeSafe's own guiding principles |
| **In user projects** | VibeSafe Principles | `.cursor/rules/vibesafe-principles.mdc` | Avoid namespace collision with user's tenets |

It's a packaging choice, not a fundamental difference.

## VibeSafe's Tenets

These principles guide how VibeSafe itself works and provide guidance to all projects using VibeSafe:

1. **validation-led-development**: Build verification before implementation (for significant changes)
2. **simplicity-of-use**: Prioritize ease of adoption and daily use
3. **documentation-as-code**: Documentation and implementation as unified whole
4. **user-autonomy**: Respect users' freedom to make their own choices
5. **shared-information-landmarks**: Create explicit reference points for collaboration
6. **information-exploration-patterns**: Support different patterns of information exploration

## How They're Deployed to User Projects

When users install VibeSafe:
1. `scripts/generate_vibesafe_principles.py` reads VibeSafe's tenets from `tenets/vibesafe/`
2. Generates `templates/.cursor/rules/vibesafe-principles.mdc` (combined cursor rule, renamed to avoid confusion)
3. `install-minimal.sh` deploys to user projects → `.cursor/rules/vibesafe-principles.mdc`
4. AI assistants in user projects follow VibeSafe's guidance automatically

Meanwhile, the user's own project tenets:
- Live in `tenets/projectname/`
- Combined via `combine_tenets.py` (same tool VibeSafe uses)
- Deployed as individual `project_tenet_*.mdc` files (per CIP-0010)

## Maintenance

These tenets are reviewed annually (see `review_frequency` in each tenet's YAML frontmatter).

When adding a new tenet:
1. Create file in `tenets/vibesafe/`
2. Run `scripts/generate_vibesafe_principles.py` to regenerate `vibesafe-principles.mdc`
3. Commit both the new tenet AND the generated cursor rule
4. Next `install-minimal.sh` will deploy to user projects

