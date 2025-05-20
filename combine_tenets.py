#!/usr/bin/env python3
"""
Script to combine individual tenet files into a single document.
Also creates a YAML representation for machine processing.
"""

import os
import re
import yaml
import glob
from collections import OrderedDict
from datetime import datetime


def extract_tenet_metadata(file_path):
    """Extract metadata from a tenet markdown file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    tenet_id = re.search(r'## Tenet: (\S+)', content)
    title = re.search(r'\*\*Title\*\*: (.+?)[\r\n]', content)
    description = re.search(r'\*\*Description\*\*: (.+?)[\r\n]', content, re.DOTALL)
    quote = re.search(r'\*\*Quote\*\*: \*"(.+?)"\*', content)
    version = re.search(r'\*\*Version\*\*: (.+?)[\r\n]', content)
    
    metadata = OrderedDict()
    if tenet_id:
        metadata['id'] = tenet_id.group(1).strip()
    if title:
        metadata['title'] = title.group(1).strip()
    if description:
        metadata['description'] = description.group(1).strip()
    if quote:
        metadata['quote'] = quote.group(1).strip()
    if version:
        metadata['version'] = version.group(1).strip()
    
    return metadata


def combine_tenets(directory, output_md, output_yaml):
    """Combine individual tenet files into a single markdown and YAML file."""
    files = glob.glob(os.path.join(directory, '*.md'))
    files.sort()  # Sort files alphabetically
    
    tenets = []
    tenets_yaml = []  # Initialize the list here
    
    for file_path in files:
        with open(file_path, 'r') as file:
            content = file.read()
        tenets.append(content)
        
        # Extract metadata for YAML
        metadata = extract_tenet_metadata(file_path)
        if metadata:
            tenets_yaml.append(metadata)
    
    # Write combined Markdown
    with open(output_md, 'w') as file:
        file.write(f"# {os.path.basename(directory).capitalize()} Tenets\n\n")
        file.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d')}*\n\n")
        file.write("This document combines all individual tenet files from the project.\n\n")
        file.write("\n\n".join(tenets))
    
    # Write YAML representation
    with open(output_yaml, 'w') as file:
        yaml.dump({'tenets': tenets_yaml}, file, default_flow_style=False)
    
    return tenets_yaml


if __name__ == "__main__":
    # Combine VibeSafe tenets
    combine_tenets(
        'vibesafe',
        'vibesafe-tenets.md',
        'vibesafe-tenets.yaml'
    )
    
    print("Tenets combined successfully!") 