---
id: "2025-12-23_whats-next-tenet-review-suggestions"
title: "Add tenet review suggestions to What's Next script"
status: "Completed"
priority: "Medium"
created: "2025-12-23"
last_updated: "2025-12-23"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ""
tags:
- feature
- whats-next
- tenets
- maintenance
- project-health
---

# Task: Add tenet review suggestions to What's Next script

## Description

Enhance the `whats-next` script to help projects maintain healthy tenets by:
1. Checking if project tenets exist
2. Suggesting creation of tenets if they don't exist
3. Tracking when tenets were last modified
4. Suggesting periodic tenet reviews based on age

Tenets are living documents that should be reviewed and updated as projects evolve. The What's Next script should help remind teams to keep their tenets relevant.

## Motivation

**Problem:**
- Projects may not create tenets initially
- Tenets can become stale or outdated over time
- No prompts to review/update tenets as projects evolve
- Teams forget about tenets after initial creation

**Solution:**
- What's Next script checks tenet health
- Suggests creation if tenets don't exist
- Recommends review after configurable period (e.g., 6 months)
- Helps keep project principles aligned with current practice

## Acceptance Criteria

- [x] Detect if `tenets/` directory exists
- [x] Detect if any project-specific tenets exist (not just VibeSafe system files)
- [x] Check creation/modification dates of tenet files
- [x] Suggest tenet creation if none exist
- [x] Suggest tenet review if tenets haven't been modified in X months (configurable)
- [x] Add tenet status section to What's Next output
- [x] Make review period configurable (default: 6 months)
- [x] Handle edge cases (no git history, new projects, etc.)
- [ ] Update What's Next documentation (deferred)

## Implementation Notes

### Tenet Detection Logic

```python
def check_tenet_status():
    """Check status of project tenets."""
    tenets_dir = Path("tenets")
    
    # Check if tenets directory exists
    if not tenets_dir.exists():
        return {
            "status": "missing",
            "message": "No tenets directory found"
        }
    
    # Find project-specific tenet files (not VibeSafe system files)
    project_tenets = []
    system_files = ["README.md", "tenet_template.md", "combine_tenets.py"]
    
    for file in tenets_dir.rglob("*.md"):
        if file.name not in system_files:
            project_tenets.append(file)
    
    if not project_tenets:
        return {
            "status": "empty",
            "message": "Tenets directory exists but no project tenets found"
        }
    
    # Check age of tenets
    oldest_modification = None
    newest_modification = None
    
    for tenet in project_tenets:
        mtime = tenet.stat().st_mtime
        if oldest_modification is None or mtime < oldest_modification:
            oldest_modification = mtime
        if newest_modification is None or mtime > newest_modification:
            newest_modification = mtime
    
    return {
        "status": "exists",
        "count": len(project_tenets),
        "oldest_modification": oldest_modification,
        "newest_modification": newest_modification,
        "files": [str(f.relative_to(tenets_dir)) for f in project_tenets]
    }
```

### Review Period Configuration

**Option 1: Command-line flag**
```bash
./whats-next --tenet-review-period 180  # 180 days = ~6 months
```

**Option 2: Configuration file**
```yaml
# .vibesafe/config.yaml
tenet_review_period_days: 180
```

**Option 3: Environment variable**
```bash
VIBESAFE_TENET_REVIEW_DAYS=180 ./whats-next
```

**Recommendation:** Use command-line flag with default of 180 days (6 months)

### Output Format

**When tenets don't exist:**
```
📋 Project Tenets
==================
❌ No project tenets found

Tenets help define guiding principles for your project.

Next steps:
  1. Review VibeSafe tenets for inspiration: tenets/vibesafe/
  2. Create your first project tenet: cp tenets/tenet_template.md tenets/my-first-tenet.md
  3. Edit and define your project's guiding principles
  
For more information: https://github.com/lawrennd/vibesafe
```

**When tenets exist and are recent:**
```
📋 Project Tenets
==================
✅ 5 project tenets found
📅 Last modified: 2025-11-15 (38 days ago)

Your tenets are up to date.
```

**When tenets need review:**
```
📋 Project Tenets
==================
⚠️  5 project tenets found
📅 Last modified: 2025-01-20 (337 days ago)

Your tenets haven't been reviewed in 11 months.

Consider reviewing your tenets to ensure they still reflect your project's
current practices and goals. Projects evolve, and tenets should too.

Next steps:
  1. Review existing tenets: ls tenets/
  2. Update tenets that need refinement
  3. Add new tenets for emerging patterns
  4. Remove or archive tenets that are no longer relevant
```

### Age Thresholds

Suggested thresholds:
- **< 3 months**: Fresh, no action needed
- **3-6 months**: Recent, no urgent action
- **6-12 months**: ⚠️ Consider review
- **> 12 months**: ⚠️ Review recommended

### Edge Cases

1. **No git history**: Use file modification times
2. **New project**: Don't nag immediately, suggest after some development
3. **VibeSafe itself**: May have frequent tenet updates, adjust thresholds
4. **Multiple tenet directories**: Check all subdirectories of `tenets/`
5. **Read-only filesystem**: Handle gracefully if can't read file stats

## Related

- What's Next script: `scripts/whats_next.py`
- Tenet system: `tenets/`
- Tenet template: `tenets/tenet_template.md`
- VibeSafe tenets: `tenets/vibesafe/`

## Questions to Resolve

1. What's the optimal review period? (Suggested: 6 months)
2. Should review suggestions be part of default output or opt-in?
3. Should we track review dates separately from modification dates?
4. Should we have different thresholds for different project types?
5. Should we integrate with git to check commit dates vs file modification?
6. Should we suggest specific tenets to review (oldest first)?

## Progress Updates

### 2025-12-23

Task created to enhance What's Next script with tenet health checking and review suggestions. This will help teams maintain living tenets that evolve with their projects.

### 2025-12-23 (Later)

**Implementation completed:**

Added `check_tenet_status()` function to `scripts/whats_next.py`:
- Detects if tenets directory exists
- Distinguishes project tenets from VibeSafe system files (excludes vibesafe/ subdirectory)
- Calculates days since last modification
- Recommends review after configurable period (default: 180 days = 6 months)
- Handles missing directory, empty directory, and existing tenets

Added command-line argument:
- `--tenet-review-period DAYS` (default: 180)

Display output with color-coded status:
- Missing: Red - suggests creation with step-by-step instructions
- Empty: Yellow - directory exists but no project tenets
- Fresh (< 3 months): Green - no action needed
- Recent (3-6 months): Yellow - no urgent action
- Needs review (> review period): Red - detailed review recommendations

Integrated with next steps generation:
- Suggests tenet creation if missing
- Suggests first tenet if directory empty
- Suggests review if tenets exceed review period

Tested on VibeSafe repository - correctly identifies no project tenets and suggests creation.

Status changed to Completed. Documentation update deferred as script has --help for usage.

