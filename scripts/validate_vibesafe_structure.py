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


# Component specifications (from REQ-0001: Standardized Component Metadata)
COMPONENT_SPECS = {
    'requirement': {
        'dir': 'requirements',
        'pattern': r'^req([0-9A-Fa-f]{4})_[\w-]+\.md$',
        'id_format': 'XXXX (4-digit hex)',
        'required_fields': ['id', 'title', 'status', 'priority', 'created', 'last_updated', 'related_tenets', 'stakeholders'],
        'optional_fields': ['related_cips', 'related_backlog', 'tags'],
        'allowed_status': ['Proposed', 'Ready', 'In Progress', 'Implemented', 'Validated', 'Deferred', 'Rejected'],
        'allowed_priority': ['High', 'Medium', 'Low'],
        'links_to': ['related_tenets'],  # Bottom-up: requirements → tenets
        'should_not_have': ['related_requirements'],  # Violates bottom-up
    },
    'cip': {
        'dir': 'cip',
        'pattern': r'^cip([0-9A-Fa-f]{4})(_[\w-]+)?\.md$',
        'id_format': 'XXXX (4-digit hex)',
        'required_fields': ['id', 'title', 'status', 'created', 'last_updated'],
        'optional_fields': ['author', 'related_requirements', 'related_cips', 'tags'],
        'allowed_status': ['Proposed', 'Accepted', 'Implemented', 'Closed', 'Rejected'],
        'links_to': ['related_requirements'],  # Bottom-up: CIPs → requirements
        'should_not_have': ['related_backlog'],  # Violates bottom-up
    },
    'backlog': {
        'dir': 'backlog',
        'pattern': r'^(\d{4})-(\d{2})-(\d{2})_[\w-]+\.md$',
        'id_format': 'YYYY-MM-DD_short-name',
        'required_fields': ['id', 'title', 'status', 'priority', 'created', 'last_updated', 'category', 'related_cips'],
        'optional_fields': ['owner', 'dependencies', 'tags'],
        'allowed_status': ['Proposed', 'Ready', 'In Progress', 'Completed', 'Abandoned'],
        'allowed_priority': ['High', 'Medium', 'Low'],
        'links_to': ['related_cips'],  # Bottom-up: backlog → CIPs
        'should_not_have': ['related_requirements'],  # Violates bottom-up
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
    """Automatically fix common frontmatter issues."""
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
        
        for filename in filenames:
            if filename.lower() == 'readme.md':
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
        print(colored("   Run without --dry-run to apply fixes", Colors.BLUE))
    
    print(colored("─" * 70, Colors.BLUE))
    print()


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
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes (implies --fix)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    parser.add_argument(
        '--root',
        default='.',
        help='Root directory of VibeSafe project (default: current directory)'
    )
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    # --dry-run implies --fix
    auto_fix = args.fix or args.dry_run
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
    
    # Collect all IDs for cross-reference validation
    all_ids = collect_all_ids(root_dir)
    
    # Validate each component type
    for component_type in components_to_validate:
        files = find_component_files(root_dir, component_type)
        result.add_info(f"Found {len(files)} {component_type} file(s)")
        
        for file_path in files:
            validate_component(root_dir, component_type, file_path, all_ids, result, auto_fix, dry_run)
    
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

