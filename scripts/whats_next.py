#!/usr/bin/env python3
"""What's Next Script for VibeSafe.

This script summarizes the current project status and identifies pending tasks,
helping LLMs quickly understand project context and prioritize future work.

The script provides a comprehensive overview of:
- Git repository status
- CIP (Change Implementation Proposal) status
- Backlog item status
- Requirements status

The script accepts status values in multiple formats for backlog items:
- Lowercase with underscores: "proposed", "in_progress", "completed"
- Capitalized with spaces: "Proposed", "In Progress", "Completed"  
- Mixed case: "Ready", "abandoned", etc.
All formats are normalized internally to lowercase with underscores.

Usage:
    python whats_next.py [--no-git] [--no-color] [--cip-only] [--backlog-only] [--requirements-only]

Options:
    --no-git              Skip Git status information
    --no-color           Disable colored output
    --cip-only           Show only CIP status
    --backlog-only       Show only backlog status
    --requirements-only  Show only requirements status

Returns:
    None. Outputs formatted status information to stdout.
"""

import os
import sys
import subprocess
import re
import glob
import argparse
from datetime import datetime
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output.
    
    This class provides color constants for terminal output formatting.
    Colors can be disabled using the disable() class method.
    """
    
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def disable(cls):
        """Disable all colors by setting them to empty strings."""
        cls.HEADER = ''
        cls.BLUE = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.ENDC = ''
        cls.BOLD = ''
        cls.UNDERLINE = ''

def normalize_status(status):
    """Normalize status to lowercase with underscores."""
    if not status:
        return None
    # Convert to lowercase and replace spaces with underscores
    return status.lower().replace(' ', '_').replace('-', '_')

def print_section(title: str):
    """Print a formatted section header.
    
    Args:
        title: The title text to display in the section header.
    """
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def run_command(command: List[str]) -> Tuple[str, int]:
    """Run a shell command and return its output and exit code.
    
    Args:
        command: List of command and arguments to run.
        
    Returns:
        Tuple containing:
            - Command output as string
            - Exit code as integer
    """
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=False
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return f"Error executing command: {e}", 1

def get_git_status() -> Dict[str, Any]:
    """Get Git repository status information.
    
    Collects information about:
    - Current branch
    - Recent commits (last 5)
    - Modified files
    - Untracked files
    
    Returns:
        Dictionary containing Git status information.
    """
    git_info = {}
    
    # Get current branch
    branch_output, _ = run_command(['git', 'branch', '--show-current'])
    git_info['current_branch'] = branch_output
    
    # Get recent commits
    commits_output, _ = run_command(['git', 'log', '--oneline', '-n', '5'])
    git_info['recent_commits'] = [
        {
            'hash': line.split(' ')[0],
            'message': ' '.join(line.split(' ')[1:])
        }
        for line in commits_output.split('\n') if line.strip()
    ]
    
    # Get modified/untracked files
    status_output, _ = run_command(['git', 'status', '--porcelain'])
    git_info['modified_files'] = []
    git_info['untracked_files'] = []
    
    for line in status_output.split('\n'):
        if not line.strip():
            continue
        status = line[:2]
        file_path = line[3:].strip()
        
        if status.startswith('??'):
            git_info['untracked_files'].append(file_path)
        else:
            git_info['modified_files'].append({
                'status': status.strip(),
                'path': file_path
            })
    
    return git_info

def extract_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from a markdown file if it exists.
    
    Args:
        file_path: Path to the markdown file.
        
    Returns:
        Dictionary containing frontmatter data if found, None otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file has YAML frontmatter (between --- markers)
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            yaml_content = frontmatter_match.group(1)
            return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"Error reading frontmatter from {file_path}: {e}")
    
    return None

def has_expected_frontmatter(file_path: str, expected_keys: List[str]) -> bool:
    """Check if a file has all the expected frontmatter keys.
    
    Args:
        file_path: Path to the markdown file.
        expected_keys: List of required frontmatter keys.
        
    Returns:
        True if all expected keys are present, False otherwise.
    """
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return False
    
    for key in expected_keys:
        if key not in frontmatter:
            return False
    
    return True

def scan_cips() -> Dict[str, Any]:
    """Scan all CIP files and collect their status.
    
    Collects information about:
    - Total number of CIPs
    - CIPs with/without frontmatter
    - CIPs by status (proposed, accepted, implemented, closed)
    - CIP details including title and dates
    
    Returns:
        Dictionary containing CIP status information.
    """
    cips_info = {
        'total': 0,
        'with_frontmatter': 0,
        'without_frontmatter': [],
        'by_status': {
            'proposed': [],
            'accepted': [],
            'implemented': [],
            'closed': []
        }
    }
    
    # Expected frontmatter keys for CIPs
    expected_keys = ['id', 'title', 'status', 'created', 'last_updated']
    
    for cip_file in sorted(glob.glob('cip/cip*.md')):
        if cip_file == 'cip/cip_template.md':
            continue
            
        cips_info['total'] += 1
        file_id = os.path.basename(cip_file).replace('.md', '')
        
        frontmatter = extract_frontmatter(cip_file)
        if frontmatter:
            cips_info['with_frontmatter'] += 1
            status = frontmatter.get('status', 'unknown').lower()
            
            if status == 'proposed':
                cips_info['by_status']['proposed'].append({
                    'id': file_id,
                    'title': frontmatter.get('title', 'Untitled'),
                    'date': frontmatter.get('created', 'Unknown')
                })
            elif status == 'accepted':
                cips_info['by_status']['accepted'].append({
                    'id': file_id,
                    'title': frontmatter.get('title', 'Untitled')
                })
            elif status == 'implemented':
                cips_info['by_status']['implemented'].append({
                    'id': file_id,
                    'title': frontmatter.get('title', 'Untitled')
                })
            elif status == 'closed':
                cips_info['by_status']['closed'].append({
                    'id': file_id,
                    'title': frontmatter.get('title', 'Untitled')
                })
        else:
            # Extract information from CIP using regex if no frontmatter
            with open(cip_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title_match = re.search(r'# CIP-[0-9A-F]+:\s*(.*)', content)
            title = title_match.group(1) if title_match else "Untitled"
            
            status_match = re.search(r'## Status.*?- \[x\] (\w+)', content, re.DOTALL)
            status = status_match.group(1).lower() if status_match else "unknown"
            
            cips_info['without_frontmatter'].append({
                'id': file_id,
                'title': title,
                'path': cip_file
            })
            
            # Add to status lists even without frontmatter
            if status == 'proposed':
                cips_info['by_status']['proposed'].append({
                    'id': file_id,
                    'title': title,
                    'no_frontmatter': True
                })
            elif status == 'accepted':
                cips_info['by_status']['accepted'].append({
                    'id': file_id,
                    'title': title,
                    'no_frontmatter': True
                })
            elif status == 'implemented':
                cips_info['by_status']['implemented'].append({
                    'id': file_id,
                    'title': title,
                    'no_frontmatter': True
                })
            elif status == 'closed':
                cips_info['by_status']['closed'].append({
                    'id': file_id,
                    'title': title,
                    'no_frontmatter': True
                })
    
    return cips_info

def scan_backlog() -> Dict[str, Any]:
    """Scan all backlog items and collect their status."""
    backlog_info = {
        'total': 0,
        'with_frontmatter': 0,
        'without_frontmatter': [],
        'by_priority': {
            'high': [],
            'medium': [],
            'low': []
        },
        'by_status': {
            'proposed': [],
            'ready': [],
            'in_progress': [],
            'completed': [],
            'abandoned': [],
            'superseded': []
        }
    }
    
    # Expected frontmatter keys for backlog items
    expected_keys = ['id', 'title', 'status', 'priority', 'created', 'last_updated']
    
    # Backlog directories to scan
    backlog_dirs = [
        'backlog/bugs/',
        'backlog/features/',
        'backlog/documentation/',
        'backlog/infrastructure/'
    ]
    
    for directory in backlog_dirs:
        if not os.path.exists(directory):
            continue
            
        for backlog_file in sorted(glob.glob(f'{directory}/*.md')):
            if 'task_template.md' in backlog_file:
                continue
                
            backlog_info['total'] += 1
            file_id = os.path.basename(backlog_file).replace('.md', '')
            
            frontmatter = extract_frontmatter(backlog_file)
            if frontmatter:
                backlog_info['with_frontmatter'] += 1
                status = normalize_status(frontmatter.get('status', 'unknown'))
                priority = frontmatter.get('priority', 'unknown').lower()
                
                item_info = {
                    'id': file_id,
                    'title': frontmatter.get('title', 'Untitled'),
                    'path': backlog_file
                }
                
                # Add to priority lists
                if priority in backlog_info['by_priority']:
                    backlog_info['by_priority'][priority].append(item_info)
                
                # Add to status lists
                if status in backlog_info['by_status']:
                    backlog_info['by_status'][status].append(item_info)
            else:
                # Extract information from backlog item using regex if no frontmatter
                with open(backlog_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title_match = re.search(r'# Task:\s*(.*)', content)
                title = title_match.group(1) if title_match else "Untitled"
                
                status_match = re.search(r'- \*\*Status\*\*:\s*(\w+)', content)
                status = normalize_status(status_match.group(1)) if status_match else "unknown"
                
                priority_match = re.search(r'- \*\*Priority\*\*:\s*(\w+)', content)
                priority = priority_match.group(1).lower() if priority_match else "unknown"
                
                item_info = {
                    'id': file_id,
                    'title': title,
                    'path': backlog_file,
                    'no_frontmatter': True
                }
                
                backlog_info['without_frontmatter'].append(item_info)
                
                # Add to priority lists even without frontmatter
                if priority in backlog_info['by_priority']:
                    backlog_info['by_priority'][priority].append(item_info)
                
                # Add to status lists even without frontmatter
                if status in backlog_info['by_status']:
                    backlog_info['by_status'][status].append(item_info)
    
    return backlog_info

def scan_requirements() -> Dict[str, Any]:
    """Scan the requirements directory and collect information."""
    requirements_info = {
        'has_framework': os.path.isdir('requirements'),
        'has_template': os.path.exists('requirements/requirement_template.md'),
        'patterns': [],
        'prompts': {
            'discovery': [],
            'refinement': [],
            'validation': [],
            'testing': []
        },
        'integrations': [],
        'examples': [],
        'guidance': []
    }
    
    # Check if the requirements framework is present
    if not requirements_info['has_framework']:
        return requirements_info
    
    # Note: The old ai-requirements/ structure with patterns/prompts/etc. has been
    # simplified to just requirements/ with flat or optional categorization.
    # This scan function is kept for backwards compatibility but will be simplified
    # in future versions to just check for requirements/*.md files.
    
    return requirements_info

def detect_codebase() -> bool:
    """Detect if there's a codebase (source code files) in the project.
    
    Excludes VibeSafe system files and common non-code directories.
    """
    source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', 
                        '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.swift', '.kt'}
    
    # VibeSafe system directories and other directories to exclude
    exclude_dirs = {
        'scripts',  # VibeSafe system scripts
        'templates',  # VibeSafe templates
        '.venv', '.venv-vibesafe',  # Virtual environments
        'node_modules', '__pycache__', '.git',  # Dependencies and system
        'venv', 'env',  # Other common venv names
        'cip', 'backlog', 'tenets', 'requirements',  # VibeSafe components
        'docs', 'doc', 'documentation',  # Documentation
        '.cursor', '.vscode', '.idea',  # IDE directories
    }
    
    # Check common source directories first
    source_dirs = ['src', 'lib', 'app', 'pkg', 'internal', 'core']
    
    for dir_name in source_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            for file in dir_path.rglob('*'):
                if file.suffix in source_extensions:
                    return True
    
    # Also check for Python packages in root or one level deep (e.g., myproject/myproject/)
    # This catches cases where the package is organized as: myproject/myproject/__init__.py
    root = Path('.')
    
    # Check root-level Python files (but not VibeSafe scripts)
    for file in root.glob('*.py'):
        if file.is_file() and file.name not in {'setup.py', 'conftest.py'}:
            return True
    
    # Check directories in root that might be Python packages or other source directories
    for item in root.iterdir():
        if item.is_dir() and item.name not in exclude_dirs and not item.name.startswith('.'):
            # Check if this directory has source files
            for file in item.rglob('*'):
                # Skip excluded subdirectories
                if any(excluded in file.parts for excluded in exclude_dirs):
                    continue
                if file.suffix in source_extensions:
                    return True
    
    return False


def detect_component(component_dir: str) -> bool:
    """Detect if a VibeSafe component exists with user content (not just templates)."""
    dir_path = Path(component_dir)
    
    if not dir_path.exists():
        return False
    
    # Template and system files to ignore
    system_files = {
        'README.md', 'readme.md',
        'task_template.md', 'cip_template.md', 'tenet_template.md', 'requirement_template.md',
        'combine_tenets.py', 'update_index.py',
        'index.md',  # Auto-generated
    }
    
    # Check for user content files
    for file in dir_path.rglob('*.md'):
        if file.name not in system_files and 'vibesafe' not in str(file.parent):
            return True
    
    return False


def detect_gaps() -> Dict[str, bool]:
    """Detect missing VibeSafe components."""
    return {
        'has_codebase': detect_codebase(),
        'has_tenets': detect_component('tenets'),
        'has_requirements': detect_component('requirements'),
        'has_cips': detect_component('cip'),
        'has_backlog': detect_component('backlog')
    }


def generate_ai_prompts(gaps: Dict[str, bool]) -> List[Dict[str, str]]:
    """Generate AI prompts based on detected gaps."""
    prompts = []
    
    # Priority 1: Tenets (foundation)
    if gaps['has_codebase'] and not gaps['has_tenets']:
        prompts.append({
            'type': 'create_tenets',
            'priority': 'high',
            'title': '📋 Create 3-5 tenets to capture your project\'s guiding principles',
            'prompt': '''Analyze this codebase and suggest 3-5 foundational tenets that capture
the project's design philosophy, architecture decisions, and priorities.

Look for:
- Recurring patterns in code organization
- Architectural decisions (e.g., modularity, separation of concerns)
- Design philosophy evident in code structure
- Trade-offs made (e.g., simplicity vs. features, performance vs. maintainability)
- User experience priorities

For each tenet, provide:
1. Title (short, memorable phrase)
2. Description (1-2 paragraphs explaining the principle)
3. Quote (one sentence that captures the essence)
4. Examples from the codebase
5. Counter-examples (what this tenet avoids)

Output format: tenets/[kebab-case-name].md with YAML frontmatter
(Use the template at tenets/tenet_template.md)

Once created, run ./whats-next again for next steps.'''
        })
    
    # Priority 2: Requirements (extracted from CIPs if they exist)
    elif gaps['has_tenets'] and gaps['has_cips'] and not gaps['has_requirements']:
        prompts.append({
            'type': 'extract_requirements',
            'priority': 'high',
            'title': '📋 Extract requirements (WHAT) from existing CIPs (HOW)',
            'prompt': '''Extract requirements from existing CIPs to establish WHAT needs to be achieved.

For each CIP, identify:
- What problem does it solve?
- What outcome is desired?
- What should be true after implementation?
- Which tenets does this support? (WHY)

Output format: requirements/req[XXXX]_short-name.md with YAML frontmatter
- Use hexadecimal numbering (req0001, req0002, ..., req000A, etc.)
- Link requirements back to tenets using related_tenets field
- Focus on desired outcomes (WHAT), not implementation (HOW)

After creating requirements:
- Update existing CIPs to reference the new requirements (related_requirements field)
- Run ./scripts/validate_vibesafe_structure.py --fix-links to fix any linking issues
- Run ./whats-next again for next steps'''
        })
    
    # Priority 3: CIPs (if requirements exist but no CIPs)
    elif gaps['has_requirements'] and not gaps['has_cips']:
        prompts.append({
            'type': 'create_cips',
            'priority': 'medium',
            'title': '📋 Create CIPs to design HOW to implement requirements',
            'prompt': '''Create CIPs (Code Improvement Proposals) to design HOW to implement requirements.

For each high-priority requirement:
- Design the implementation approach
- Identify affected components
- Plan the changes needed
- Consider trade-offs and alternatives

Output format: cip/cip[XXXX]_short-name.md with YAML frontmatter
- Use hexadecimal numbering (cip0001, cip0002, ..., cip000A, etc.)
- Link CIPs to requirements using related_requirements field
- Include: Description, Motivation, Implementation, Status

After creating CIPs:
- Run ./whats-next again for next steps'''
        })
    
    # Priority 4: Backlog (if CIPs exist but no backlog)
    elif gaps['has_cips'] and not gaps['has_backlog']:
        prompts.append({
            'type': 'create_backlog',
            'priority': 'medium',
            'title': '📋 Break down CIPs into actionable backlog tasks',
            'prompt': '''Break down CIPs into concrete backlog tasks.

For each CIP:
- Identify specific implementation steps
- Create tasks for each step
- Set priorities based on dependencies
- Link tasks to CIPs

Output format: backlog/[category]/YYYY-MM-DD_short-name.md with YAML frontmatter
- Categories: features, bugs, documentation, infrastructure
- Use today's date for new tasks
- Link backlog items to CIPs using related_cips field

After creating backlog:
- Run ./whats-next again to see task priorities'''
        })
    
    # Edge case: No components at all
    elif not any([gaps['has_tenets'], gaps['has_requirements'], gaps['has_cips'], gaps['has_backlog']]):
        if gaps['has_codebase']:
            prompts.append({
                'type': 'bootstrap_all',
                'priority': 'high',
                'title': '📋 Bootstrap VibeSafe: Start with tenets',
                'prompt': '''Your project has code but no VibeSafe components yet. Let's bootstrap!

Start by creating 3-5 tenets that capture your project's guiding principles.
(See the create_tenets prompt above for detailed guidance)

Recommended order:
1. Tenets (WHY) - Guiding principles
2. Requirements (WHAT) - Desired outcomes
3. CIPs (HOW) - Implementation plans
4. Backlog (DOING) - Concrete tasks'''
            })
    
    return prompts


def check_tenet_status(review_period_days: int = 180) -> Dict[str, Any]:
    """Check the status of project tenets.
    
    Args:
        review_period_days: Number of days after which tenets should be reviewed (default: 180 = 6 months)
    
    Returns:
        Dictionary containing tenet status information:
        - status: 'missing', 'empty', or 'exists'
        - count: Number of project tenets found
        - oldest_modification: Timestamp of oldest modification
        - newest_modification: Timestamp of newest modification
        - days_since_modification: Days since last modification
        - needs_review: Boolean indicating if review is recommended
        - files: List of tenet file paths
    """
    tenets_dir = Path("tenets")
    
    # Check if tenets directory exists
    if not tenets_dir.exists():
        return {
            "status": "missing",
            "message": "No tenets directory found",
            "count": 0,
            "needs_review": False
        }
    
    # Find project-specific tenet files (not VibeSafe system files)
    project_tenets = []
    system_files = ["README.md", "tenet_template.md", "combine_tenets.py", 
                    "vibesafe-tenets.md", "vibesafe-tenets.yaml"]
    
    for file in tenets_dir.rglob("*.md"):
        # Skip system files and files in vibesafe subdirectory
        if file.name not in system_files and "vibesafe" not in str(file.parent):
            project_tenets.append(file)
    
    if not project_tenets:
        return {
            "status": "empty",
            "message": "Tenets directory exists but no project tenets found",
            "count": 0,
            "needs_review": False
        }
    
    # Check age of tenets
    oldest_modification = None
    newest_modification = None
    
    for tenet in project_tenets:
        try:
            mtime = tenet.stat().st_mtime
            if oldest_modification is None or mtime < oldest_modification:
                oldest_modification = mtime
            if newest_modification is None or mtime > newest_modification:
                newest_modification = mtime
        except OSError:
            continue
    
    # Calculate days since last modification
    days_since_modification = None
    needs_review = False
    if newest_modification:
        days_since_modification = (datetime.now().timestamp() - newest_modification) / (60 * 60 * 24)
        needs_review = days_since_modification > review_period_days
    
    return {
        "status": "exists",
        "count": len(project_tenets),
        "oldest_modification": oldest_modification,
        "newest_modification": newest_modification,
        "days_since_modification": days_since_modification,
        "needs_review": needs_review,
        "review_period_days": review_period_days,
        "files": [str(f.relative_to(tenets_dir)) for f in project_tenets]
    }


def run_validation() -> Dict[str, Any]:
    """Run VibeSafe structure validation and return summary.
    
    Returns:
        dict: Validation results with keys:
            - error_count: Number of validation errors
            - warning_count: Number of validation warnings
            - has_issues: True if errors or warnings found
            - exit_code: Validator exit code
            - error: Error message if validation failed to run
    """
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    validator_path = os.path.join(script_dir, 'validate_vibesafe_structure.py')
    
    # Check if validator exists
    if not os.path.exists(validator_path):
        return {'error': 'Validator script not found'}
    
    try:
        # Run validator with no-color flag
        result = subprocess.run(
            [sys.executable, validator_path, '--no-color'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout + result.stderr
        
        # Parse output for error and warning counts
        error_match = re.search(r'ERRORS \((\d+)\)', output)
        warning_match = re.search(r'WARNINGS \((\d+)\)', output)
        
        error_count = int(error_match.group(1)) if error_match else 0
        warning_count = int(warning_match.group(1)) if warning_match else 0
        
        return {
            'error_count': error_count,
            'warning_count': warning_count,
            'has_issues': error_count > 0 or warning_count > 0,
            'exit_code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'error': 'Validation timed out'}
    except Exception as e:
        return {'error': str(e)}


def generate_next_steps(git_info: Dict[str, Any], cips_info: Dict[str, Any], 
                         backlog_info: Dict[str, Any], requirements_info: Dict[str, Any],
                         tenet_info: Dict[str, Any] = None,
                         validation_info: Dict[str, Any] = None,
                         gaps_info: Dict[str, Any] = None) -> List[str]:
    """Generate suggested next steps based on the project state."""
    next_steps = []
    
    # Add validation issues as highest priority if present
    if validation_info and not validation_info.get('error'):
        if validation_info.get('error_count', 0) > 0:
            next_steps.append(
                f"{Colors.RED}Fix {validation_info['error_count']} validation error(s):{Colors.ENDC} "
                f"./scripts/validate_vibesafe_structure.py --fix --fix-links"
            )
        elif validation_info.get('warning_count', 0) > 0:
            next_steps.append(
                f"{Colors.YELLOW}Address {validation_info['warning_count']} validation warning(s):{Colors.ENDC} "
                f"./scripts/validate_vibesafe_structure.py"
            )
    
    # Add gap detection and AI-assisted prompts
    if gaps_info and gaps_info.get('prompts'):
        for prompt_info in gaps_info['prompts']:
            # Format the prompt nicely
            title = prompt_info['title']
            prompt_text = prompt_info['prompt']
            
            # Add title
            next_steps.append(f"\n{Colors.BLUE}{title}{Colors.ENDC}")
            
            # Add prompt with indentation
            prompt_lines = prompt_text.strip().split('\n')
            next_steps.append(f"\n{Colors.YELLOW}   AI Prompt:{Colors.ENDC}")
            for line in prompt_lines[:10]:  # Show first 10 lines
                next_steps.append(f"   {line}")
            if len(prompt_lines) > 10:
                next_steps.append(f"   ... ({len(prompt_lines) - 10} more lines)")
            next_steps.append("")  # Empty line for spacing
    
    # Add suggestion to create/review tenets if needed (legacy, now handled by gaps)
    if tenet_info and not gaps_info:
        if tenet_info.get('status') == 'missing':
            next_steps.append("Create tenets directory and define your project's guiding principles")
        elif tenet_info.get('status') == 'empty':
            next_steps.append("Create your first project tenet to document guiding principles")
        elif tenet_info.get('needs_review'):
            next_steps.append("Review and update project tenets to reflect current practices")
    
    # Add suggestion to create requirements framework if missing
    if not requirements_info['has_framework']:
        next_steps.append(
            "Create requirements directory: mkdir -p requirements"
        )
    # Check if there are actual requirement files (not just templates/README)
    elif not gaps.get('has_requirements', False):
        next_steps.append(
            "Create first requirement (WHAT): Define what needs to be built before planning how (CIP)"
        )
    
    # Add suggestion to use requirements for backlog tasks
    if requirements_info['has_framework'] and backlog_info['by_status']['proposed']:
        next_steps.append(
            "Review requirements to refine proposed backlog tasks"
        )
    
    # Check for missing frontmatter
    if cips_info and cips_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(cips_info['without_frontmatter'])} CIP files")
    
    if backlog_info and backlog_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(backlog_info['without_frontmatter'])} backlog items")
    
    # Requirements process recommendations
    if requirements_info['has_framework']:
        # Check for in-progress backlog items related to requirements
        requirements_related_items = []
        if backlog_info and backlog_info.get('by_status') and backlog_info['by_status'].get('in_progress'):
            for item in backlog_info['by_status']['in_progress']:
                title = item.get('title', '').lower()
                if any(keyword in title for keyword in ['requirement', 'goal decomposition', 'stakeholder']):
                    requirements_related_items.append(item)
                    
        # If requirements-related items are in progress
        if requirements_related_items:
            next_steps.append(f"Continue implementation of requirements-related item: {requirements_related_items[0]['title']}")
            next_steps.append("Verify requirements-related implementation against acceptance criteria")
            
        # Suggest requirements process for new features
        # Check if there are proposed CIPs that might need requirements gathering
        proposed_cips_needing_requirements = []
        if cips_info and cips_info.get('by_status') and cips_info['by_status'].get('proposed'):
            for cip in cips_info['by_status']['proposed']:
                # This is a simple heuristic - in a real implementation you might want to check
                # if the CIP already has associated requirements documents
                proposed_cips_needing_requirements.append(cip)
        
        if proposed_cips_needing_requirements:
            cip = proposed_cips_needing_requirements[0]
            next_steps.append(f"Start requirements gathering for proposed CIP: {cip['id']} - {cip['title']}")
            next_steps.append("Document requirements (WHAT) before implementation (HOW)")
            
        # Remind about checking for requirements drift for implemented CIPs
        implemented_cips = []
        if cips_info and cips_info.get('by_status') and cips_info['by_status'].get('implemented'):
            implemented_cips = cips_info['by_status']['implemented']
            
        if implemented_cips:
            cip = implemented_cips[0]
            next_steps.append(f"Verify implementation of {cip['id']} against original requirements")
            next_steps.append("Check for requirements drift - ensure code aligns with specified requirements")
    else:
        # If requirements framework doesn't exist, suggest setting it up
        next_steps.append("Set up requirements framework to improve requirements gathering")
    
    # Check for accepted CIPs that need implementation
    if cips_info and cips_info.get('by_status') and cips_info['by_status'].get('accepted'):
        next_steps.append(f"Implement accepted CIP: {cips_info['by_status']['accepted'][0]['id']} - {cips_info['by_status']['accepted'][0]['title']}")
        # Add requirements reminder for implementation
        next_steps.append("Start implementation by reviewing requirements")
    
    # Check for in-progress backlog items
    if backlog_info and backlog_info.get('by_status') and backlog_info['by_status'].get('in_progress'):
        next_steps.append(f"Continue work on in-progress backlog item: {backlog_info['by_status']['in_progress'][0]['title']}")
    
    # Check for high priority backlog items
    if backlog_info and backlog_info.get('by_priority') and backlog_info['by_priority'].get('high'):
        for item in backlog_info['by_priority']['high'][:2]:  # Top 2 high priority items
            if not any(item['title'] in step for step in next_steps):  # Avoid duplicates
                next_steps.append(f"Address high priority backlog item: {item['title']}")
    
    # Check Git status for uncommitted changes
    if git_info and (git_info.get('modified_files') or git_info.get('untracked_files')):
        total_changes = len(git_info.get('modified_files', [])) + len(git_info.get('untracked_files', []))
        next_steps.append(f"Commit {total_changes} pending changes to Git repository")
    
    # If no specific tasks, suggest requirements-related activities
    if not next_steps:
        next_steps.append("Review and update project roadmap")
        next_steps.append("Consider creating new CIPs for upcoming features")
        if requirements_info['has_framework']:
            # Suggest using specific patterns
            if any('goal-decomposition' in pattern for pattern in requirements_info['patterns']):
                next_steps.append("Use the Goal Decomposition Pattern to break down high-level goals into specific requirements")
            if any('stakeholder-identification' in pattern for pattern in requirements_info['patterns']):
                next_steps.append("Use the Stakeholder Identification Pattern to identify all stakeholders for upcoming features")
    
    return next_steps

def run_update_scripts() -> List[str]:
    """Run all update scripts to ensure registries are up to date."""
    update_scripts = [
        'backlog/update_index.py',
        'cip/update_index.py',
        'tenets/update_index.py',
        'requirements/update_index.py'
    ]
    
    results = []
    for script in update_scripts:
        if os.path.exists(script):
            try:
                output, exit_code = run_command(['python3', script])
                if exit_code == 0:
                    results.append(f"✓ Updated {script}")
                else:
                    results.append(f"✗ Failed to update {script}: {output}")
            except Exception as e:
                results.append(f"✗ Error running {script}: {str(e)}")
    
    return results

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="What's Next for VibeSafe projects")
    parser.add_argument('--no-git', action='store_true', help='Skip Git information')
    parser.add_argument('--no-color', action='store_true', help='Disable colorized output')
    parser.add_argument('--cip-only', action='store_true', help='Only show CIP information')
    parser.add_argument('--backlog-only', action='store_true', help='Only show backlog information')
    parser.add_argument('--requirements-only', action='store_true', help='Only show requirements information')
    parser.add_argument('--no-update', action='store_true', help='Skip running update scripts')
    parser.add_argument('--skip-validation', action='store_true', help='Skip VibeSafe structure validation')
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()

    # Run update scripts first if not disabled
    if not args.no_update:
        print_section("Updating Registries")
        update_results = run_update_scripts()
        for result in update_results:
            print(result)
        print()  # Add a blank line for spacing
    
    # Get Git info if requested
    git_info = {}
    if not args.no_git:
        git_info = get_git_status()
        
        if git_info.get('current_branch'):
            print(f"{Colors.BOLD}Current Branch:{Colors.ENDC} {git_info['current_branch']}")
            print("")
        
        if git_info.get('recent_commits'):
            print(f"{Colors.BOLD}Recent Commits:{Colors.ENDC}")
            for commit in git_info['recent_commits']:
                print(f"  {Colors.YELLOW}{commit['hash']}{Colors.ENDC} {commit['message']}")
            print("")
    
    # Get CIP info if not backlog-only
    cips_info = {}
    if not args.backlog_only and not args.requirements_only:
        cips_info = scan_cips()
        
        print(f"{Colors.BOLD}CIPs:{Colors.ENDC}")
        print(f"  Total: {cips_info['total']}")
        
        if cips_info['by_status']['proposed']:
            print(f"  {Colors.YELLOW}Proposed:{Colors.ENDC} {len(cips_info['by_status']['proposed'])}")
            for cip in cips_info['by_status']['proposed']:
                title = cip.get('title', 'Untitled')
                if cip.get('no_frontmatter'):
                    title += f" {Colors.RED}(No frontmatter){Colors.ENDC}"
                print(f"    - {cip['id']}: {title}")
        
        if cips_info['by_status']['accepted']:
            print(f"  {Colors.BLUE}Accepted:{Colors.ENDC} {len(cips_info['by_status']['accepted'])}")
            for cip in cips_info['by_status']['accepted']:
                print(f"    - {cip['id']}: {cip.get('title', 'Untitled')}")
        
        if cips_info['by_status']['implemented']:
            print(f"  {Colors.GREEN}Implemented:{Colors.ENDC} {len(cips_info['by_status']['implemented'])}")
        
        if cips_info['by_status']['closed']:
            print(f"  Closed: {len(cips_info['by_status']['closed'])}")
        
        if cips_info['without_frontmatter']:
            print(f"  {Colors.RED}Missing Frontmatter:{Colors.ENDC} {len(cips_info['without_frontmatter'])}")
            for cip in cips_info['without_frontmatter']:
                print(f"    - {cip['id']}: {cip.get('title', 'Untitled')}")
        
        print("")
    
    # Get backlog info if not cip-only
    backlog_info = {}
    if not args.cip_only and not args.requirements_only:
        backlog_info = scan_backlog()
        
        print(f"{Colors.BOLD}Backlog:{Colors.ENDC}")
        print(f"  Total: {backlog_info['total']}")
        
        if backlog_info['by_status']['in_progress']:
            print(f"  {Colors.BLUE}In Progress:{Colors.ENDC} {len(backlog_info['by_status']['in_progress'])}")
            for task in backlog_info['by_status']['in_progress']:
                print(f"    - {task['title']} ({task['id']})")
        
        if backlog_info['by_status']['ready']:
            print(f"  {Colors.GREEN}Ready:{Colors.ENDC} {len(backlog_info['by_status']['ready'])}")
            for task in backlog_info['by_status']['ready']:
                print(f"    - {task['title']} ({task['id']})")
        
        if backlog_info['by_status']['proposed']:
            print(f"  {Colors.YELLOW}Proposed:{Colors.ENDC} {len(backlog_info['by_status']['proposed'])}")
            for task in backlog_info['by_status']['proposed']:
                print(f"    - {task['title']} ({task['id']})")
        
        if backlog_info['by_priority']['high']:
            print(f"  {Colors.RED}High Priority:{Colors.ENDC} {len(backlog_info['by_priority']['high'])}")
            for task in backlog_info['by_priority']['high']:
                print(f"    - {task['title']} ({task['id']})")
        
        print("")
    
    # Get requirements info if not cip-only or backlog-only, or if requirements-only
    requirements_info = {}
    if not args.cip_only and not args.backlog_only or args.requirements_only:
        requirements_info = scan_requirements()
        
        print(f"{Colors.BOLD}Requirements Framework:{Colors.ENDC}")
        if requirements_info['has_framework']:
            print(f"  Framework installed: {Colors.GREEN}Yes{Colors.ENDC}")
            
            if requirements_info['patterns']:
                print(f"  Patterns: {len(requirements_info['patterns'])}")
                for pattern in requirements_info['patterns']:
                    print(f"    - {pattern}")
            else:
                print(f"  Patterns: {Colors.YELLOW}None defined{Colors.ENDC}")
            
            prompt_count = sum(len(prompts) for prompts in requirements_info['prompts'].values())
            if prompt_count > 0:
                print(f"  Prompts: {prompt_count}")
                for prompt_type, prompts in requirements_info['prompts'].items():
                    if prompts:
                        print(f"    - {prompt_type.capitalize()}: {len(prompts)}")
            else:
                print(f"  Prompts: {Colors.YELLOW}None defined{Colors.ENDC}")
            
            if requirements_info['integrations']:
                print(f"  Integrations: {len(requirements_info['integrations'])}")
                for integration in requirements_info['integrations']:
                    print(f"    - {integration}")
            else:
                print(f"  Integrations: {Colors.YELLOW}None defined{Colors.ENDC}")
        else:
            print(f"  Framework installed: {Colors.RED}No{Colors.ENDC}")
        
        print("")
    
    # Check tenet status
    tenet_info = check_tenet_status()
    
    # Run validation if not skipped
    validation_info = {}
    if not args.skip_validation:
        validation_info = run_validation()
    
    # Detect gaps and generate AI prompts
    gaps = detect_gaps()
    ai_prompts = generate_ai_prompts(gaps)
    gaps_info = {
        'gaps': gaps,
        'prompts': ai_prompts
    }
    
    # Generate next steps
    if args.cip_only:
        next_steps = generate_next_steps(git_info, cips_info, {}, {}, tenet_info, validation_info, gaps_info)
    elif args.backlog_only:
        next_steps = generate_next_steps(git_info, {}, backlog_info, {}, tenet_info, validation_info, gaps_info)
    elif args.requirements_only:
        next_steps = generate_next_steps(git_info, {'by_status': {'proposed': []}}, {'by_status': {'proposed': []}, 'by_priority': {'high': []}}, requirements_info, tenet_info, validation_info, gaps_info)
    else:
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, validation_info, gaps_info)
    
    if next_steps:
        print_section("Suggested Next Steps")
        for i, step in enumerate(next_steps, 1):
            print(f"{i}. {step}")
    
    # Output files needing frontmatter
    if not args.requirements_only and (cips_info.get('without_frontmatter') or backlog_info.get('without_frontmatter')):
        print_section("Files Needing YAML Frontmatter")
        
        if cips_info.get('without_frontmatter'):
            print(f"{Colors.BOLD}CIPs Needing Frontmatter:{Colors.ENDC}")
            for cip in cips_info['without_frontmatter']:
                print(f"  {Colors.YELLOW}{cip['path']}{Colors.ENDC}")
        
        if backlog_info.get('without_frontmatter'):
            print(f"{Colors.BOLD}Backlog Items Needing Frontmatter:{Colors.ENDC}")
            for item in backlog_info['without_frontmatter']:
                print(f"  {Colors.YELLOW}{item['path']}{Colors.ENDC}")
    
    if not args.requirements_only:
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation canceled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error:{Colors.ENDC} {str(e)}")
        sys.exit(1) 