#!/usr/bin/env python3
"""
What's Next Script for VibeSafe

This script summarizes the current project status and identifies pending tasks,
helping LLMs quickly understand project context and prioritize future work.

Usage:
  python whats_next.py [--no-git] [--no-color] [--cip-only] [--backlog-only]
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
        """Disable all colors."""
        cls.HEADER = ''
        cls.BLUE = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.ENDC = ''
        cls.BOLD = ''
        cls.UNDERLINE = ''

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def run_command(command: List[str]) -> Tuple[str, int]:
    """Run a shell command and return its output and exit code."""
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
    """Get Git repository status information."""
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
    """Extract YAML frontmatter from a markdown file if it exists."""
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
    """Check if a file has all the expected frontmatter keys."""
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return False
    
    for key in expected_keys:
        if key not in frontmatter:
            return False
    
    return True

def scan_cips() -> Dict[str, Any]:
    """Scan all CIP files and collect their status."""
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
            'abandoned': []
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
                status = frontmatter.get('status', 'unknown').lower()
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
                status = status_match.group(1).lower() if status_match else "unknown"
                
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
    """Scan the AI-Requirements directory for requirement artifacts."""
    requirements_info = {
        'exists': os.path.exists('ai-requirements'),
        'patterns': [],
        'examples': [],
        'prompts': [],
        'integrations': []
    }
    
    if not requirements_info['exists']:
        return requirements_info
    
    # Scan patterns
    if os.path.exists('ai-requirements/patterns'):
        for pattern_file in glob.glob('ai-requirements/patterns/*.md'):
            pattern_name = os.path.basename(pattern_file).replace('.md', '')
            requirements_info['patterns'].append({
                'name': pattern_name,
                'path': pattern_file
            })
    
    # Scan examples
    if os.path.exists('ai-requirements/examples'):
        for example_file in glob.glob('ai-requirements/examples/*.md'):
            example_name = os.path.basename(example_file).replace('.md', '')
            requirements_info['examples'].append({
                'name': example_name,
                'path': example_file
            })
    
    # Scan prompts
    if os.path.exists('ai-requirements/prompts'):
        for prompt_dir in glob.glob('ai-requirements/prompts/*'):
            if os.path.isdir(prompt_dir):
                prompt_name = os.path.basename(prompt_dir)
                requirements_info['prompts'].append({
                    'name': prompt_name,
                    'path': prompt_dir
                })
    
    # Scan integrations
    if os.path.exists('ai-requirements/integrations'):
        for integration_file in glob.glob('ai-requirements/integrations/*.md'):
            integration_name = os.path.basename(integration_file).replace('.md', '')
            requirements_info['integrations'].append({
                'name': integration_name,
                'path': integration_file
            })
    
    return requirements_info

def generate_next_steps(git_info: Dict[str, Any], cips_info: Dict[str, Any], backlog_info: Dict[str, Any]) -> List[str]:
    """Generate a list of recommended next steps based on project status."""
    next_steps = []
    
    # Check if the requirements framework exists
    requirements_info = scan_requirements()
    
    # Check for missing frontmatter
    if cips_info and cips_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(cips_info['without_frontmatter'])} CIP files")
    
    if backlog_info and backlog_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(backlog_info['without_frontmatter'])} backlog items")
    
    # Requirements process recommendations
    if requirements_info['exists']:
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
        if requirements_info['exists']:
            # Suggest using specific patterns
            if any('goal-decomposition' in pattern['name'] for pattern in requirements_info['patterns']):
                next_steps.append("Use the Goal Decomposition Pattern to break down high-level goals into specific requirements")
            if any('stakeholder-identification' in pattern['name'] for pattern in requirements_info['patterns']):
                next_steps.append("Use the Stakeholder Identification Pattern to identify all stakeholders for upcoming features")
    
    return next_steps

def main():
    """Main function to run the 'what's next' script."""
    parser = argparse.ArgumentParser(description='Show what to work on next in the VibeSafe project.')
    parser.add_argument('--no-git', action='store_true', help='Skip Git repository information')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--cip-only', action='store_true', help='Only show CIP information')
    parser.add_argument('--backlog-only', action='store_true', help='Only show backlog information')
    parser.add_argument('--requirements-only', action='store_true', help='Only show requirements information')
    parser.add_argument('--quiet', action='store_true', help='Only show next steps, no detailed status')
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        Colors.disable()
    
    # Print header
    if not args.quiet:
        print(f"\n{Colors.BOLD}VibeSafe Project Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
    
    # Get Git information if not using --no-git
    git_info = {}
    if not args.no_git and not args.requirements_only:
        if not args.quiet:
            print_section("Git Repository Status")
        git_info = get_git_status()
        
        if not args.quiet:
            if git_info.get('current_branch'):
                print(f"{Colors.BOLD}Current Branch:{Colors.ENDC} {git_info['current_branch']}")
            
            if git_info.get('recent_commits'):
                print(f"\n{Colors.BOLD}Recent Commits:{Colors.ENDC}")
                for commit in git_info['recent_commits']:
                    print(f"  {Colors.YELLOW}{commit['hash']}{Colors.ENDC} {commit['message']}")
            
            if git_info.get('modified_files'):
                print(f"\n{Colors.BOLD}Modified Files:{Colors.ENDC}")
                for file in git_info['modified_files']:
                    print(f"  {Colors.RED}{file['status']}{Colors.ENDC} {file['path']}")
            
            if git_info.get('untracked_files'):
                print(f"\n{Colors.BOLD}Untracked Files:{Colors.ENDC}")
                for file in git_info['untracked_files']:
                    print(f"  {Colors.RED}??{Colors.ENDC} {file}")
    
    # Scan CIPs if not backlog-only and not requirements-only
    cips_info = {}
    if not args.backlog_only and not args.requirements_only:
        if not args.quiet:
            print_section("CIP Status")
        cips_info = scan_cips()
        
        if not args.quiet:
            print(f"{Colors.BOLD}Total CIPs:{Colors.ENDC} {cips_info['total']}")
            print(f"{Colors.BOLD}CIPs with Frontmatter:{Colors.ENDC} {cips_info['with_frontmatter']}")
            print(f"{Colors.BOLD}CIPs without Frontmatter:{Colors.ENDC} {len(cips_info['without_frontmatter'])}")
            
            if cips_info['by_status']['proposed']:
                print(f"\n{Colors.BOLD}Proposed CIPs:{Colors.ENDC}")
                for cip in cips_info['by_status']['proposed']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if cip.get('no_frontmatter') else ""
                    print(f"  {Colors.BLUE}{cip['id']}{Colors.ENDC}: {cip['title']}{frontmatter_indicator}")
            
            if cips_info['by_status']['accepted']:
                print(f"\n{Colors.BOLD}Accepted CIPs:{Colors.ENDC}")
                for cip in cips_info['by_status']['accepted']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if cip.get('no_frontmatter') else ""
                    print(f"  {Colors.YELLOW}{cip['id']}{Colors.ENDC}: {cip['title']}{frontmatter_indicator}")
            
            if cips_info['by_status']['implemented']:
                print(f"\n{Colors.BOLD}Implemented CIPs:{Colors.ENDC}")
                for cip in cips_info['by_status']['implemented']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if cip.get('no_frontmatter') else ""
                    print(f"  {Colors.GREEN}{cip['id']}{Colors.ENDC}: {cip['title']}{frontmatter_indicator}")
            
            if cips_info['by_status']['closed']:
                print(f"\n{Colors.BOLD}Closed CIPs:{Colors.ENDC}")
                for cip in cips_info['by_status']['closed']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if cip.get('no_frontmatter') else ""
                    print(f"  {Colors.GREEN}{cip['id']}{Colors.ENDC}: {cip['title']}{frontmatter_indicator}")
    
    # Scan Backlog if not cip-only and not requirements-only
    backlog_info = {}
    if not args.cip_only and not args.requirements_only:
        if not args.quiet:
            print_section("Backlog Status")
        backlog_info = scan_backlog()
        
        if not args.quiet:
            print(f"{Colors.BOLD}Total Backlog Items:{Colors.ENDC} {backlog_info['total']}")
            print(f"{Colors.BOLD}Items with Frontmatter:{Colors.ENDC} {backlog_info['with_frontmatter']}")
            print(f"{Colors.BOLD}Items without Frontmatter:{Colors.ENDC} {len(backlog_info['without_frontmatter'])}")
            
            if backlog_info['by_priority']['high']:
                print(f"\n{Colors.BOLD}High Priority Items:{Colors.ENDC}")
                for item in backlog_info['by_priority']['high']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if item.get('no_frontmatter') else ""
                    print(f"  {Colors.RED}[HIGH]{Colors.ENDC} {item['title']}{frontmatter_indicator}")
            
            if backlog_info['by_status']['in_progress']:
                print(f"\n{Colors.BOLD}In Progress Items:{Colors.ENDC}")
                for item in backlog_info['by_status']['in_progress']:
                    frontmatter_indicator = f" {Colors.RED}(No Frontmatter){Colors.ENDC}" if item.get('no_frontmatter') else ""
                    print(f"  {Colors.YELLOW}[IN PROGRESS]{Colors.ENDC} {item['title']}{frontmatter_indicator}")
    
    # Print requirements info
    requirements_info = scan_requirements()
    if not args.quiet and (not args.cip_only and not args.backlog_only or args.requirements_only):
        if requirements_info['exists']:
            print_section("AI-Requirements Framework")
            print(f"{Colors.BOLD}Available Patterns:{Colors.ENDC}")
            if requirements_info['patterns']:
                for pattern in requirements_info['patterns']:
                    print(f"  - {pattern['name']}")
            else:
                print("  None found")
                
            print(f"\n{Colors.BOLD}Available Examples:{Colors.ENDC}")
            if requirements_info['examples']:
                for example in requirements_info['examples']:
                    print(f"  - {example['name']}")
            else:
                print("  None found")
                
            print(f"\n{Colors.BOLD}Available Prompts:{Colors.ENDC}")
            if requirements_info['prompts']:
                for prompt in requirements_info['prompts']:
                    print(f"  - {prompt['name']}")
            else:
                print("  None found")
                
            print(f"\n{Colors.BOLD}Available Integrations:{Colors.ENDC}")
            if requirements_info['integrations']:
                for integration in requirements_info['integrations']:
                    print(f"  - {integration['name']}")
            else:
                print("  None found")
        else:
            print(f"\n{Colors.YELLOW}AI-Requirements Framework not found in this project.{Colors.ENDC}")
            print("Consider implementing it to improve requirements gathering for new features.")
    
    # Generate next steps
    if not args.quiet:
        print_section("Recommended Next Steps")
    
    next_steps = generate_next_steps(git_info, cips_info, backlog_info)
    
    # Filter next steps based on command line options
    if args.cip_only:
        next_steps = [step for step in next_steps if "CIP" in step]
    elif args.backlog_only:
        next_steps = [step for step in next_steps if "backlog" in step.lower() or "high priority" in step.lower()]
    elif args.requirements_only:
        next_steps = [step for step in next_steps if any(term in step.lower() for term in 
                                        ["requirements", "goal decomposition", "stakeholder", "drift", "acceptance criteria"])]
    
    for i, step in enumerate(next_steps, 1):
        print(f"{Colors.BOLD}{i}.{Colors.ENDC} {step}")
    
    # Output files needing frontmatter
    if not args.quiet and not args.requirements_only and (cips_info.get('without_frontmatter') or backlog_info.get('without_frontmatter')):
        print_section("Files Needing YAML Frontmatter")
        
        if cips_info.get('without_frontmatter'):
            print(f"{Colors.BOLD}CIPs Needing Frontmatter:{Colors.ENDC}")
            for cip in cips_info['without_frontmatter']:
                print(f"  {Colors.YELLOW}{cip['path']}{Colors.ENDC}")
        
        if backlog_info.get('without_frontmatter'):
            print(f"{Colors.BOLD}Backlog Items Needing Frontmatter:{Colors.ENDC}")
            for item in backlog_info['without_frontmatter']:
                print(f"  {Colors.YELLOW}{item['path']}{Colors.ENDC}")
    
    if not args.quiet:
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