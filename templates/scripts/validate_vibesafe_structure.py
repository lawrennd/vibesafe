#!/usr/bin/env python3
"""
VibeSafe Structure Validator

Validates that VibeSafe components conform to requirements specifications:
- REQ-0001: Standardized component metadata (YAML frontmatter)
- REQ-0006: Automated process conformance validation

Checks:
- File naming conventions (reqXXXX, cipXXXX, YYYY-MM-DD, kebab-case)
- YAML frontmatter structure (required fields, valid values)
- Cross-references between components (valid IDs)
- Bottom-up linking pattern (requirements→tenets, CIPs→requirements, backlog→CIPs)

Implementation: CIP-0011 Phase 0a
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False
    print("Error: python-frontmatter not available. Install with: pip install python-frontmatter")
    sys.exit(1)


# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def disable():
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.BLUE = ''
        Colors.BOLD = ''
        Colors.END = ''


def colored(text, color):
    """Apply color to text."""
    return f"{color}{text}{Colors.END}"


# REQ-0010: Human-authored responsibility (AIs advise; humans decide)
_ATTRIBUTION_BRACKET_PLACEHOLDER_RE = re.compile(r'^\[.*\]$')
_ATTRIBUTION_DISALLOWED_EXACT = {
    "",
    "unknown",
    "n/a",
    "na",
    "none",
    "tbd",
    "todo",
    "and date",
    "vibesafe team",
    "team",
    "ai",
    "assistant",
    "openai",
    "chatgpt",
    "claude",
    "copilot",
    "codex",
}
_ATTRIBUTION_DISALLOWED_SUBSTRINGS = [
    "your name",
    "author name",
    "person name",
]


def validate_human_attribution(component_type, file_path, field_name, value, result):
    """
    Validate that an attribution field (e.g. author/owner) names a specific human.

    Enforces REQ-0010: values must be non-empty and must not be placeholders or
    non-human/tool attributions.
    """
    if not isinstance(value, str):
        result.add_error(f"Invalid '{field_name}': expected string, got {type(value).__name__}", file_path)
        return

    raw = value
    v = value.strip()
    v_lower = v.lower()

    if v_lower in _ATTRIBUTION_DISALLOWED_EXACT:
        result.add_error(f"Invalid '{field_name}': must be a human name (got '{raw}')", file_path)
        return

    if _ATTRIBUTION_BRACKET_PLACEHOLDER_RE.match(v):
        result.add_error(f"Invalid '{field_name}': placeholder value '{raw}'", file_path)
        return

    for s in _ATTRIBUTION_DISALLOWED_SUBSTRINGS:
        if s in v_lower:
            result.add_error(f"Invalid '{field_name}': placeholder value '{raw}'", file_path)
            return

    # Single-threaded ownership: one primary accountable human per artifact
    if "," in v or ";" in v or " & " in v_lower or " and " in v_lower or "/" in v:
        result.add_error(
            f"Invalid '{field_name}': must name a single primary accountable human (got '{raw}')",
            file_path,
        )
        return


def _get_git_changed_paths(root_dir: str) -> Optional[List[str]]:
    """Return a list of changed file paths from `git status --porcelain`, or None if not a git repo."""
    try:
        import subprocess

        # Are we in a git repo?
        p = subprocess.run(
            ['git', '-C', root_dir, 'rev-parse', '--is-inside-work-tree'],
            capture_output=True,
            text=True,
            check=False,
        )
        if p.returncode != 0 or p.stdout.strip() != "true":
            return None

        status = subprocess.run(
            ['git', '-C', root_dir, 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=False,
        )
        if status.returncode != 0:
            return None

        changed: List[str] = []
        for line in status.stdout.splitlines():
            if not line.strip():
                continue
            # Format: XY <path> (or rename: XY old -> new)
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1].strip()
            changed.append(path)
        return changed
    except Exception:
        return None


def check_governance_drift(root_dir: str, result):
    """
    Warn when implementation/tooling changes occur without updating planning artifacts.

    This catches "own goal" process failures like: updating validators/scripts/templates
    without recording intent in CIP/backlog and/or without updating requirements where appropriate.
    """
    changed = _get_git_changed_paths(root_dir)
    if changed is None or len(changed) == 0:
        return

    def any_prefix(prefixes) -> bool:
        return any(p.startswith(prefixes) for p in changed)

    implementation_prefixes = (
        "scripts/",
        "templates/scripts/",
        "tests/",
        "install-minimal.sh",
        "install-whats-next.sh",
        "whats-next",
        "combine_tenets.py",
        "tenets/combine_tenets.py",
        "templates/.cursor/rules/",
    )
    planning_prefixes = ("cip/", "backlog/")
    requirements_prefixes = ("requirements/",)
    tenets_prefixes = ("tenets/",)

    has_impl = any_prefix(implementation_prefixes)
    has_planning = any_prefix(planning_prefixes)
    has_requirements = any_prefix(requirements_prefixes)
    has_tenets = any_prefix(tenets_prefixes)

    if has_impl and not has_planning:
        result.add_warning(
            "Governance drift: implementation/tooling changed but no CIP/backlog changed. "
            "Consider creating/updating a CIP (HOW) and/or backlog task (DO) to record intent and accountability.",
            os.path.join(root_dir, ".git"),
        )

    if has_impl and has_requirements and not has_planning:
        result.add_warning(
            "Traceability gap: requirements (WHAT) changed alongside implementation, but no CIP/backlog changed. "
            "This often means we skipped documenting HOW (CIP) or DO (task).",
            os.path.join(root_dir, ".git"),
        )

    if has_impl and has_tenets and not (has_requirements or has_planning):
        result.add_warning(
            "Tenet→implementation gap: tenets (WHY) and implementation changed, but no requirements/CIPs/backlog were updated. "
            "Consider adding a requirement to encode WHAT the tenet implies, and a CIP/task if behavior changed.",
            os.path.join(root_dir, ".git"),
        )


# Component specifications (from REQ-0001: Standardized Component Metadata)
COMPONENT_SPECS = {
    'requirement': {
        'dir': 'requirements',
        'pattern': r'^req([0-9A-Fa-f]{4})_[\w-]+\.md$',
        'id_format': 'XXXX (4-digit hex)',
        'required_fields': ['id', 'title', 'status', 'priority', 'created', 'last_updated', 'related_tenets', 'stakeholders'],
        'optional_fields': ['tags'],
        'allowed_status': ['Proposed', 'Ready', 'In Progress', 'Implemented', 'Validated', 'Deferred', 'Rejected'],
        'allowed_priority': ['High', 'Medium', 'Low'],
        'links_to': ['related_tenets'],  # Bottom-up: requirements → tenets
        # Requirements are WHAT and should not link down into HOW/DO.
        'should_not_have': ['related_requirements', 'related_cips', 'related_backlog'],  # Violates bottom-up
    },
    'cip': {
        'dir': 'cip',
        'pattern': r'^cip([0-9A-Fa-f]{4})(_[\w-]+)?\.md$',
        'id_format': 'XXXX (4-digit hex)',
        'required_fields': ['id', 'title', 'status', 'created', 'last_updated', 'author'],
        'optional_fields': ['related_requirements', 'related_cips', 'blocked_by', 'superseded_by', 'tags'],
        'allowed_status': ['Proposed', 'Accepted', 'In Progress', 'Implemented', 'Closed', 'Rejected', 'Deferred'],
        'links_to': ['related_requirements'],  # Bottom-up: CIPs → requirements
        'should_not_have': ['related_backlog'],  # Violates bottom-up
    },
    'backlog': {
        'dir': 'backlog',
        'pattern': r'^(\d{4})-(\d{2})-(\d{2})_[\w-]+\.md$',
        'id_format': 'YYYY-MM-DD_short-name',
        'required_fields': ['id', 'title', 'status', 'priority', 'created', 'last_updated', 'category', 'related_cips', 'owner'],
        # Exception path (Option B): allow backlog → requirement only when explicitly justified.
        'optional_fields': ['dependencies', 'tags', 'related_requirements', 'no_cip_reason'],
        'allowed_status': ['Proposed', 'Ready', 'In Progress', 'Completed', 'Abandoned'],
        'allowed_priority': ['High', 'Medium', 'Low'],
        'links_to': ['related_cips'],  # Bottom-up: backlog → CIPs
        'should_not_have': [],  # 'related_requirements' is allowed only via explicit exception (validated below)
    },
    'tenet': {
        'dir': 'tenets',
        'pattern': r'^[\w-]+\.md$',
        'id_format': 'kebab-case',
        'required_fields': ['id', 'title', 'status', 'created', 'last_reviewed', 'review_frequency'],
        'optional_fields': ['conflicts_with', 'tags'],
        'allowed_status': ['Active', 'Under Review', 'Archived'],
        'links_to': [],  # Foundation layer - no upward links
        'should_not_have': ['related_requirements', 'related_cips', 'related_backlog', 'related_tenets'],  # Foundation
    },
}


class ValidationResult:
    """Track validation results."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.fixes = []  # Track what was fixed
    
    def add_error(self, message, file_path=None):
        self.errors.append((message, file_path))
    
    def add_warning(self, message, file_path=None):
        self.warnings.append((message, file_path))
    
    def add_info(self, message):
        self.info.append(message)
    
    def add_fix(self, message, file_path=None):
        self.fixes.append((message, file_path))
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def has_warnings(self):
        return len(self.warnings) > 0
    
    def has_fixes(self):
        return len(self.fixes) > 0


def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file using python-frontmatter."""
    try:
        post = frontmatter.load(file_path)
        # Return metadata if it exists, None if no frontmatter
        return post.metadata if post.metadata else None
    except Exception as e:
        return None


def write_frontmatter(file_path, metadata, dry_run=False):
    """Write updated YAML frontmatter back to file using python-frontmatter."""
    if dry_run:
        return True
    
    try:
        # Load existing post
        post = frontmatter.load(file_path)
        
        # Update metadata
        post.metadata = metadata
        
        # Write back
        with open(file_path, 'wb') as f:
            frontmatter.dump(post, f)
        
        return True
    
    except Exception as e:
        return False


def auto_fix_frontmatter(component_type, file_path, frontmatter, result, dry_run=False):
    """Automatically fix common frontmatter issues (safe, single-file fixes)."""
    spec = COMPONENT_SPECS[component_type]
    fixed = False
    fixes_made = []
    
    if frontmatter is None:
        return False
    
    # Make a copy to modify
    updated = dict(frontmatter)
    
    # Fix 1: Capitalize status values
    if 'status' in updated and 'allowed_status' in spec:
        old_status = updated['status']
        # Try to find matching status with different case
        for allowed in spec['allowed_status']:
            if old_status.lower() == allowed.lower() and old_status != allowed:
                updated['status'] = allowed
                fixes_made.append(f"Capitalized status: '{old_status}' → '{allowed}'")
                fixed = True
                break
    
    # Fix 2: Capitalize priority values
    if 'priority' in updated and 'allowed_priority' in spec:
        old_priority = updated['priority']
        for allowed in spec['allowed_priority']:
            if old_priority.lower() == allowed.lower() and old_priority != allowed:
                updated['priority'] = allowed
                fixes_made.append(f"Capitalized priority: '{old_priority}' → '{allowed}'")
                fixed = True
                break
    
    # Fix 3: Add missing last_updated (use created date or today)
    if 'last_updated' in spec['required_fields'] and 'last_updated' not in updated:
        if 'created' in updated:
            updated['last_updated'] = updated['created']
            fixes_made.append(f"Added last_updated: {updated['created']} (from created)")
        else:
            today = datetime.now().strftime('%Y-%m-%d')
            updated['last_updated'] = today
            fixes_made.append(f"Added last_updated: {today}")
        fixed = True
    
    # Fix 4: Add missing category for backlog (infer from directory)
    if component_type == 'backlog' and 'category' not in updated:
        # Infer from directory structure
        if 'documentation' in file_path:
            updated['category'] = 'documentation'
        elif 'features' in file_path:
            updated['category'] = 'features'
        elif 'bugs' in file_path:
            updated['category'] = 'bugs'
        elif 'infrastructure' in file_path:
            updated['category'] = 'infrastructure'
        else:
            updated['category'] = 'features'  # default
        fixes_made.append(f"Added category: '{updated['category']}' (inferred from path)")
        fixed = True
    
    # Fix 5: Add missing related_cips for backlog (empty array)
    if component_type == 'backlog' and 'related_cips' not in updated:
        updated['related_cips'] = []
        fixes_made.append("Added related_cips: [] (empty)")
        fixed = True
    
    # Fix 6: Add missing related_tenets for requirements (empty array)
    if component_type == 'requirement' and 'related_tenets' not in updated:
        updated['related_tenets'] = []
        fixes_made.append("Added related_tenets: [] (empty)")
        fixed = True
    
    # Apply fixes
    if fixed:
        if write_frontmatter(file_path, updated, dry_run):
            for fix in fixes_made:
                result.add_fix(fix, file_path)
            return True
    
    return False


def find_component_file_by_id(root_dir, component_type, target_id):
    """Find a component file by its ID."""
    spec = COMPONENT_SPECS[component_type]
    component_dir = os.path.join(root_dir, spec['dir'])
    
    if not os.path.exists(component_dir):
        return None
    
    # Search for file with matching ID
    for root, dirs, files in os.walk(component_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            fm = extract_frontmatter(file_path)
            if fm and fm.get('id') == target_id:
                return file_path
    
    return None


def fix_reverse_links(root_dir, result, dry_run=False):
    """
    Fix reverse links by moving references to the correct direction.
    
    Bottom-up pattern:
    - Requirements link to Tenets (related_tenets)
    - CIPs link to Requirements (related_requirements)
    - Backlog links to CIPs (related_cips)
    
    This function detects reverse links and moves them to the correct file.
    """
    fixes_applied = 0
    
    # Pattern: requirement → tenet (requirement should link UP to tenet)
    # If tenet has related_requirements, move to requirement's related_tenets
    for tenet_file in find_component_files(root_dir, 'tenet'):
        tenet_fm = extract_frontmatter(tenet_file)
        if not tenet_fm or 'related_requirements' not in tenet_fm:
            continue
        
        tenet_id = tenet_fm.get('id')
        reverse_links = tenet_fm.get('related_requirements', [])
        
        for req_id in reverse_links:
            req_file = find_component_file_by_id(root_dir, 'requirement', req_id)
            if not req_file:
                result.add_warning(f"Cannot fix reverse link: requirement '{req_id}' not found", tenet_file)
                continue
            
            # Update requirement to link to tenet
            req_fm = extract_frontmatter(req_file)
            if not req_fm:
                continue
            
            if 'related_tenets' not in req_fm:
                req_fm['related_tenets'] = []
            
            if tenet_id not in req_fm['related_tenets']:
                req_fm['related_tenets'].append(tenet_id)
                write_frontmatter(req_file, req_fm, dry_run)
                result.add_fix(f"Moved link: Added tenet '{tenet_id}' to related_tenets", req_file)
                fixes_applied += 1
        
        # Remove reverse link from tenet
        tenet_fm_updated = dict(tenet_fm)
        del tenet_fm_updated['related_requirements']
        write_frontmatter(tenet_file, tenet_fm_updated, dry_run)
        result.add_fix(f"Removed reverse link: related_requirements (moved to requirements)", tenet_file)
    
    # Pattern: CIP → requirement (CIP should link UP to requirement)
    # If requirement has related_cips, move to CIP's related_requirements
    for req_file in find_component_files(root_dir, 'requirement'):
        req_fm = extract_frontmatter(req_file)
        if not req_fm or 'related_cips' not in req_fm:
            continue
        
        req_id = req_fm.get('id')
        reverse_links = req_fm.get('related_cips', [])
        
        for cip_id in reverse_links:
            cip_file = find_component_file_by_id(root_dir, 'cip', cip_id)
            if not cip_file:
                result.add_warning(f"Cannot fix reverse link: CIP '{cip_id}' not found", req_file)
                continue
            
            # Update CIP to link to requirement
            cip_fm = extract_frontmatter(cip_file)
            if not cip_fm:
                continue
            
            if 'related_requirements' not in cip_fm:
                cip_fm['related_requirements'] = []
            
            if req_id not in cip_fm['related_requirements']:
                cip_fm['related_requirements'].append(req_id)
                write_frontmatter(cip_file, cip_fm, dry_run)
                result.add_fix(f"Moved link: Added requirement '{req_id}' to related_requirements", cip_file)
                fixes_applied += 1
        
        # Remove reverse link from requirement
        req_fm_updated = dict(req_fm)
        del req_fm_updated['related_cips']
        write_frontmatter(req_file, req_fm_updated, dry_run)
        result.add_fix(f"Removed reverse link: related_cips (moved to CIPs)", req_file)
    
    # Pattern: backlog → CIP (backlog should link UP to CIP)
    # If CIP has related_backlog, move to backlog's related_cips
    for cip_file in find_component_files(root_dir, 'cip'):
        cip_fm = extract_frontmatter(cip_file)
        if not cip_fm or 'related_backlog' not in cip_fm:
            continue
        
        cip_id = cip_fm.get('id')
        reverse_links = cip_fm.get('related_backlog', [])
        
        for backlog_id in reverse_links:
            backlog_file = find_component_file_by_id(root_dir, 'backlog', backlog_id)
            if not backlog_file:
                result.add_warning(f"Cannot fix reverse link: backlog '{backlog_id}' not found", cip_file)
                continue
            
            # Update backlog to link to CIP
            backlog_fm = extract_frontmatter(backlog_file)
            if not backlog_fm:
                continue
            
            if 'related_cips' not in backlog_fm:
                backlog_fm['related_cips'] = []
            
            if cip_id not in backlog_fm['related_cips']:
                backlog_fm['related_cips'].append(cip_id)
                write_frontmatter(backlog_file, backlog_fm, dry_run)
                result.add_fix(f"Moved link: Added CIP '{cip_id}' to related_cips", backlog_file)
                fixes_applied += 1
        
        # Remove reverse link from CIP
        cip_fm_updated = dict(cip_fm)
        del cip_fm_updated['related_backlog']
        write_frontmatter(cip_file, cip_fm_updated, dry_run)
        result.add_fix(f"Removed reverse link: related_backlog (moved to backlog items)", cip_file)
    
    # Pattern: backlog → requirement (Option B - allowed only with explicit justification)
    for backlog_file in find_component_files(root_dir, 'backlog'):
        backlog_fm = extract_frontmatter(backlog_file)
        if not backlog_fm or not backlog_fm.get('related_requirements'):
            continue

        related_cips = backlog_fm.get('related_cips')
        no_cip_reason = backlog_fm.get('no_cip_reason')
        if not isinstance(related_cips, list) or len(related_cips) != 0 or not isinstance(no_cip_reason, str) or not no_cip_reason.strip():
            result.add_warning(
                "Backlog has related_requirements but does not satisfy the exception conditions "
                "(requires related_cips: [] and non-empty no_cip_reason).",
                backlog_file,
            )
    
    return fixes_applied


def validate_file_naming(component_type, file_path, result):
    """Validate file naming conventions."""
    spec = COMPONENT_SPECS[component_type]
    filename = os.path.basename(file_path)
    
    pattern = re.compile(spec['pattern'])
    if not pattern.match(filename):
        result.add_error(
            f"File naming violation: '{filename}' doesn't match pattern {spec['pattern']}",
            file_path
        )
        return False
    
    return True


def validate_yaml_frontmatter(component_type, file_path, result, auto_fix=False, dry_run=False):
    """Validate YAML frontmatter structure."""
    spec = COMPONENT_SPECS[component_type]
    frontmatter = extract_frontmatter(file_path)
    
    if frontmatter is None:
        result.add_error(f"Missing or invalid YAML frontmatter", file_path)
        return None
    
    # Try auto-fix first if enabled
    if auto_fix:
        auto_fix_frontmatter(component_type, file_path, frontmatter, result, dry_run)
        # Re-read frontmatter after fixes (unless dry-run)
        if not dry_run:
            frontmatter = extract_frontmatter(file_path)
    
    # Check required fields
    for field in spec['required_fields']:
        if field not in frontmatter:
            result.add_error(f"Missing required field: '{field}'", file_path)
    
    # REQ-0010: Human attribution must be explicit for responsibility-bearing artifacts
    if component_type == 'cip':
        if 'author' in frontmatter:
            validate_human_attribution(component_type, file_path, 'author', frontmatter.get('author'), result)
    elif component_type == 'backlog':
        if 'owner' in frontmatter:
            validate_human_attribution(component_type, file_path, 'owner', frontmatter.get('owner'), result)

    # Backlog exception path (Option B):
    # Allow backlog to reference requirements directly ONLY when:
    # - related_cips exists and is empty (no CIP)
    # - no_cip_reason is present and non-empty (explicit justification)
    if component_type == 'backlog' and frontmatter.get('related_requirements'):
        related_reqs = frontmatter.get('related_requirements')
        if not isinstance(related_reqs, list):
            result.add_error("Invalid 'related_requirements': expected list of requirement IDs", file_path)
        related_cips = frontmatter.get('related_cips')
        if related_cips is None:
            result.add_error("Invalid exception: backlog has related_requirements but missing required field 'related_cips'", file_path)
        elif not isinstance(related_cips, list):
            result.add_error("Invalid 'related_cips': expected list", file_path)
        elif len(related_cips) != 0:
            result.add_error(
                "Invalid exception: backlog has related_requirements but related_cips is non-empty (use a CIP instead of direct requirement linkage)",
                file_path,
            )
        no_cip_reason = frontmatter.get('no_cip_reason')
        if not isinstance(no_cip_reason, str) or not no_cip_reason.strip():
            result.add_error(
                "Invalid exception: backlog has related_requirements but missing/empty 'no_cip_reason' (explicit justification required)",
                file_path,
            )

    # Validate field values
    if 'status' in frontmatter:
        if 'allowed_status' in spec:
            if frontmatter['status'] not in spec['allowed_status']:
                result.add_error(
                    f"Invalid status: '{frontmatter['status']}'. Allowed: {spec['allowed_status']}",
                    file_path
                )
    
    if 'priority' in frontmatter:
        if 'allowed_priority' in spec:
            if frontmatter['priority'] not in spec['allowed_priority']:
                result.add_error(
                    f"Invalid priority: '{frontmatter['priority']}'. Allowed: {spec['allowed_priority']}",
                    file_path
                )
    
    # Validate date formats
    for date_field in ['created', 'last_updated', 'last_reviewed']:
        if date_field in frontmatter:
            date_str = frontmatter[date_field]
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_str)):
                result.add_error(
                    f"Invalid date format for '{date_field}': '{date_str}'. Expected YYYY-MM-DD",
                    file_path
                )
    
    # Check for fields that violate bottom-up pattern
    for field in spec['should_not_have']:
        if field in frontmatter and frontmatter[field]:
            result.add_warning(
                f"Violates bottom-up pattern: Has '{field}' field. {component_type}s should only link upward",
                file_path
            )
    
    return frontmatter


def find_component_files(root_dir, component_type):
    """Find all files for a component type."""
    spec = COMPONENT_SPECS[component_type]
    component_dir = os.path.join(root_dir, spec['dir'])
    
    if not os.path.exists(component_dir):
        return []
    
    files = []
    pattern = re.compile(spec['pattern'])
    
    for root, dirs, filenames in os.walk(component_dir):
        # Skip template files and README
        if 'templates' in root or 'template' in root.lower():
            continue
        
        # System/template files to exclude
        excluded_files = {'readme.md', 'tenet_template.md', 'task_template.md', 'cip_template.md', 'requirement_template.md', 'vibesafe-tenets.md', 'index.md'}
        
        for filename in filenames:
            if filename.lower() in excluded_files:
                continue
            if filename.endswith('.md') and pattern.match(filename):
                files.append(os.path.join(root, filename))
    
    return files


def collect_all_ids(root_dir):
    """Collect all component IDs for cross-reference validation."""
    all_ids = {
        'requirement': set(),
        'cip': set(),
        'backlog': set(),
        'tenet': set(),
    }
    
    for component_type in all_ids.keys():
        files = find_component_files(root_dir, component_type)
        for file_path in files:
            frontmatter = extract_frontmatter(file_path)
            if frontmatter and 'id' in frontmatter:
                all_ids[component_type].add(frontmatter['id'])
    
    return all_ids


def validate_cross_references(component_type, file_path, frontmatter, all_ids, result):
    """Validate cross-references to other components."""
    spec = COMPONENT_SPECS[component_type]
    
    for link_field in spec['links_to']:
        if link_field in frontmatter:
            refs = frontmatter[link_field]
            if not isinstance(refs, list):
                refs = [refs]
            
            # Determine target component type from field name
            target_type = None
            if 'tenet' in link_field:
                target_type = 'tenet'
            elif 'requirement' in link_field:
                target_type = 'requirement'
            elif 'cip' in link_field:
                target_type = 'cip'
            elif 'backlog' in link_field:
                target_type = 'backlog'
            
            if target_type:
                for ref_id in refs:
                    if ref_id not in all_ids[target_type]:
                        result.add_warning(
                            f"Broken reference: {link_field} references '{ref_id}' which doesn't exist",
                            file_path
                        )

    # Backlog exception path (Option B): if related_requirements is present, validate requirement IDs.
    if component_type == 'backlog' and frontmatter.get('related_requirements'):
        refs = frontmatter.get('related_requirements')
        if not isinstance(refs, list):
            refs = [refs]
        for ref_id in refs:
            if ref_id not in all_ids.get('requirement', set()):
                result.add_warning(
                    f"Broken reference: related_requirements references '{ref_id}' which doesn't exist",
                    file_path,
                )


def validate_component(root_dir, component_type, file_path, all_ids, result, auto_fix=False, dry_run=False):
    """Validate a single component file."""
    # 1. File naming
    if not validate_file_naming(component_type, file_path, result):
        return  # Skip further validation if filename is wrong
    
    # 2. YAML frontmatter
    frontmatter = validate_yaml_frontmatter(component_type, file_path, result, auto_fix, dry_run)
    if frontmatter is None:
        return  # Skip further validation if no frontmatter
    
    # 3. Cross-references
    validate_cross_references(component_type, file_path, frontmatter, all_ids, result)


def print_results(result, strict=False, dry_run=False):
    """Print validation results with color coding."""
    print()
    print(colored("═" * 70, Colors.BLUE))
    if dry_run:
        print(colored("  VibeSafe Structure Validation Results (DRY RUN)", Colors.BOLD + Colors.BLUE))
    else:
        print(colored("  VibeSafe Structure Validation Results", Colors.BOLD + Colors.BLUE))
    print(colored("═" * 70, Colors.BLUE))
    print()
    
    # Fixes (if any)
    if result.fixes:
        fix_verb = "Would fix" if dry_run else "Fixed"
        print(colored(f"🔧 {fix_verb.upper()} ({len(result.fixes)}):", Colors.GREEN + Colors.BOLD))
        current_file = None
        for message, file_path in result.fixes:
            if file_path:
                rel_path = os.path.relpath(file_path)
                if rel_path != current_file:
                    print(colored(f"  {rel_path}:", Colors.GREEN))
                    current_file = rel_path
                print(f"    {message}")
            else:
                print(f"  {message}")
        print()
    
    # Errors
    if result.errors:
        print(colored(f"❌ ERRORS ({len(result.errors)}):", Colors.RED + Colors.BOLD))
        for message, file_path in result.errors:
            if file_path:
                rel_path = os.path.relpath(file_path)
                print(colored(f"  {rel_path}:", Colors.RED))
                print(f"    {message}")
            else:
                print(f"  {message}")
        print()
    else:
        print(colored("✅ No errors found", Colors.GREEN + Colors.BOLD))
        print()
    
    # Warnings
    if result.warnings:
        status_symbol = "❌" if strict else "⚠️ "
        status_text = "ERRORS" if strict else "WARNINGS"
        print(colored(f"{status_symbol} {status_text} ({len(result.warnings)}):", Colors.YELLOW + Colors.BOLD))
        for message, file_path in result.warnings:
            if file_path:
                rel_path = os.path.relpath(file_path)
                print(colored(f"  {rel_path}:", Colors.YELLOW))
                print(f"    {message}")
            else:
                print(f"  {message}")
        print()
    else:
        print(colored("✅ No warnings", Colors.GREEN + Colors.BOLD))
        print()
    
    # Info
    if result.info:
        print(colored(f"ℹ️  INFO:", Colors.BLUE + Colors.BOLD))
        for message in result.info:
            print(f"  {message}")
        print()
    
    # Summary
    print(colored("─" * 70, Colors.BLUE))
    if not result.has_errors() and (not strict or not result.has_warnings()):
        print(colored("🎉 Validation PASSED!", Colors.GREEN + Colors.BOLD))
        print(colored("   VibeSafe structure conforms to requirements (REQ-0001, REQ-0006)", Colors.GREEN))
    else:
        print(colored("❌ Validation FAILED", Colors.RED + Colors.BOLD))
        if strict and result.has_warnings():
            print(colored("   (Warnings treated as errors in --strict mode)", Colors.RED))
    
    if dry_run and result.has_fixes():
        print()
        print(colored("   To apply automatic fixes, run:", Colors.BLUE))
        print(colored("   ./scripts/validate_vibesafe_structure.py --fix --fix-links", Colors.BOLD))
    
    print(colored("─" * 70, Colors.BLUE))
    print()


def check_system_file_drift(root_dir, result):
    """
    Check for drift between runtime files and templates/
    
    Per CIP-000E (Clean Installation Philosophy), templates/ is the source 
    of truth for system files that propagate on install. This validates that 
    runtime files haven't diverged from their templates.
    
    Args:
        root_dir: Root directory of the repository
        result: ValidationResult to update
    """
    def _read_text_normalized(path: str) -> str:
        # Normalize newlines to avoid false drift due to editor/platform settings.
        with open(path, "r", encoding="utf-8") as f:
            return f.read().replace("\r\n", "\n")

    def _check_pair(template_rel: str, runtime_rel: str) -> None:
        template_path = os.path.join(root_dir, template_rel)
        runtime_path = os.path.join(root_dir, runtime_rel)

        if not os.path.exists(template_path):
            # Template missing is a real problem: templates are the canonical source.
            result.add_error(f"Missing template system file: {template_rel}", template_path)
            return

        if not os.path.exists(runtime_path):
            # In this repo, runtime copies may be absent (templates are canonical).
            # In downstream projects, these are materialized on install.
            return

        # Compare content; only warn on divergence.
        try:
            template_text = _read_text_normalized(template_path)
            runtime_text = _read_text_normalized(runtime_path)
        except Exception as e:
            result.add_warning(f"Could not read system file drift pair ({runtime_rel}): {e}", runtime_path)
            return

        if template_text == runtime_text:
            return

        # Heuristic: if runtime copy is newer, it's likely an agent edited the wrong file.
        try:
            template_mtime = os.path.getmtime(template_path)
            runtime_mtime = os.path.getmtime(runtime_path)
        except Exception:
            template_mtime = None
            runtime_mtime = None

        ahead = (
            runtime_mtime is not None
            and template_mtime is not None
            and runtime_mtime > template_mtime
        )

        # Drift is treated as an error when templates are present: it indicates a
        # process problem (wrong file edited) or a missing propagation step.
        if ahead:
            result.add_error(
                "System file drift (runtime AHEAD of templates): "
                f"{runtime_rel} differs from {template_rel}. "
                "This strongly suggests an agent edited the runtime copy instead of the canonical template. "
                "Port the changes into templates/ (preferred), then reinstall/recopy runtime files as needed.",
                runtime_path,
            )
        else:
            result.add_error(
                "System file drift (runtime differs from templates): "
                f"{runtime_rel} differs from {template_rel}. "
                "If templates/ is canonical (VibeSafe repo), update templates/ then reinstall/recopy runtime files. "
                "If this is a downstream project, reinstall will refresh runtime from templates.",
                runtime_path,
            )

    # Only enforce drift checks when templates exist (VibeSafe repo / dogfood).
    # In downstream projects, templates/ won't be present and drift checks should be skipped.
    if not os.path.isdir(os.path.join(root_dir, "templates")):
        return

    # Focused pairs that the installer materializes from templates.
    # (We intentionally do NOT require these runtime copies to exist.)
    _check_pair("templates/scripts/whats_next.py", "scripts/whats_next.py")
    _check_pair("templates/scripts/validate_vibesafe_structure.py", "scripts/validate_vibesafe_structure.py")
    _check_pair("templates/backlog/update_index.py", "backlog/update_index.py")
    _check_pair("templates/tenets/combine_tenets.py", "tenets/combine_tenets.py")


def main():
    parser = argparse.ArgumentParser(
        description='Validate VibeSafe structure against requirements (REQ-0001, REQ-0006)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Validate all components
  %(prog)s --component req    # Validate only requirements
  %(prog)s --strict           # Treat warnings as errors
  %(prog)s --no-color         # Disable colored output
        """
    )
    
    parser.add_argument(
        '--component',
        choices=['req', 'cip', 'backlog', 'tenet'],
        help='Validate only specific component type'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (exit code 1 if any warnings)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix simple issues (capitalization, missing fields)'
    )
    parser.add_argument(
        '--fix-links',
        action='store_true',
        help='Fix reverse links by moving references to correct files (multi-file operation)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes (implies --fix and --fix-links if specified)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    parser.add_argument(
        '--no-governance-drift',
        action='store_true',
        help='Skip git-based governance drift warnings (implementation changes without CIP/backlog updates)'
    )
    parser.add_argument(
        '--root',
        default='.',
        help='Root directory of VibeSafe project (default: current directory)'
    )
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    # --dry-run implies --fix and --fix-links (if specified)
    auto_fix = args.fix or args.dry_run
    fix_links = args.fix_links or (args.dry_run and args.fix_links)
    dry_run = args.dry_run
    
    root_dir = os.path.abspath(args.root)
    result = ValidationResult()
    
    # Determine which components to validate
    if args.component:
        component_map = {
            'req': 'requirement',
            'cip': 'cip',
            'backlog': 'backlog',
            'tenet': 'tenet'
        }
        components_to_validate = [component_map[args.component]]
    else:
        components_to_validate = ['requirement', 'cip', 'backlog', 'tenet']
    
    # Step 1: Fix reverse links first (if requested)
    # This must happen before validation to avoid false positives
    if args.fix_links:
        result.add_info("Fixing reverse links...")
        fixes_count = fix_reverse_links(root_dir, result, dry_run)
        result.add_info(f"Reverse link fixes applied: {fixes_count}")
    
    # Step 2: Collect all IDs for cross-reference validation
    all_ids = collect_all_ids(root_dir)
    
    # Step 3: Validate each component type
    for component_type in components_to_validate:
        files = find_component_files(root_dir, component_type)
        result.add_info(f"Found {len(files)} {component_type} file(s)")
        
        for file_path in files:
            validate_component(root_dir, component_type, file_path, all_ids, result, auto_fix, dry_run)
    
    # Step 4: Check for system file drift (REQ-0006)
    check_system_file_drift(root_dir, result)

    # Step 5: Optional git-based process warnings
    if not args.no_governance_drift:
        check_governance_drift(root_dir, result)
    
    # Print results
    print_results(result, strict=args.strict, dry_run=dry_run)
    
    # Exit code
    if result.has_errors():
        sys.exit(1)
    elif args.strict and result.has_warnings():
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

