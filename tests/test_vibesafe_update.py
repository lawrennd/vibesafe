#!/usr/bin/env python3
"""
Tests for the VibeSafe Update script.
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# Import the script
import vibesafe_update

class TestVibeSafeUpdate(unittest.TestCase):
    """Test cases for the VibeSafe Update script."""
    
    def setUp(self):
        """Set up a temporary workspace for testing."""
        self.workspace_dir = tempfile.mkdtemp()
        
        # Create the basic VibeSafe directory structure
        os.makedirs(os.path.join(self.workspace_dir, "cip"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, "backlog"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, "scripts"), exist_ok=True)
    
    def tearDown(self):
        """Clean up the temporary workspace."""
        shutil.rmtree(self.workspace_dir)
    
    def test_get_components(self):
        """Test that the get_components function returns a list of components."""
        components = vibesafe_update.get_components()
        self.assertIsInstance(components, list)
        self.assertTrue(len(components) > 0)
        
        # Check that all items in the list are Component objects
        for component in components:
            self.assertIsInstance(component, vibesafe_update.Component)
    
    def test_check_installation_empty_workspace(self):
        """Test check_installation on an empty workspace."""
        # Use a mock args object
        class Args:
            force = False
        
        args = Args()
        
        installed, missing = vibesafe_update.check_installation(self.workspace_dir, args)
        
        # An empty workspace should have no installed components
        self.assertEqual(len(installed), 0)
        
        # All components should be missing
        self.assertEqual(len(missing), len(vibesafe_update.get_components()))
    
    def test_whats_next_component(self):
        """Test the WhatsNextComponent."""
        component = vibesafe_update.WhatsNextComponent()
        
        # Should not be installed initially
        self.assertFalse(component.is_installed(self.workspace_dir))
        
        # Install the component
        result = component.install(self.workspace_dir)
        self.assertTrue(result)
        
        # Should now be installed
        self.assertTrue(component.is_installed(self.workspace_dir))
        
        # Verify the files exist
        self.assertTrue(os.path.exists(os.path.join(self.workspace_dir, "scripts", "whats_next.py")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_dir, "whats-next")))
    
    def test_yaml_frontmatter_component(self):
        """Test the YAMLFrontmatterComponent."""
        component = vibesafe_update.YAMLFrontmatterComponent()
        
        # Should not be installed initially
        self.assertFalse(component.is_installed(self.workspace_dir))
        
        # Install the component
        result = component.install(self.workspace_dir)
        self.assertTrue(result)
        
        # Should now be installed
        self.assertTrue(component.is_installed(self.workspace_dir))
        
        # Verify the files exist
        self.assertTrue(os.path.exists(os.path.join(self.workspace_dir, "scripts", "add_frontmatter.py")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_dir, "scripts", "add_cip_frontmatter.py")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_dir, "scripts", "add_backlog_frontmatter.py")))
    
    def test_update_all_components(self):
        """Test updating all components in an empty workspace."""
        # Use a mock args object
        class Args:
            force = False
            check = False
        
        args = Args()
        
        # Initially no components should be installed
        installed, missing = vibesafe_update.check_installation(self.workspace_dir, args)
        self.assertEqual(len(installed), 0)
        
        # Run update
        result = vibesafe_update.update(self.workspace_dir, args)
        self.assertTrue(result)
        
        # Now all components should be installed
        installed, missing = vibesafe_update.check_installation(self.workspace_dir, args)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(installed), len(vibesafe_update.get_components()))

if __name__ == "__main__":
    unittest.main() 