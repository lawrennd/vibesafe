#!/usr/bin/env python3
"""
VibeSafe Update Script

This script checks for and adds missing components to a VibeSafe installation,
ensuring that all features and tools are up-to-date.
"""

import os
import sys
import shutil
import argparse
import glob
import subprocess
import yaml
from pathlib import Path

VERSION = "0.1.0"

class Colors:
    """ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

class Component:
    """Base class for VibeSafe components that can be managed by the update script."""
    def __init__(self, name, description, version):
        self.name = name
        self.description = description
        self.version = version
        self.required_files = []
        
    def is_installed(self, workspace_dir):
        """Check if the component is installed."""
        for file_path in self.required_files:
            full_path = os.path.join(workspace_dir, file_path)
            if not os.path.exists(full_path):
                return False
        return True
        
    def install(self, workspace_dir, force=False):
        """Install the component."""
        raise NotImplementedError("Subclasses must implement the install method")
        
    def __str__(self):
        return f"{self.name} (v{self.version})"

class WhatsNextComponent(Component):
    """The What's Next script component."""
    def __init__(self):
        super().__init__(
            "What's Next Script", 
            "A script that provides an overview of project status and recommends next steps",
            "1.0.0"
        )
        self.required_files = [
            "scripts/whats_next.py",
            "whats-next"
        ]
    
    def install(self, workspace_dir, force=False):
        """Install the What's Next script."""
        print(f"{Colors.BOLD}Installing {self.name}...{Colors.ENDC}")
        
        # Create directories if they don't exist
        os.makedirs(os.path.join(workspace_dir, "scripts"), exist_ok=True)
        
        # Define the paths
        script_path = os.path.join(workspace_dir, "scripts", "whats_next.py")
        wrapper_path = os.path.join(workspace_dir, "whats-next")
        
        # Create the Python script
        if not os.path.exists(script_path) or force:
            with open(script_path, 'w') as f:
                f.write(WHATS_NEXT_SCRIPT_CONTENT)
            print(f"{Colors.GREEN}Created {script_path}{Colors.ENDC}")
        
        # Create the wrapper script
        if not os.path.exists(wrapper_path) or force:
            with open(wrapper_path, 'w') as f:
                f.write(WHATS_NEXT_WRAPPER_CONTENT)
            
            # Make it executable
            os.chmod(wrapper_path, 0o755)
            print(f"{Colors.GREEN}Created {wrapper_path}{Colors.ENDC}")
            
        return True

class YAMLFrontmatterComponent(Component):
    """Component for adding YAML frontmatter to CIP and backlog files."""
    def __init__(self):
        super().__init__(
            "YAML Frontmatter Scripts", 
            "Scripts to add YAML frontmatter to CIP and backlog files",
            "1.0.0"
        )
        self.required_files = [
            "scripts/add_frontmatter.py",
            "scripts/add_cip_frontmatter.py",
            "scripts/add_backlog_frontmatter.py"
        ]
    
    def install(self, workspace_dir, force=False):
        """Install the YAML frontmatter scripts."""
        print(f"{Colors.BOLD}Installing {self.name}...{Colors.ENDC}")
        
        # Create directories if they don't exist
        os.makedirs(os.path.join(workspace_dir, "scripts"), exist_ok=True)
        
        # Define the paths
        base_script_path = os.path.join(workspace_dir, "scripts", "add_frontmatter.py")
        cip_script_path = os.path.join(workspace_dir, "scripts", "add_cip_frontmatter.py")
        backlog_script_path = os.path.join(workspace_dir, "scripts", "add_backlog_frontmatter.py")
        
        # Create the base script
        if not os.path.exists(base_script_path) or force:
            with open(base_script_path, 'w') as f:
                f.write(ADD_FRONTMATTER_SCRIPT_CONTENT)
            os.chmod(base_script_path, 0o755)
            print(f"{Colors.GREEN}Created {base_script_path}{Colors.ENDC}")
        
        # Create the CIP frontmatter script
        if not os.path.exists(cip_script_path) or force:
            with open(cip_script_path, 'w') as f:
                f.write(ADD_CIP_FRONTMATTER_SCRIPT_CONTENT)
            os.chmod(cip_script_path, 0o755)
            print(f"{Colors.GREEN}Created {cip_script_path}{Colors.ENDC}")
            
        # Create the backlog frontmatter script
        if not os.path.exists(backlog_script_path) or force:
            with open(backlog_script_path, 'w') as f:
                f.write(ADD_BACKLOG_FRONTMATTER_SCRIPT_CONTENT)
            os.chmod(backlog_script_path, 0o755)
            print(f"{Colors.GREEN}Created {backlog_script_path}{Colors.ENDC}")
            
        return True

def get_components():
    """Return a list of all available components."""
    return [
        WhatsNextComponent(),
        YAMLFrontmatterComponent()
    ]

def check_installation(workspace_dir, args):
    """Check which components are installed and which are missing."""
    print(f"{Colors.BOLD}Checking VibeSafe installation in {workspace_dir}...{Colors.ENDC}")
    
    components = get_components()
    missing_components = []
    installed_components = []
    
    for component in components:
        if component.is_installed(workspace_dir):
            status = f"{Colors.GREEN}Installed{Colors.ENDC}"
            installed_components.append(component)
        else:
            status = f"{Colors.RED}Missing{Colors.ENDC}"
            missing_components.append(component)
        
        print(f"{Colors.BOLD}{component.name}{Colors.ENDC} (v{component.version}): {status}")
    
    return installed_components, missing_components

def update(workspace_dir, args):
    """Update the VibeSafe installation by adding missing components."""
    installed_components, missing_components = check_installation(workspace_dir, args)
    
    if not missing_components:
        print(f"\n{Colors.GREEN}All components are installed!{Colors.ENDC}")
        return True
    
    print(f"\n{Colors.BOLD}Installing missing components...{Colors.ENDC}")
    
    success = True
    for component in missing_components:
        try:
            if not component.install(workspace_dir, args.force):
                success = False
        except Exception as e:
            print(f"{Colors.RED}Error installing {component.name}: {str(e)}{Colors.ENDC}")
            success = False
    
    if success:
        print(f"\n{Colors.GREEN}Update completed successfully!{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}Update completed with errors. Some components may not have been installed correctly.{Colors.ENDC}")
    
    return success

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Update VibeSafe with missing components.')
    parser.add_argument('--force', action='store_true', help='Force update of all components even if already installed')
    parser.add_argument('--check', action='store_true', help='Only check for missing components without installing them')
    parser.add_argument('--version', action='store_true', help='Show version information')
    parser.add_argument('--workspace', help='Path to the VibeSafe workspace directory', default=os.getcwd())
    
    args = parser.parse_args()
    
    if args.version:
        print(f"VibeSafe Update Script v{VERSION}")
        return 0
    
    workspace_dir = os.path.abspath(args.workspace)
    
    # Check if the directory is a VibeSafe workspace
    if not os.path.isdir(os.path.join(workspace_dir, "cip")) or not os.path.isdir(os.path.join(workspace_dir, "backlog")):
        print(f"{Colors.RED}Error: The specified directory does not appear to be a valid VibeSafe workspace.{Colors.ENDC}")
        return 1
    
    print(f"{Colors.BOLD}VibeSafe Update Script v{VERSION}{Colors.ENDC}")
    print(f"Workspace: {workspace_dir}\n")
    
    if args.check:
        check_installation(workspace_dir, args)
        return 0
    
    return 0 if update(workspace_dir, args) else 1

# Script content templates
WHATS_NEXT_WRAPPER_CONTENT = """#!/bin/sh
# Wrapper script for the What's Next Python script

# Determine the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the Python script
python "$SCRIPT_DIR/scripts/whats_next.py" "$@"
"""

# This is a placeholder - in a real implementation, we would include the actual 
# content of the scripts or download them from a repository
WHATS_NEXT_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"
What's Next Script for VibeSafe

This script analyzes the current state of a VibeSafe project and provides
recommendations on what to do next.
\"\"\"

# Placeholder for the actual script content
# In a real implementation, this would contain the full script

print("Placeholder for the What's Next script")
print("In a real implementation, this would contain the full script content")
"""

ADD_FRONTMATTER_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"
Base module for adding YAML frontmatter to files
\"\"\"

# Placeholder for the actual script content
"""

ADD_CIP_FRONTMATTER_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"
Script to add YAML frontmatter to CIP files
\"\"\"

# Placeholder for the actual script content
"""

ADD_BACKLOG_FRONTMATTER_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"
Script to add YAML frontmatter to backlog files
\"\"\"

# Placeholder for the actual script content
"""

if __name__ == "__main__":
    sys.exit(main()) 