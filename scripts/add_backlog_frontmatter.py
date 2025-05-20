#!/usr/bin/env python3
"""
Script to add YAML frontmatter to backlog items lacking it.
"""

import os
import re
import glob
import yaml
from datetime import datetime

def extract_title(content):
    """Extract the title from a backlog item."""
    title_match = re.search(r'# Task:\s*(.*)', content)
    if title_match:
        return title_match.group(1).strip()
    return "Unknown Task"

def extract_status(content):
    """Extract the current status from a backlog item."""
    status_match = re.search(r'- \*\*Status\*\*:\s*(\w+)', content)
    if status_match:
        status = status_match.group(1).lower()
        # Map to one of the standardized statuses
        if status in ["proposed", "ready", "in_progress", "completed", "abandoned"]:
            return status
        elif "progress" in status:
            return "in_progress"
        elif "complete" in status:
            return "completed"
        elif "abandon" in status:
            return "abandoned"
        elif "ready" in status:
            return "ready"
        else:
            return "proposed"
    
    # Default to proposed if status can't be determined
    return "proposed"

def extract_priority(content):
    """Extract the priority from a backlog item."""
    priority_match = re.search(r'- \*\*Priority\*\*:\s*(\w+)', content)
    if priority_match:
        priority = priority_match.group(1).lower()
        # Map to one of the standardized priorities
        if priority in ["high", "medium", "low"]:
            return priority
        elif "high" in priority:
            return "high"
        elif "medium" in priority or "med" in priority:
            return "medium"
        else:
            return "low"
    
    # Default to medium if priority can't be determined
    return "medium"

def extract_date_from_filename(filename):
    """Extract date from backlog item filename."""
    # Format: YYYY-MM-DD_short-description.md or YYYYMMDD-short-description.md
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    
    date_match = re.search(r'(\d{8})', filename)
    if date_match:
        date_str = date_match.group(1)
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    
    return datetime.now().strftime("%Y-%m-%d")

def extract_owner(content):
    """Extract the owner from a backlog item."""
    owner_match = re.search(r'- \*\*Owner\*\*:\s*(.*)', content)
    if owner_match:
        return owner_match.group(1).strip()
    return "Unassigned"

def extract_tags(content):
    """Extract potential tags from a backlog item based on key terms and location."""
    tags = []
    
    # Add tags based on file location
    if "documentation" in content.lower() or "/documentation/" in os.getcwd():
        tags.append("documentation")
    
    if "feature" in content.lower() or "/features/" in os.getcwd():
        tags.append("feature")
    
    if "infrastructure" in content.lower() or "/infrastructure/" in os.getcwd():
        tags.append("infrastructure")
    
    if "bug" in content.lower() or "/bugs/" in os.getcwd():
        tags.append("bug")
    
    # Check for common terms
    if re.search(r'test|testing', content, re.IGNORECASE):
        tags.append("testing")
    
    if re.search(r'install|installation', content, re.IGNORECASE):
        tags.append("installation")
    
    if re.search(r'tenet', content, re.IGNORECASE):
        tags.append("tenets")
    
    if re.search(r'cip', content, re.IGNORECASE):
        tags.append("cip")
    
    # Always add the backlog tag
    tags.append("backlog")
    
    return tags

def has_frontmatter(content):
    """Check if the file already has YAML frontmatter."""
    return content.startswith('---')

def add_frontmatter_to_file(file_path):
    """Add YAML frontmatter to a backlog item if it doesn't have it already."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return
    
    # Skip if already has frontmatter
    if has_frontmatter(content):
        print(f"Skipping {file_path} - already has frontmatter")
        return
    
    # Generate ID from filename
    file_basename = os.path.basename(file_path)
    backlog_id = file_basename.replace('.md', '')
    
    # Extract metadata from content
    title = extract_title(content)
    status = extract_status(content)
    priority = extract_priority(content)
    date = extract_date_from_filename(file_basename)
    owner = extract_owner(content)
    tags = extract_tags(content)
    
    # Create frontmatter
    frontmatter = {
        'id': backlog_id,
        'title': title,
        'status': status,
        'priority': priority,
        'created': date,
        'last_updated': datetime.now().strftime("%Y-%m-%d"),
        'owner': owner,
        'tags': tags
    }
    
    # Format frontmatter as YAML
    yaml_str = yaml.dump(frontmatter, default_flow_style=False)
    
    # Add frontmatter to content
    new_content = f"---\n{yaml_str}---\n\n{content}"
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added frontmatter to {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def main():
    """Main function."""
    # Process all backlog items except for the template
    backlog_dirs = [
        'backlog/documentation',
        'backlog/features',
        'backlog/infrastructure',
        'backlog/bugs'
    ]
    
    for directory in backlog_dirs:
        if not os.path.exists(directory):
            continue
            
        backlog_files = glob.glob(f'{directory}/*.md')
        
        # Exclude template file
        backlog_files = [f for f in backlog_files if 'template' not in f]
        
        for file_path in backlog_files:
            add_frontmatter_to_file(file_path)

if __name__ == "__main__":
    main() 