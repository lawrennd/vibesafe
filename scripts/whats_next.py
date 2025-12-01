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
    """Scan the AI-Requirements directory and collect information."""
    requirements_info = {
        'has_framework': os.path.isdir('ai-requirements'),
        'has_template': os.path.exists('ai-requirements/requirement_template.md'),
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
    
    # Check if the AI-Requirements framework is present
    if not requirements_info['has_framework']:
        return requirements_info
    
    # Scan patterns
    if os.path.isdir('ai-requirements/patterns'):
        pattern_files = glob.glob('ai-requirements/patterns/*.md')
        requirements_info['patterns'] = [os.path.basename(f).replace('.md', '') for f in pattern_files]
    
    # Scan prompts
    for prompt_type in ['discovery', 'refinement', 'validation', 'testing']:
        prompt_dir = f'ai-requirements/prompts/{prompt_type}'
        if os.path.isdir(prompt_dir):
            prompt_files = glob.glob(f'{prompt_dir}/*.md')
            requirements_info['prompts'][prompt_type] = [os.path.basename(f) for f in prompt_files]
    
    # Scan integrations
    if os.path.isdir('ai-requirements/integrations'):
        integration_files = glob.glob('ai-requirements/integrations/*.md')
        requirements_info['integrations'] = [os.path.basename(f).replace('.md', '') for f in integration_files]
    
    # Scan examples
    if os.path.isdir('ai-requirements/examples'):
        example_files = glob.glob('ai-requirements/examples/*.md')
        requirements_info['examples'] = [os.path.basename(f) for f in example_files]
    
    # Scan guidance
    if os.path.isdir('ai-requirements/guidance'):
        guidance_files = glob.glob('ai-requirements/guidance/*.md')
        requirements_info['guidance'] = [os.path.basename(f) for f in guidance_files]
    
    return requirements_info

def generate_next_steps(git_info: Dict[str, Any], cips_info: Dict[str, Any], 
                         backlog_info: Dict[str, Any], requirements_info: Dict[str, Any]) -> List[str]:
    """Generate suggested next steps based on the project state."""
    next_steps = []
    
    # Add suggestion to create AI-Requirements framework if missing
    if not requirements_info['has_framework']:
        next_steps.append(
            "Create AI-Requirements framework directory structure: "
            "mkdir -p ai-requirements/{patterns,prompts/{discovery,refinement,validation,testing},integrations,examples,guidance}"
        )
    # Check if requirement template exists
    elif not requirements_info.get('has_template'):
        next_steps.append(
            "Create requirements template: cp templates/ai-requirements/requirement_template.md ai-requirements/"
        )
    # Add suggestion if no patterns exist
    elif not requirements_info['patterns']:
        next_steps.append(
            "Create requirements patterns in ai-requirements/patterns/"
        )
    # Add suggestion if no prompts exist in any category
    elif all(not prompts for prompts in requirements_info['prompts'].values()):
        next_steps.append(
            "Create requirements prompts in ai-requirements/prompts/"
        )
    
    # Add suggestion to use requirements for backlog tasks
    if requirements_info['has_framework'] and backlog_info['by_status']['proposed']:
        next_steps.append(
            "Use AI-Requirements patterns to refine proposed backlog tasks"
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
            next_steps.append("Use AI-Requirements framework prompts and patterns for structured requirements discovery")
            
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
        next_steps.append("Set up AI-Requirements framework to improve requirements gathering")
    
    # Check for accepted CIPs that need implementation
    if cips_info and cips_info.get('by_status') and cips_info['by_status'].get('accepted'):
        next_steps.append(f"Implement accepted CIP: {cips_info['by_status']['accepted'][0]['id']} - {cips_info['by_status']['accepted'][0]['title']}")
        # Add requirements reminder for implementation
        next_steps.append("Start implementation by reviewing requirements from the AI-Requirements framework")
    
    # Check for in-progress backlog items
    if backlog_info and backlog_info.get('by_status') and backlog_info['by_status'].get('in_progress'):
        next_steps.append(f"Continue work on in-progress backlog item: {backlog_info['by_status']['in_progress'][0]['title']}")
    
    # Check for high priority backlog items (excluding completed)
    if backlog_info and backlog_info.get('by_priority') and backlog_info['by_priority'].get('high'):
        # Filter out completed items
        completed_ids = {task['id'] for task in backlog_info.get('by_status', {}).get('completed', [])}
        high_priority_active = [
            item for item in backlog_info['by_priority']['high']
            if item['id'] not in completed_ids
        ]
        for item in high_priority_active[:2]:  # Top 2 active high priority items
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
        'ai-requirements/update_index.py'
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
            # Filter out completed items from high priority display
            completed_ids = {task['id'] for task in backlog_info['by_status']['completed']}
            high_priority_active = [
                task for task in backlog_info['by_priority']['high']
                if task['id'] not in completed_ids
            ]
            if high_priority_active:
                print(f"  {Colors.RED}High Priority:{Colors.ENDC} {len(high_priority_active)}")
                for task in high_priority_active:
                    print(f"    - {task['title']} ({task['id']})")
        
        print("")
    
    # Get requirements info if not cip-only or backlog-only, or if requirements-only
    requirements_info = {}
    if not args.cip_only and not args.backlog_only or args.requirements_only:
        requirements_info = scan_requirements()
        
        print(f"{Colors.BOLD}AI-Requirements Framework:{Colors.ENDC}")
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
    
    # Generate next steps
    # Ensure requirements_info has minimal structure for next_steps generation
    if not requirements_info:
        requirements_info = {'has_framework': False}
    
    if args.cip_only:
        next_steps = generate_next_steps(git_info, cips_info, {}, requirements_info)
    elif args.backlog_only:
        next_steps = generate_next_steps(git_info, {}, backlog_info, requirements_info)
    elif args.requirements_only:
        next_steps = generate_next_steps(git_info, {'by_status': {'proposed': []}}, {'by_status': {'proposed': []}, 'by_priority': {'high': []}}, requirements_info)
    else:
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
    
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