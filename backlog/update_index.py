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
            
            # First try to extract YAML frontmatter
            frontmatter = extract_yaml_frontmatter(content)
            if frontmatter:
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
            
            # If YAML frontmatter didn't provide all metadata, try traditional format
            
            # Extract title from the first line if not already set
            if not metadata['title']:
                title_match = re.search(r'# Task: (.*)', content)
                if title_match:
                    metadata['title'] = title_match.group(1)
            
            # Extract ID from content if not already set
            if not metadata['id'] and id_from_filename:
                id_match = re.search(r'\*\*ID\*\*: (.*)', content)
                if id_match:
                    metadata['id'] = id_match.group(1).strip()
            
            # Extract status if not already set
            if not metadata['status']:
                status_match = re.search(r'\*\*Status\*\*: (.*)', content)
                if status_match:
                    metadata['status'] = status_match.group(1).strip()
            
            # Extract priority if not already set
            if not metadata['priority']:
                priority_match = re.search(r'\*\*Priority\*\*: (.*)', content)
                if priority_match:
                    metadata['priority'] = priority_match.group(1).strip()
            
            # Extract created date if not already set
            if not metadata['created']:
                created_match = re.search(r'\*\*Created\*\*: (.*)', content)
                if created_match:
                    metadata['created'] = created_match.group(1).strip()
            
            # Extract updated date if not already set
            if not metadata['updated']:
                updated_match = re.search(r'\*\*Last Updated\*\*: (.*)', content)
                if updated_match:
                    metadata['updated'] = updated_match.group(1).strip()
                
        return metadata
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return None

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
        status = task['status'].strip()
        
        # Ensure status is one of the valid statuses (case-insensitive)
        matching_status = None
        for valid_status in STATUSES:
            if status.lower() == valid_status.lower():
                matching_status = valid_status
                break
        
        if matching_status and category in categorized_tasks and matching_status in categorized_tasks[category]:
            categorized_tasks[category][matching_status].append(task)
        else:
            print(f"Skipping task with invalid category or status: {category}, {status}")
    
    # Generate the main section of the index
    for category in CATEGORIES:
        content.append(f"## {category.title()}\n")
        
        for status in ['Ready', 'In Progress', 'Proposed']:
            content.append(f"### {status}\n")
            
            tasks_with_status = categorized_tasks[category][status]
            if tasks_with_status:
                # Sort by created date
                def sort_key(task):
                    # Return empty string if created is None to avoid comparison issues
                    return task.get('created', '') or ''
                
                for task in sorted(tasks_with_status, key=sort_key, reverse=True):
                    relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
                    # Use title if available, otherwise use ID
                    title = task.get('title') or task.get('id', 'Untitled Task')
                    content.append(f"- [{title}]({relative_path})\n")
            else:
                content.append(f"*No tasks currently {status.lower()}.*\n")
            
            content.append("")
    
    # Add recently completed and abandoned tasks
    content.append("---\n")
    content.append("## Recently Completed Tasks\n")
    
    completed_tasks = []
    for category in CATEGORIES:
        completed_tasks.extend(categorized_tasks[category]['Completed'])
    
    if completed_tasks:
        def sort_key(task):
            # Return empty string if updated is None to avoid comparison issues
            return task.get('updated', '') or ''
        
        for task in sorted(completed_tasks, key=sort_key, reverse=True)[:5]:  # Show only recent 5
            relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
            title = task.get('title') or task.get('id', 'Untitled Task')
            content.append(f"- [{title}]({relative_path})\n")
    else:
        content.append("*No tasks recently completed.*\n")
    
    content.append("\n## Recently Abandoned Tasks\n")
    
    abandoned_tasks = []
    for category in CATEGORIES:
        abandoned_tasks.extend(categorized_tasks[category]['Abandoned'])
    
    if abandoned_tasks:
        def sort_key(task):
            # Return empty string if updated is None to avoid comparison issues
            return task.get('updated', '') or ''
        
        for task in sorted(abandoned_tasks, key=sort_key, reverse=True)[:5]:  # Show only recent 5
            relative_path = os.path.relpath(task['filepath'], Path(__file__).parent)
            title = task.get('title') or task.get('id', 'Untitled Task')
            content.append(f"- [{title}]({relative_path})\n")
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