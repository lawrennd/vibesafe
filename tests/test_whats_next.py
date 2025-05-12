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
                "accepted": [],
                "implemented": [],
                "closed": [],
            },
        }
        
        backlog_info = {
            "without_frontmatter": [],
            "by_status": {
                "proposed": [],
                "ready": [],
                "in_progress": [],
                "completed": [],
                "abandoned": [],
            },
            "by_priority": {
                "high": [],
                "medium": [],
                "low": [],
            },
        }
        
        # Test generating next steps
        next_steps = generate_next_steps(git_info, cips_info, backlog_info)
        
        # Check that it recommends adding frontmatter to CIPs
        self.assertTrue(any("Add YAML frontmatter to 1 CIP files" in step for step in next_steps))
        
        # Check that it recommends committing changes
        self.assertTrue(any("Commit 2 pending changes" in step for step in next_steps))


if __name__ == "__main__":
    unittest.main() 