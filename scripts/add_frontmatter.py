#!/usr/bin/env python3
"""
Migration Script for Adding YAML Frontmatter

This script adds YAML frontmatter to existing CIP and backlog markdown files.
It extracts metadata from the existing files and creates properly formatted
frontmatter at the top of each file.
"""

import os
import re
import sys
import glob
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

def extract_cip_info(file_path: str) -> Dict[str, Any]:
    """Extract CIP information from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {}
    
    # Extract CIP ID and title
    title_match = re.search(r'# CIP-([0-9A-F]+):\s*(.*)', content)
    if title_match:
        info['id'] = title_match.group(1)
        info['title'] = title_match.group(1).strip()
    
    # Extract status
    status_section = re.search(r'## Status.*?(##|$)', content, re.DOTALL)
    if status_section:
        status_text = status_section.group(0)
        
        # Look for the checked status
        if re.search(r'- \[x\] Proposed', status_text, re.IGNORECASE):
            info['status'] = 'proposed'
        elif re.search(r'- \[x\] Accepted', status_text, re.IGNORECASE):
            info['status'] = 'accepted'
        elif re.search(r'- \[x\] Implemented', status_text, re.IGNORECASE):
            info['status'] = 'implemented'
        elif re.search(r'- \[x\] Closed', status_text, re.IGNORECASE):
            info['status'] = 'closed'
        else:
            info['status'] = 'proposed'  # Default to proposed
        
        # Extract the date if available
        date_match = re.search(r'- \[x\] \w+:\s*\[([0-9-]+)\]', status_text)
        if date_match:
            info['created'] = date_match.group(1)
    
    # Extract author
    author_match = re.search(r'## Author\s*\n([^\n#]+)', content)
    if author_match:
        info['author'] = author_match.group(1).strip()
    
    # Extract date
    date_match = re.search(r'## Date\s*\n([0-9-]+)', content)
    if date_match:
        if 'created' not in info:
            info['created'] = date_match.group(1).strip()
    
    # Set defaults for missing required fields
    if 'id' not in info:
        info['id'] = os.path.basename(file_path).replace('cip', '').replace('.md', '')
    
    if 'title' not in info:
        info['title'] = "Untitled CIP"
    
    if 'status' not in info:
        info['status'] = "proposed"
    
    if 'created' not in info:
        info['created'] = datetime.now().strftime('%Y-%m-%d')
    
    # Always set last_updated to today
    info['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    return info

def extract_backlog_info(file_path: str) -> Dict[str, Any]:
    """Extract backlog item information from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {}
    
    # Extract ID from filename
    filename = os.path.basename(file_path)
    if re.match(r'\d{4}-\d{2}-\d{2}', filename):
        info['id'] = filename.replace('.md', '')
    else:
        # Generate ID based on creation date and filename
        today = datetime.now().strftime('%Y-%m-%d')
        name_part = filename.replace('.md', '').lower()
        info['id'] = f"{today}_{name_part}"
    
    # Extract title
    title_match = re.search(r'# Task:\s*(.*)', content)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    # Extract metadata from the metadata section
    metadata_section = re.search(r'- \*\*ID\*\*.*?## Description', content, re.DOTALL)
    if metadata_section:
        metadata_text = metadata_section.group(0)
        
        # Extract status
        status_match = re.search(r'- \*\*Status\*\*:\s*(\w+)', metadata_text)
        if status_match:
            info['status'] = status_match.group(1).lower()
        
        # Extract priority
        priority_match = re.search(r'- \*\*Priority\*\*:\s*(\w+)', metadata_text)
        if priority_match:
            info['priority'] = priority_match.group(1).lower()
        
        # Extract created date
        created_match = re.search(r'- \*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})', metadata_text)
        if created_match:
            info['created'] = created_match.group(1)
        
        # Extract last updated date
        updated_match = re.search(r'- \*\*Last Updated\*\*:\s*(\d{4}-\d{2}-\d{2})', metadata_text)
        if updated_match:
            info['last_updated'] = updated_match.group(1)
        
        # Extract owner
        owner_match = re.search(r'- \*\*Owner\*\*:\s*([^\n]+)', metadata_text)
        if owner_match:
            owner = owner_match.group(1).strip()
            if owner and owner != '[Person responsible for the task]':
                info['owner'] = owner
        
        # Extract GitHub issue
        issue_match = re.search(r'- \*\*GitHub Issue\*\*:\s*(\d+)', metadata_text)
        if issue_match:
            info['github_issue'] = int(issue_match.group(1))
        
        # Extract dependencies
        dependencies_match = re.search(r'- \*\*Dependencies\*\*:\s*([^\n]+)', metadata_text)
        if dependencies_match:
            deps = dependencies_match.group(1).strip()
            if deps and deps != '[List of dependencies]':
                info['dependencies'] = [d.strip() for d in deps.split(',')]
    
    # Set defaults for missing required fields
    if 'title' not in info:
        info['title'] = "Untitled Task"
    
    if 'status' not in info:
        info['status'] = "proposed"
    
    if 'priority' not in info:
        info['priority'] = "medium"
    
    if 'created' not in info:
        info['created'] = datetime.now().strftime('%Y-%m-%d')
    
    # Always set last_updated to today
    info['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    return info

def add_frontmatter_to_file(file_path: str, frontmatter: Dict[str, Any]) -> bool:
    """Add YAML frontmatter to a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has frontmatter
        if content.startswith('---\n'):
            print(f"Skipping {file_path}: Already has frontmatter")
            return False
        
        # Format the YAML frontmatter
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)
        new_content = f"---\n{frontmatter_yaml}---\n\n{content}"
        
        # Write back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added frontmatter to {file_path}")
        return True
    except Exception as e:
        print(f"Error adding frontmatter to {file_path}: {e}")
        return False

def process_cip_files(cip_dir: str = 'cip', dry_run: bool = False) -> Tuple[int, int]:
    """Process all CIP files and add frontmatter."""
    if not os.path.exists(cip_dir):
        print(f"CIP directory {cip_dir} not found.")
        return 0, 0
    
    total = 0
    updated = 0
    
    for cip_file in glob.glob(f'{cip_dir}/cip*.md'):
        if cip_file == f'{cip_dir}/cip_template.md':
            continue
        
        total += 1
        print(f"Processing {cip_file}...")
        
        # Extract CIP information
        cip_info = extract_cip_info(cip_file)
        
        # Skip if already has frontmatter
        with open(cip_file, 'r', encoding='utf-8') as f:
            if f.read().startswith('---\n'):
                print(f"Skipping {cip_file}: Already has frontmatter")
                continue
        
        # Add frontmatter
        if not dry_run:
            if add_frontmatter_to_file(cip_file, cip_info):
                updated += 1
        else:
            print(f"Would add frontmatter to {cip_file}:")
            print(yaml.dump(cip_info, default_flow_style=False))
            updated += 1
    
    return total, updated

def process_backlog_files(backlog_dir: str = 'backlog', dry_run: bool = False) -> Tuple[int, int]:
    """Process all backlog files and add frontmatter."""
    if not os.path.exists(backlog_dir):
        print(f"Backlog directory {backlog_dir} not found.")
        return 0, 0
    
    total = 0
    updated = 0
    
    # Backlog directories to scan
    backlog_dirs = [
        f'{backlog_dir}/bugs/',
        f'{backlog_dir}/features/',
        f'{backlog_dir}/documentation/',
        f'{backlog_dir}/infrastructure/'
    ]
    
    for directory in backlog_dirs:
        if not os.path.exists(directory):
            continue
        
        for backlog_file in glob.glob(f'{directory}/*.md'):
            if 'task_template.md' in backlog_file:
                continue
            
            total += 1
            print(f"Processing {backlog_file}...")
            
            # Extract backlog item information
            backlog_info = extract_backlog_info(backlog_file)
            
            # Skip if already has frontmatter
            with open(backlog_file, 'r', encoding='utf-8') as f:
                if f.read().startswith('---\n'):
                    print(f"Skipping {backlog_file}: Already has frontmatter")
                    continue
            
            # Add frontmatter
            if not dry_run:
                if add_frontmatter_to_file(backlog_file, backlog_info):
                    updated += 1
            else:
                print(f"Would add frontmatter to {backlog_file}:")
                print(yaml.dump(backlog_info, default_flow_style=False))
                updated += 1
    
    return total, updated

def main():
    """Main function to run the migration script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Add YAML frontmatter to CIP and backlog files.')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without modifying files')
    parser.add_argument('--cip-only', action='store_true', help='Process only CIP files')
    parser.add_argument('--backlog-only', action='store_true', help='Process only backlog files')
    parser.add_argument('--cip-dir', default='cip', help='Directory containing CIP files')
    parser.add_argument('--backlog-dir', default='backlog', help='Directory containing backlog files')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("Performing dry run (no files will be modified)")
    
    cip_total, cip_updated = 0, 0
    backlog_total, backlog_updated = 0, 0
    
    if not args.backlog_only:
        cip_total, cip_updated = process_cip_files(args.cip_dir, args.dry_run)
    
    if not args.cip_only:
        backlog_total, backlog_updated = process_backlog_files(args.backlog_dir, args.dry_run)
    
    print("\nSummary:")
    if not args.backlog_only:
        print(f"CIP files: {cip_total} processed, {cip_updated} would be updated")
    
    if not args.cip_only:
        print(f"Backlog files: {backlog_total} processed, {backlog_updated} would be updated")
    
    if args.dry_run:
        print("\nThis was a dry run. No files were modified.")
        print("Run without --dry-run to apply the changes.")

if __name__ == "__main__":
    main() 