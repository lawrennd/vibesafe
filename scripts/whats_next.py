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

def generate_next_steps(git_info: Dict[str, Any], cips_info: Dict[str, Any], backlog_info: Dict[str, Any]) -> List[str]:
    """Generate a list of recommended next steps based on project status."""
    next_steps = []
    
    # Check for missing frontmatter
    if cips_info and cips_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(cips_info['without_frontmatter'])} CIP files")
    
    if backlog_info and backlog_info.get('without_frontmatter'):
        next_steps.append(f"Add YAML frontmatter to {len(backlog_info['without_frontmatter'])} backlog items")
    
    # Check for accepted CIPs that need implementation
    if cips_info and cips_info.get('by_status') and cips_info['by_status'].get('accepted'):
        next_steps.append(f"Implement accepted CIP: {cips_info['by_status']['accepted'][0]['id']} - {cips_info['by_status']['accepted'][0]['title']}")
    
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
    
    # If no specific tasks, suggest reviewing project status
    if not next_steps:
        next_steps.append("Review and update project roadmap")
        next_steps.append("Consider creating new CIPs for upcoming features")
    
    return next_steps

def main():
    """Main function to run the 'what's next' script."""
    parser = argparse.ArgumentParser(description='Summarize the current project status and identify next steps.')
    parser.add_argument('--no-git', action='store_true', help='Skip Git status information')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--cip-only', action='store_true', help='Only show CIP information')
    parser.add_argument('--backlog-only', action='store_true', help='Only show backlog information')
    parser.add_argument('--quiet', action='store_true', help='Suppress all output except next steps')
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    if not args.quiet:
        print_section("VibeSafe Project Status")
        print(f"{Colors.BOLD}Run Date:{Colors.ENDC} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get Git status if requested
    git_info = {}
    if not args.no_git:
        if not args.quiet:
            print_section("Git Status")
        git_info = get_git_status()
        
        if not args.quiet:
            print(f"{Colors.BOLD}Current Branch:{Colors.ENDC} {git_info['current_branch']}")
            print(f"\n{Colors.BOLD}Recent Commits:{Colors.ENDC}")
            for commit in git_info['recent_commits']:
                print(f"  {Colors.YELLOW}{commit['hash']}{Colors.ENDC} {commit['message']}")
            
            if git_info['modified_files']:
                print(f"\n{Colors.BOLD}Modified Files:{Colors.ENDC}")
                for file in git_info['modified_files']:
                    print(f"  {Colors.RED}{file['status']}{Colors.ENDC} {file['path']}")
            
            if git_info['untracked_files']:
                print(f"\n{Colors.BOLD}Untracked Files:{Colors.ENDC}")
                for file in git_info['untracked_files']:
                    print(f"  {Colors.RED}??{Colors.ENDC} {file}")
    
    # Scan CIPs if not backlog-only
    cips_info = {}
    if not args.backlog_only:
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
                    print(f"  {Colors.GREEN}{cip['id']}{Colors.ENDC}: {cip['title']}{frontmatter_indicator}")
    
    # Scan Backlog if not cip-only
    backlog_info = {}
    if not args.cip_only:
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
    
    # Generate next steps
    if not args.quiet:
        print_section("Recommended Next Steps")
    
    next_steps = generate_next_steps(git_info, cips_info, backlog_info)
    
    for i, step in enumerate(next_steps, 1):
        print(f"{Colors.BOLD}{i}.{Colors.ENDC} {step}")
    
    # Output files needing frontmatter
    if not args.quiet and (cips_info.get('without_frontmatter') or backlog_info.get('without_frontmatter')):
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