# VibeSafe Architecture

This document describes VibeSafe's technical architecture and infrastructure decisions.

## Installation System

### Clean Installation Philosophy

**Implemented in:** [CIP-000E](../../cip/cip000E.md) - Clean Installation Philosophy

Every VibeSafe installation is conceptually a reinstallation. The system distinguishes between:
- **System files**: Templates, scripts, cursor rules (always updated)
- **User content**: Project-specific CIPs, backlog, requirements, tenets (always preserved)

**Key principles:**
1. Installation is idempotent (safe to run multiple times)
2. System files propagate from `templates/` directory
3. User content is never modified without explicit action
4. Clear separation prevents accidental overwrites

This philosophy enables painless updates and consistent behavior across fresh installs and updates.

### Auto-Gitignore Protection

**Implemented in:** [CIP-000F](../../cip/cip000F.md) - Auto-Gitignore Protection

VibeSafe automatically manages `.gitignore` entries to prevent users from accidentally committing system files. During installation, the script:
1. Detects existing `.gitignore`
2. Adds/updates VibeSafe section atomically
3. Protects templates, generated files, and installation artifacts
4. Preserves user's existing ignore rules

**Benefits:**
- Users don't need to understand which files are system vs user
- Reduces documentation burden
- Prevents common mistakes
- Aligns with "Simplicity at All Levels" tenet

### Update Script

**Implemented in:** [CIP-000B](../../cip/cip000B.md) - VibeSafe Update Script

VibeSafe provides a self-contained update mechanism that:
- Fetches latest version from GitHub
- Updates system files in `templates/`
- Preserves all user content
- Reports what was updated

**Command:**
```bash
bash <(curl -s https://raw.githubusercontent.com/lawrennd/vibesafe/main/scripts/install-minimal.sh)
```

The same script handles both fresh installs and updates, demonstrating the Clean Installation Philosophy in practice.

---

## Project Status Tools

### What's Next Script

**Implemented in:** [CIP-000A](../../cip/cip000A.md) - Project Status Summarizer

The `whats-next` script provides real-time project status for both humans and AI assistants:

**Features:**
- Scans CIPs, backlog, requirements, tenets
- Reports current status by category
- Suggests next actionable steps
- Compression candidate detection
- Documentation spec integration
- Traceability analysis (CIP-0014)

**Architecture:**
- Pure Python (minimal dependencies: PyYAML)
- Separate virtual environment (`.venv-vibesafe`)  
- Command-line flags for filtering (`--cip-only`, `--quiet`, etc.)
- Extensible prompt generation system

**Key insight**: A single command should provide complete project context without requiring users to manually scan multiple directories.

---

## Tenet System

**Implemented in:** [CIP-0004](../../cip/cip0004.md) - Tenet System for Project Governance

VibeSafe's tenet system provides foundational principles that guide decision-making:

**Architecture:**
```
tenets/
├── vibesafe/          # VibeSafe's own tenets
│   ├── user-autonomy.md
│   ├── simplicity-at-all-levels.md
│   └── ...
└── [project]/         # User's project tenets
    └── ...
```

**Automatic Integration:**
- Tenets are automatically converted to AI assistant prompts
- Generated during installation for all platforms (Cursor, Copilot, Claude, Codex)
- No manual copying required

**Design principles:**
1. Limited number (7±2 tenets optimal)
2. Memorable and actionable
3. Document conflicts and resolutions
4. Include examples and counter-examples

**Key insight**: Tenets codify the "WHY" that informs all other decisions (WHAT, HOW, DO).

---

## Multi-Platform AI Assistant Support

**Implemented in:** [CIP-0012](../../cip/cip0012.md) - AI Assistant Framework Independence

VibeSafe works across multiple AI coding assistants without platform lock-in:

**Supported Platforms:**
- Cursor (`.cursor/rules/*.mdc`)
- GitHub Copilot (`.github/copilot-instructions.md`)  
- Claude Code (`CLAUDE.md`)
- Codex (`AGENTS.md`)

**Architecture:**
```
templates/prompts/
├── always-apply/      # Core VibeSafe guidance (installed for all platforms)
├── context-specific/  # Loaded based on file context (CIPs, backlog, etc.)
└── ...
```

**Prompt Generation:**
1. Store platform-agnostic markdown in `templates/prompts/`
2. Generate platform-specific files at install time
3. Single source of truth prevents drift
4. Users can customize via `VIBESAFE_PLATFORM` environment variable

**Key insight**: Framework independence respects user autonomy and ensures VibeSafe remains useful regardless of tooling choices.

---

*Last updated: 2026-01-09*
*This file is part of the VibeSafe formal documentation system.*

