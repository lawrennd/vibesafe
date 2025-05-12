"""
Tests for the What's Next script.

This module contains tests for the script's functionality, ensuring that it
properly analyzes the repository status, CIPs, and backlog items.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.whats_next import (
    extract_frontmatter,
    has_expected_frontmatter,
    run_command,
    get_git_status,
    generate_next_steps,
    scan_requirements,
)


class TestWhatsNextCore(unittest.TestCase):
    """Test the core functionality of the What's Next script."""

    def test_run_command(self):
        """Test the run_command function."""
        # Test a simple command
        output, exit_code = run_command(["echo", "test"])
        self.assertEqual(output, "test")
        self.assertEqual(exit_code, 0)

        # Test a failing command
        output, exit_code = run_command(["ls", "non_existent_directory"])
        self.assertTrue(exit_code != 0)

    @patch("scripts.whats_next.run_command")
    def test_get_git_status(self, mock_run_command):
        """Test the get_git_status function."""
        # Mock the output of git branch --show-current
        mock_run_command.side_effect = [
            ("main", 0),  # git branch --show-current
            ("abc123 commit message 1\ndef456 commit message 2", 0),  # git log
            ("M  file1.txt\n?? file2.txt", 0),  # git status
        ]

        git_info = get_git_status()

        # Check the result
        self.assertEqual(git_info["current_branch"], "main")
        self.assertEqual(len(git_info["recent_commits"]), 2)
        self.assertEqual(git_info["recent_commits"][0]["hash"], "abc123")
        self.assertEqual(git_info["recent_commits"][0]["message"], "commit message 1")
        self.assertEqual(len(git_info["modified_files"]), 1)
        self.assertEqual(git_info["modified_files"][0]["path"], "file1.txt")
        self.assertEqual(len(git_info["untracked_files"]), 1)
        self.assertEqual(git_info["untracked_files"][0], "file2.txt")

    def test_extract_frontmatter(self):
        """Test the extract_frontmatter function."""
        # Create a temporary file with frontmatter
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
            temp.write("""---
title: Test Title
status: proposed
---

# Test Content
""")
            temp_path = temp.name

        try:
            # Test extracting frontmatter
            frontmatter = extract_frontmatter(temp_path)
            self.assertEqual(frontmatter["title"], "Test Title")
            self.assertEqual(frontmatter["status"], "proposed")
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_has_expected_frontmatter(self):
        """Test the has_expected_frontmatter function."""
        # Create a temporary file with frontmatter
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
            temp.write("""---
title: Test Title
status: proposed
---

# Test Content
""")
            temp_path = temp.name

        try:
            # Test with all required keys present
            self.assertTrue(has_expected_frontmatter(temp_path, ["title", "status"]))
            
            # Test with missing key
            self.assertFalse(has_expected_frontmatter(temp_path, ["title", "status", "missing_key"]))
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_scan_requirements(self):
        """Test the scan_requirements function."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create ai-requirements directory and subdirectories
            os.makedirs(os.path.join(temp_dir, "ai-requirements/patterns"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "ai-requirements/examples"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "ai-requirements/prompts/discovery"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "ai-requirements/integrations"), exist_ok=True)
            
            # Create sample files
            pattern_file = os.path.join(temp_dir, "ai-requirements/patterns/goal-decomposition.md")
            example_file = os.path.join(temp_dir, "ai-requirements/examples/web-app-discovery.md")
            integration_file = os.path.join(temp_dir, "ai-requirements/integrations/cip-integration.md")
            
            # Write some content to files
            for file_path in [pattern_file, example_file, integration_file]:
                with open(file_path, 'w') as f:
                    f.write("# Test Content")
            
            # Change to the temporary directory to test
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Run the scan_requirements function
                requirements_info = scan_requirements()
                
                # Verify the results
                self.assertTrue(requirements_info['exists'])
                self.assertEqual(len(requirements_info['patterns']), 1)
                self.assertEqual(requirements_info['patterns'][0]['name'], 'goal-decomposition')
                self.assertEqual(len(requirements_info['examples']), 1)
                self.assertEqual(requirements_info['examples'][0]['name'], 'web-app-discovery')
                self.assertEqual(len(requirements_info['prompts']), 1)
                self.assertEqual(requirements_info['prompts'][0]['name'], 'discovery')
                self.assertEqual(len(requirements_info['integrations']), 1)
                self.assertEqual(requirements_info['integrations'][0]['name'], 'cip-integration')
            finally:
                # Change back to original directory
                os.chdir(original_dir)
        
        # Test when ai-requirements directory doesn't exist
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                requirements_info = scan_requirements()
                self.assertFalse(requirements_info['exists'])
                self.assertEqual(len(requirements_info['patterns']), 0)
                self.assertEqual(len(requirements_info['examples']), 0)
                self.assertEqual(len(requirements_info['prompts']), 0)
                self.assertEqual(len(requirements_info['integrations']), 0)
            finally:
                os.chdir(original_dir)

    def test_generate_next_steps(self):
        """Test the generate_next_steps function."""
        # Create test data
        git_info = {
            "modified_files": [{"status": "M", "path": "file1.txt"}],
            "untracked_files": ["file2.txt"],
        }
        
        cips_info = {
            "without_frontmatter": [{"id": "cip0001", "title": "Test CIP", "path": "cip/cip0001.md"}],
            "by_status": {
                "proposed": [{"id": "cip0001", "title": "Test CIP"}],
                "accepted": [{"id": "cip0002", "title": "Accepted CIP"}],
                "implemented": [{"id": "cip0003", "title": "Implemented CIP"}],
                "closed": [],
            },
        }
        
        backlog_info = {
            "without_frontmatter": [],
            "by_status": {
                "proposed": [],
                "ready": [],
                "in_progress": [{"title": "In Progress Item"}],
                "completed": [],
                "abandoned": [],
            },
            "by_priority": {
                "high": [{"title": "High Priority Item"}],
                "medium": [],
                "low": [],
            },
        }
        
        # Create a temporary directory with a mock ai-requirements structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create ai-requirements directory and pattern file
            os.makedirs(os.path.join(temp_dir, "ai-requirements/patterns"), exist_ok=True)
            pattern_file = os.path.join(temp_dir, "ai-requirements/patterns/goal-decomposition.md")
            with open(pattern_file, 'w') as f:
                f.write("# Test Content")
            
            # Change to the temporary directory
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Test generating next steps with requirements framework
                next_steps = generate_next_steps(git_info, cips_info, backlog_info)
                
                # Check requirements-related recommendations
                self.assertTrue(any("Start requirements gathering for proposed CIP" in step for step in next_steps))
                self.assertTrue(any("AI-Requirements framework" in step for step in next_steps))
                self.assertTrue(any("Implement accepted CIP" in step for step in next_steps))
                self.assertTrue(any("Verify implementation" in step for step in next_steps))
                self.assertTrue(any("Continue work on in-progress backlog item" in step for step in next_steps))
                self.assertTrue(any("Address high priority backlog item" in step for step in next_steps))
                self.assertTrue(any("Commit 2 pending changes" in step for step in next_steps))
                self.assertTrue(any("Add YAML frontmatter to 1 CIP files" in step for step in next_steps))
            finally:
                os.chdir(original_dir)
        
        # Test without ai-requirements directory
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Test generating next steps without requirements framework
                next_steps = generate_next_steps(git_info, cips_info, backlog_info)
                
                # Check that it recommends setting up requirements framework
                self.assertTrue(any("Set up AI-Requirements framework" in step for step in next_steps))
            finally:
                os.chdir(original_dir)


if __name__ == "__main__":
    unittest.main() 