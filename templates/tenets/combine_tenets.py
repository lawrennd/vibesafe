#!/usr/bin/env python3
"""
Script to combine individual tenet files into a single document.
Also creates a YAML representation for machine processing.
"""

import os
import re
import glob
from collections import OrderedDict
from datetime import datetime

# Optional import for YAML functionality
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


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
    
    # Write YAML representation (if yaml is available)
    if YAML_AVAILABLE:
        with open(output_yaml, 'w') as file:
            yaml.dump({'tenets': tenets_yaml}, file, default_flow_style=False)
    else:
        print("Warning: PyYAML not available, skipping YAML output")


def extract_tenet_metadata_for_cursor_rules(content):
    """Extract metadata from tenet content for cursor rule generation."""
    metadata = {}
    
    # Extract title
    title_match = re.search(r'\*\*Title\*\*:\s*(.+)', content)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract description
    desc_match = re.search(r'\*\*Description\*\*:\s*(.+)', content)
    if desc_match:
        metadata['description'] = desc_match.group(1).strip()
    
    # Extract quote
    quote_match = re.search(r'\*\*Quote\*\*:\s*\*"([^"]+)"\*', content)
    if quote_match:
        metadata['quote'] = quote_match.group(1).strip()
    
    # Extract examples
    examples_match = re.search(r'\*\*Examples\*\*:(.*?)(?=\*\*|$)', content, re.DOTALL)
    if examples_match:
        metadata['examples'] = examples_match.group(1).strip()
    
    # Extract counter-examples
    counter_match = re.search(r'\*\*Counter-examples\*\*:(.*?)(?=\*\*|$)', content, re.DOTALL)
    if counter_match:
        metadata['counter_examples'] = counter_match.group(1).strip()
    
    # Extract conflicts
    conflicts_match = re.search(r'\*\*Conflicts\*\*:(.*?)(?=\*\*|$)', content, re.DOTALL)
    if conflicts_match:
        metadata['conflicts'] = conflicts_match.group(1).strip()
    
    return metadata


def generate_cursor_rule_content(tenet_metadata):
    """Generate cursor rule content from tenet metadata."""
    rule_content = f"""---
description: "Project Tenet: {tenet_metadata.get('title', 'Unknown')}"
globs: "**/*"
alwaysApply: true
---

# Project Tenet: {tenet_metadata.get('title', 'Unknown')}

## Description
{tenet_metadata.get('description', 'No description provided.')}

## Quote
*"{tenet_metadata.get('quote', 'No quote provided.')}"*

## Examples
{tenet_metadata.get('examples', 'No examples provided.')}

## Counter-examples
{tenet_metadata.get('counter_examples', 'No counter-examples provided.')}

## Conflicts
{tenet_metadata.get('conflicts', 'No conflicts documented.')}
"""
    return rule_content


def generate_cursor_rules_from_tenets(tenets_directory, output_directory):
    """Generate cursor rules from project tenets."""
    from pathlib import Path
    
    tenets_dir = Path(tenets_directory)
    output_dir = Path(output_directory)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all tenet files recursively
    for tenet_file in tenets_dir.rglob("*.md"):
        if tenet_file.name == "README.md":
            continue
            
        # Extract tenet ID from filename or content
        tenet_id = tenet_file.stem
        
        # Read tenet content
        with open(tenet_file, 'r') as f:
            content = f.read()
        
        # Extract metadata
        metadata = extract_tenet_metadata_for_cursor_rules(content)
        
        # Generate cursor rule content
        rule_content = generate_cursor_rule_content(metadata)
        
        # Write cursor rule file
        rule_file = output_dir / f"project_tenet_{tenet_id}.mdc"
        
        # Only write if file doesn't exist (preserve existing rules)
        if not rule_file.exists():
            with open(rule_file, 'w') as f:
                f.write(rule_content)
            print(f"Generated cursor rule: {rule_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process project tenets')
    
    # New platform-neutral flag (CIP-0012 Phase 2)
    parser.add_argument('--generate-prompts', action='store_true',
                       help='Generate AI prompts from project tenets (platform-neutral base format)')
    
    # Legacy flag for backward compatibility (deprecated)
    parser.add_argument('--generate-cursor-rules', action='store_true',
                       help='(Deprecated: use --generate-prompts) Generate cursor rules from project tenets')
    
    parser.add_argument('--platform', default='cursor',
                       choices=['cursor', 'copilot', 'claude', 'codex', 'all'],
                       help='Target platform for prompt generation (default: cursor for backward compatibility)')
    
    parser.add_argument('--tenets-dir', default='.',
                       help='Directory containing tenet files (default: current directory)')
    
    parser.add_argument('--output-dir', default=None,
                       help='Output directory (default: .cursor/rules for legacy compatibility)')
    
    args = parser.parse_args()
    
    # Handle legacy flag with deprecation warning
    if args.generate_cursor_rules:
        print("⚠️  Warning: --generate-cursor-rules is deprecated, use --generate-prompts instead")
        args.generate_prompts = True
        if args.output_dir is None:
            args.output_dir = '.cursor/rules'  # Legacy default
    
    # Set default output directory based on mode
    if args.output_dir is None:
        args.output_dir = '.cursor/rules'  # Default for backward compatibility
    
    if args.generate_prompts or args.generate_cursor_rules:
        print(f"Generating prompts from project tenets for platform: {args.platform}...")
        generate_cursor_rules_from_tenets(args.tenets_dir, args.output_dir)
    else:
        # Original behavior - combine VibeSafe tenets
        tenets_yaml = []
        
        # Combine VibeSafe tenets
        combine_tenets(
            'vibesafe',
            'vibesafe-tenets.md',
            'vibesafe-tenets.yaml'
        )
        
        print("Tenets combined successfully!") 