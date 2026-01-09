# Contributing to VibeSafe

This guide is for contributors working on **VibeSafe itself**, not for users adopting VibeSafe in their projects.

## Development Setup

### Installing the Pre-Commit Hook

VibeSafe uses a pre-commit hook to prevent system file drift:

```bash
# Install the pre-commit hook (recommended for contributors)
cp templates/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This hook:
- ✅ Validates that `scripts/` and `templates/scripts/` are in sync
- ✅ Checks YAML frontmatter and cross-references
- ✅ Prevents commits that would break the installation

### Understanding System File Sync

Per [CIP-000E](../../cip/cip000E.md) (Clean Installation Philosophy), `templates/` is the **source of truth**:

```
templates/scripts/whats_next.py  → (SOURCE OF TRUTH - propagates on install)
scripts/whats_next.py            → (runtime copy for development)
```

**When modifying system scripts:**

1. Edit the file in `scripts/` (for development/testing)
2. When satisfied, sync to `templates/`:
   ```bash
   cp scripts/whats_next.py templates/scripts/whats_next.py
   ```
3. Commit both files together

**The validation script checks this automatically:**

```bash
python scripts/validate_vibesafe_structure.py
```

## Validation (REQ-0006)

VibeSafe validates its own conformance to requirements:

```bash
# Run full validation
python scripts/validate_vibesafe_structure.py

# Check specific component types
python scripts/validate_vibesafe_structure.py --component req
python scripts/validate_vibesafe_structure.py --component cip

# Auto-fix simple issues
python scripts/validate_vibesafe_structure.py --fix --dry-run
```

See [REQ-0006](../../requirements/req0006_process-conformance-validation.md) for the validation approach.

## Testing

```bash
# Run all tests
bats scripts/test/*.bats
python -m pytest tests/ -v

# Run specific test suites
bats scripts/test/install-test.bats
python -m pytest tests/test_whats_next.py -v
```

## VibeSafe Development Workflow

1. **Check current state**: `./whats-next`
2. **Review requirements**: Check `requirements/` for WHAT needs to be true
3. **Create CIP**: Define HOW to implement the requirement
4. **Create backlog tasks**: Break down the CIP into DO items
5. **Implement**: Follow the backlog tasks
6. **Validate**: Run validation script
7. **Compress**: Update formal docs when complete (see [Compression Guide](compression-guide.md))

## Following Our Own Process

VibeSafe dogfoods its own practices:

- Requirements in `requirements/` define WHAT
- CIPs in `cip/` define HOW
- Backlog in `backlog/` defines DO
- Tenets in `tenets/vibesafe/` define WHY

We use our own tools (`whats-next`, validation, compression) to develop VibeSafe itself.

