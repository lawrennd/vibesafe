#!/usr/bin/env python3
"""
Script to add YAML frontmatter to CIP files lacking it.
"""

import os
import re
import glob
import yaml
from datetime import datetime

def extract_title(content):
    """Extract the title from a CIP file."""
    title_match = re.search(r'# CIP-[0-9A-F]+:(.*)', content)
    if title_match:
        return title_match.group(1).strip()
    return "Unknown Title"

def extract_status(content):
    """Extract the current status from a CIP file."""
    status_section = re.search(r'## Status.*?##', content, re.DOTALL)
    if not status_section:
        status_section = re.search(r'## Status.*', content, re.DOTALL)
    
    if status_section:
        section_text = status_section.group(0)
        
        # Check which status is marked with [x]
        if re.search(r'- \[x\]\s*Proposed', section_text):
            return "proposed"
        elif re.search(r'- \[x\]\s*Accepted', section_text):
            return "accepted"
        elif re.search(r'- \[x\]\s*Implemented', section_text):
            return "implemented"
        elif re.search(r'- \[x\]\s*Closed', section_text):
            return "closed"
    
    # Default to proposed if status can't be determined
    return "proposed"

def extract_date(content):
    """Extract the date from a CIP file."""
    # Look for the date specified in the status section
    date_match = re.search(r'Proposed:.*?\[(\d{4}-\d{2}-\d{2})\]', content)
    if date_match:
        return date_match.group(1)
    
    # Look for the date at the bottom of the file
    date_match = re.search(r'## Date\s*(\d{4}-\d{2}-\d{2})', content, re.DOTALL)
    if date_match:
        return date_match.group(1)
    
    # Look for any date format in the file
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        return date_match.group(1)
    
    # Default to today's date if no date found
    return datetime.now().strftime("%Y-%m-%d")

def extract_author(content):
    """Extract the author from a CIP file."""
    author_match = re.search(r'## Author\s*(.*)', content)
    if author_match:
        return author_match.group(1).strip()
    return "Unknown"

def extract_tags(content):
    """Extract potential tags from a CIP file based on key terms."""
    tags = []
    
    # Check for common categories
    if re.search(r'document|documentation', content, re.IGNORECASE):
        tags.append("documentation")
    
    if re.search(r'test|testing', content, re.IGNORECASE):
        tags.append("testing")
    
    if re.search(r'install|installation', content, re.IGNORECASE):
        tags.append("installation")
    
    if re.search(r'tenet', content, re.IGNORECASE):
        tags.append("tenets")
    
    if re.search(r'backlog', content, re.IGNORECASE):
        tags.append("backlog")
    
    if re.search(r'template', content, re.IGNORECASE):
        tags.append("templates")
    
    # Always add the cip tag
    tags.append("cip")
    
    return tags

def has_frontmatter(content):
    """Check if the file already has YAML frontmatter."""
    return content.startswith('---')

def add_frontmatter_to_file(file_path):
    """Add YAML frontmatter to a CIP file if it doesn't have it already."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has frontmatter
    if has_frontmatter(content):
        print(f"Skipping {file_path} - already has frontmatter")
        return
    
    # Extract CIP ID from filename
    cip_id = os.path.basename(file_path).replace('cip', '').replace('.md', '')
    
    # Extract metadata from content
    title = extract_title(content)
    status = extract_status(content)
    date = extract_date(content)
    author = extract_author(content)
    tags = extract_tags(content)
    
    # Create frontmatter
    frontmatter = {
        'id': cip_id,
        'title': title,
        'status': status,
        'created': date,
        'last_updated': datetime.now().strftime("%Y-%m-%d"),
        'author': author,
        'tags': tags
    }
    
    # Format frontmatter as YAML
    yaml_str = yaml.dump(frontmatter, default_flow_style=False)
    
    # Add frontmatter to content
    new_content = f"---\n{yaml_str}---\n\n{content}"
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added frontmatter to {file_path}")

def main():
    """Main function."""
    # Process all CIP files except for the template
    cip_files = glob.glob('cip/cip*.md')
    
    # Exclude template file
    cip_files = [f for f in cip_files if 'template' not in f]
    
    for file_path in cip_files:
        add_frontmatter_to_file(file_path)

if __name__ == "__main__":
    main() 