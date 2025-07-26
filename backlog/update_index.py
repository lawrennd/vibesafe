#!/usr/bin/env python
"""
Update the backlog index.md file based on the current task files.

This script scans all task files in the backlog directory structure,
extracts their metadata, and generates an updated index.md file.

The script accepts status values in multiple formats:
- Lowercase with underscores: "proposed", "in_progress", "completed"
- Capitalized with spaces: "Proposed", "In Progress", "Completed"  
- Mixed case: "Ready", "abandoned", etc.
All formats are normalized internally to lowercase with underscores.
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

# Categories to organize backlog items
CATEGORIES = ['documentation', 'infrastructure', 'features', 'bugs']
# Use lowercase internally but accept both formats
STATUSES = ['proposed', 'ready', 'in_progress', 'completed', 'abandoned']

def normalize_status(status):
    """Normalize status to lowercase with underscores."""
    if not status:
        return None
    # Convert to lowercase and replace spaces with underscores
    return status.lower().replace(' ', '_').replace('-', '_')

def extract_task_metadata(filepath):
    """Extract metadata from a task file."""
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
            
            # Check if file has YAML frontmatter
            if content.startswith('---'):
                # Split content into frontmatter and body
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    body_text = parts[2]
                    
                    # Parse YAML frontmatter
                    try:
                        front_matter = yaml.safe_load(frontmatter_text)
                        if front_matter:
                            metadata['id'] = front_matter.get('id', id_from_filename)
                            metadata['title'] = front_matter.get('title', None)
                            metadata['status'] = normalize_status(front_matter.get('status', None))
                            metadata['priority'] = front_matter.get('priority', None)
                            metadata['created'] = front_matter.get('created', None)
                            # Handle both 'updated' and 'last_updated' field names
                            metadata['updated'] = front_matter.get('updated', front_matter.get('last_updated', None))
                            metadata['category'] = front_matter.get('category', category)
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML in {filepath}: {e}")
                    
                    # Also try to extract title from markdown header in body
                    title_match = re.search(r'# Task: (.*)', body_text)
                    if title_match and not metadata['title']:
                        metadata['title'] = title_match.group(1)
                        
                else:
                    # No valid frontmatter, try old format
                    _extract_old_format_metadata(content, metadata)
            else:
                # No frontmatter, try old format
                _extract_old_format_metadata(content, metadata)
                
        return metadata
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return None

def _extract_old_format_metadata(content, metadata):
    """Extract metadata from old format task files."""
    # Extract title from the first line
    title_match = re.search(r'# Task: (.*)', content)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    # Extract ID from content (overrides filename-based ID if found)
    id_match = re.search(r'\*\*ID\*\*: (.*)', content)
    if id_match:
        metadata['id'] = id_match.group(1).strip()
    
    # Extract status
    status_match = re.search(r'\*\*Status\*\*: (.*)', content)
    if status_match:
        metadata['status'] = status_match.group(1).strip()
    
    # Extract priority
    priority_match = re.search(r'\*\*Priority\*\*: (.*)', content)
    if priority_match:
        metadata['priority'] = priority_match.group(1).strip()
    
    # Extract created date
    created_match = re.search(r'\*\*Created\*\*: (.*)', content)
    if created_match:
        metadata['created'] = created_match.group(1).strip()
    
    # Extract updated date
    updated_match = re.search(r'\*\*Last Updated\*\*: (.*)', content)
    if updated_match:
        metadata['updated'] = updated_match.group(1).strip()

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
    content = []
    content.append("# Lynguine Backlog Index\n")
    content.append("This file provides an overview of all current backlog items organized by category and status.\n")
    
    # Organize tasks by category and status
    categorized_tasks = {}
    for category in CATEGORIES:
        categorized_tasks[category] = {}
        for status in STATUSES:
            categorized_tasks[category][status] = []
    
    for task in tasks:
        if task is None or 'category' not in task or task['category'] is None or 'status' not in task or task['status'] is None:
            print(f"Skipping invalid task: {task}")
            continue
        
        category = task['category']
        status = normalize_status(task['status'])
        
        if category in categorized_tasks and status in categorized_tasks[category]:
            categorized_tasks[category][status].append(task)
        else:
            print(f"Skipping task with invalid category or status: {category}, {status}")
    
    # Generate the main section of the index
    for category in CATEGORIES:
        content.append(f"## {category.title()}\n")
        
        for status in ['ready', 'in_progress', 'proposed']:
            content.append(f"### {status.replace('_', ' ').title()}\n")
            
            tasks_with_status = categorized_tasks[category][status]
            if tasks_with_status:
                # Sort by created date
                def sort_key(task):
                    return task.get('created', '')
                
                for task in sorted(tasks_with_status, key=sort_key, reverse=True):
                    relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
                    content.append(f"- [{task['title']}]({relative_path})\n")
            else:
                content.append(f"*No tasks currently {status.lower()}.*\n")
            
            content.append("")
    
    # Add recently completed and abandoned tasks
    content.append("---\n")
    content.append("## Recently Completed Tasks\n")
    
    completed_tasks = []
    for category in CATEGORIES:
        if 'completed' in categorized_tasks[category]:
            completed_tasks.extend(categorized_tasks[category]['completed'])
    
    if completed_tasks:
        def sort_key(task):
            return task.get('updated', '') or ''
        
        for task in sorted(completed_tasks, key=sort_key, reverse=True)[:5]:  # Show only recent 5
            relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
            content.append(f"- [{task['title']}]({relative_path})\n")
    else:
        content.append("*No tasks recently completed.*\n")
    
    content.append("\n## Recently Abandoned Tasks\n")
    
    abandoned_tasks = []
    for category in CATEGORIES:
        if 'abandoned' in categorized_tasks[category]:
            abandoned_tasks.extend(categorized_tasks[category]['abandoned'])
    
    if abandoned_tasks:
        def sort_key(task):
            return task.get('updated', '') or ''
        
        for task in sorted(abandoned_tasks, key=sort_key, reverse=True)[:5]:  # Show only recent 5
            relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
            content.append(f"- [{task['title']}]({relative_path})\n")
    else:
        content.append("*No tasks recently abandoned.*\n")
    
    return "\n".join(content)

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