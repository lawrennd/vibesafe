#!/usr/bin/env python3
"""
Update the backlog index file based on the current task files.

This script scans all task files in the backlog directory structure,
extracts their metadata, and generates an updated index.md file.
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

__all__ = [
    'extract_yaml_frontmatter',
    'extract_task_metadata',
    'find_all_task_files',
    'generate_index_content',
    'update_index',
    'CATEGORIES',
    'STATUSES'
]

# Categories to organize backlog items
CATEGORIES = ['documentation', 'infrastructure', 'features', 'bugs']
STATUSES = ['Proposed', 'Ready', 'In Progress', 'Completed', 'Abandoned']

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from content if present."""
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        try:
            return yaml.safe_load(frontmatter_text)
        except Exception as e:
            print(f"Error parsing YAML frontmatter: {str(e)}")
            return {}
    return {}

def extract_task_metadata(filepath):
    """Extract metadata from a task file. Requires YAML frontmatter."""
    # Extract category from filepath
    filepath_str = str(filepath)
    category = None
    for cat in CATEGORIES:
        if f"{os.sep}{cat}{os.sep}" in filepath_str:
            category = cat
            break
    
    # Extract ID from filename if using either naming convention
    filename = filepath.name
    id_from_filename = None
    
    # Try YYYY-MM-DD_description.md pattern
    date_desc_match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)\.md', filename)
    if date_desc_match:
        id_from_filename = filename[:-3]  # Remove .md extension
    
    # Try YYYYMMDD-description.md pattern
    date_desc_match2 = re.match(r'(\d{8})-(.+)\.md', filename)
    if date_desc_match2:
        id_from_filename = filename[:-3]  # Remove .md extension
    
    metadata = {
        'filepath': filepath,
        'id': id_from_filename,  # Default to filename-based ID
        'title': None,
        'status': None,
        'priority': None,
        'created': None,
        'updated': None,
        'category': category
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Extract YAML frontmatter
            frontmatter = extract_yaml_frontmatter(content)
            if not frontmatter:
                raise ValueError(f"Missing YAML frontmatter in file: {filepath}")
            # Map frontmatter fields to metadata
            if 'id' in frontmatter:
                metadata['id'] = frontmatter['id']
            if 'title' in frontmatter:
                metadata['title'] = frontmatter['title']
            if 'status' in frontmatter:
                metadata['status'] = frontmatter['status']
            if 'priority' in frontmatter:
                metadata['priority'] = frontmatter['priority']
            if 'created' in frontmatter:
                metadata['created'] = frontmatter['created']
            if 'last_updated' in frontmatter:
                metadata['updated'] = frontmatter['last_updated']
        return metadata
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        raise

def find_all_task_files():
    """Find all task files in the backlog directory."""
    backlog_dir = Path(__file__).parent
    task_files = []
    
    print(f"Searching for task files in {backlog_dir}")
    
    for category in CATEGORIES:
        category_dir = backlog_dir / category
        if category_dir.exists():
            print(f"Checking category directory: {category_dir}")
            for file in category_dir.glob('*.md'):
                # Skip README and index files, but include all task files regardless of naming convention
                if file.name != 'README.md' and file.name != 'index.md' and not file.name.startswith('_'):
                    print(f"Found task file: {file}")
                    task_files.append(file)
    
    return task_files

def generate_index_content(tasks):
    """Generate the content for the index.md file."""
    # Initialize categorized tasks
    categorized_tasks = {}
    for category in CATEGORIES:
        categorized_tasks[category] = {}
        for status in STATUSES:
            categorized_tasks[category][status] = []
    
    # Categorize tasks
    for task in tasks:
        if task is None or 'category' not in task or task['category'] is None or 'status' not in task or task['status'] is None:
            continue
        
        category = task['category']
        status = task['status'].strip()
        
        # Ensure status is one of the valid statuses (case-insensitive)
        matching_status = None
        for valid_status in STATUSES:
            if status.lower() == valid_status.lower():
                matching_status = valid_status
                break
        
        if matching_status and category in categorized_tasks and matching_status in categorized_tasks[category]:
            categorized_tasks[category][matching_status].append(task)
    
    # Generate content
    content = "# Backlog Index\n\n"
    
    # Add sections for each category
    for category in CATEGORIES:
        content += f"## {category.title()}\n\n"
        
        # Add sections for each status
        for status in STATUSES:
            tasks = categorized_tasks[category][status]
            if tasks:
                content += f"### {status}\n\n"
                
                # Sort tasks by priority (high to low)
                tasks.sort(key=lambda x: x.get('priority', '').lower(), reverse=True)
                
                # Add task entries
                for task in tasks:
                    content += f"- [{task['title']}]({task['filepath'].name})"
                    if task.get('priority'):
                        content += f" (Priority: {task['priority']})"
                    content += "\n"
                
                content += "\n"
    
    return content

def update_index():
    """Update the index.md file with current backlog items."""
    backlog_dir = Path(__file__).parent
    index_file = backlog_dir / "index.md"
    
    # Find all task files
    task_files = find_all_task_files()
    
    # Extract metadata from each task file
    tasks = [extract_task_metadata(file) for file in task_files]
    
    # Generate the index content
    content = generate_index_content(tasks)
    
    # Write the index file
    with open(index_file, 'w') as f:
        f.write(content)
    
    print(f"Updated {index_file} with {len(task_files)} tasks.")

if __name__ == "__main__":
    update_index() 