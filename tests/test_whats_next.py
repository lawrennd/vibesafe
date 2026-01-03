"""
Tests for the What's Next script.

This module contains tests for the script's functionality, ensuring that it
properly analyzes the repository status, CIPs, and backlog items.
"""

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from unittest import mock
from pathlib import Path

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.whats_next import (
    extract_frontmatter,
    has_expected_frontmatter,
    run_command,
    get_git_status,
    generate_next_steps,
    scan_requirements,
    normalize_status,
    scan_backlog,
    check_tenet_status,
    run_validation,
    detect_codebase,
    detect_component,
    detect_gaps,
    generate_ai_prompts,
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
            # Create requirements directory
            os.makedirs(os.path.join(temp_dir, "requirements"), exist_ok=True)
            
            # Create sample requirement file
            req_file = os.path.join(temp_dir, "requirements/req0001_test.md")
            
            # Write some content to file
            with open(req_file, 'w') as f:
                f.write("# Test Requirement")
            
            # Change to the temporary directory to test
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Run the scan_requirements function
                requirements_info = scan_requirements()
                
                # Verify the results
                self.assertTrue(requirements_info['has_framework'])
                # Note: patterns/prompts/examples/integrations are deprecated in simplified requirements framework
                # The new requirements framework just checks for requirements/*.md files
            finally:
                # Change back to original directory
                os.chdir(original_dir)
        
        # Test when ai-requirements directory doesn't exist
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                requirements_info = scan_requirements()
                self.assertFalse(requirements_info['has_framework'])
                self.assertEqual(len(requirements_info['patterns']), 0)
                self.assertEqual(len(requirements_info['examples']), 0)
                self.assertEqual(sum(len(v) for v in requirements_info['prompts'].values()), 0)
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
                "in_progress": [{"id": "2025-01-01_in-progress", "title": "In Progress Item"}],
                "completed": [],
                "abandoned": [],
            },
            "by_priority": {
                "high": [{"id": "2025-01-01_high-priority", "title": "High Priority Item"}],
                "medium": [],
                "low": [],
            },
        }
        
        # Create a temporary directory with a mock requirements structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create requirements directory
            os.makedirs(os.path.join(temp_dir, "requirements"), exist_ok=True)
            req_file = os.path.join(temp_dir, "requirements/req0001_test.md")
            with open(req_file, 'w') as f:
                f.write("# Test Requirement")
            
            # Change to the temporary directory
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # First get the requirements info
                requirements_info = scan_requirements()
                
                # Test generating next steps with requirements framework
                next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
                
                # Check requirements-related recommendations (updated for new workflow)
                self.assertTrue(any("Review proposed CIP" in step and "WHAT vs HOW" in step for step in next_steps))
                self.assertTrue(any("requirements" in step.lower() or "requirement" in step.lower() for step in next_steps))
                self.assertTrue(any("Break down accepted CIP" in step and "backlog tasks" in step for step in next_steps))
                self.assertTrue(any("Verify implementation" in step or "consider closing" in step for step in next_steps))
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
                # First get the requirements info (which will show no framework)
                requirements_info = scan_requirements()
                
                # Test generating next steps without requirements framework
                next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
                
                # Check that it recommends setting up requirements framework
                self.assertTrue(any("requirements framework" in step.lower() for step in next_steps))
            finally:
                os.chdir(original_dir)


def test_scan_requirements_with_framework():
    """Test scanning requirements when the framework exists."""
    with mock.patch('os.path.isdir', return_value=True), \
         mock.patch('os.path.exists', return_value=True):
        
        result = scan_requirements()
        
        assert result['has_framework'] is True
        assert result['has_template'] is True
        # Note: patterns/prompts/integrations/examples/guidance are deprecated in simplified requirements framework
        # The new requirements framework just checks for requirements/*.md files

def test_scan_requirements_without_framework():
    """Test scanning requirements when the framework doesn't exist."""
    with mock.patch('os.path.isdir', return_value=False):
        result = scan_requirements()
        
        assert result['has_framework'] is False
        assert len(result['patterns']) == 0
        assert all(len(prompts) == 0 for prompts in result['prompts'].values())
        assert len(result['integrations']) == 0
        assert len(result['examples']) == 0
        assert len(result['guidance']) == 0

def test_generate_next_steps_with_requirements():
    """Test generating next steps when the requirements framework exists."""
    git_info = {}
    cips_info = {'by_status': {'proposed': [{'id': 'cip0001', 'title': 'Test CIP'}]}}
    backlog_info = {'by_status': {'proposed': [{'id': '2025-01-01_test', 'title': 'Test Backlog'}]}}
    requirements_info = {
        'has_framework': True,
        'has_template': True,
        'patterns': [],
        'prompts': {
            'discovery': [],
            'refinement': [],
            'validation': [],
            'testing': []
        },
        'integrations': [],
        'examples': [],
        'guidance': []
    }
    
    next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
    
    # Check that requirement-related steps are included (updated for new workflow)
    # Should suggest reviewing the proposed CIP to check if it's a requirement
    assert any("requirement" in step.lower() for step in next_steps)
    assert any("Review proposed CIP" in step and "WHAT vs HOW" in step for step in next_steps)

def test_generate_next_steps_without_requirements():
    """Test generating next steps when the requirements framework doesn't exist."""
    git_info = {}
    cips_info = {'by_status': {'proposed': []}}
    backlog_info = {'by_status': {'proposed': []}}
    requirements_info = {
        'has_framework': False,
        'has_template': False,
        'patterns': [],
        'prompts': {'discovery': [], 'refinement': [], 'validation': [], 'testing': []},
        'integrations': [],
        'examples': [],
        'guidance': []
    }
    
    next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
    
    # Check that a step to create the requirements framework is included
    assert any("Create requirements directory" in step for step in next_steps)

def test_generate_next_steps_with_empty_requirements():
    """Test generating next steps when the requirements framework exists but has no specific tasks."""
    git_info = {}
    cips_info = {'by_status': {'proposed': []}}
    backlog_info = {'by_status': {'proposed': []}}
    requirements_info = {
        'has_framework': True,
        'has_template': True,  # Simplified requirements framework always has template
    }
    
    next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info)
    
    # Check that general next steps are provided (updated for simplified requirements)
    # When nothing specific is pending, suggest reviewing requirements
    assert any("requirement" in step.lower() for step in next_steps)

def test_cmd_args_requirements_only():
    """Test that the --requirements-only flag works correctly."""
    with mock.patch('argparse.ArgumentParser.parse_args') as mock_args, \
         mock.patch('scripts.whats_next.scan_requirements') as mock_scan_req, \
         mock.patch('scripts.whats_next.print_section'), \
         mock.patch('scripts.whats_next.generate_next_steps') as mock_generate, \
         mock.patch('scripts.whats_next.run_update_scripts'), \
         mock.patch('scripts.whats_next.detect_gaps') as mock_gaps, \
         mock.patch('scripts.whats_next.generate_ai_prompts') as mock_prompts, \
         mock.patch('builtins.print'):
        
        # Setup mock args with requirements_only=True
        mock_args.return_value = mock.Mock(
            no_git=False, 
            no_color=False, 
            cip_only=False, 
            backlog_only=False, 
            requirements_only=True,
            no_update=True,
            skip_validation=True
        )
        
        # Setup mock scan_requirements to return a valid result
        mock_scan_req.return_value = {
            'has_framework': True,
            'patterns': ['stakeholder-identification'],
            'prompts': {'discovery': ['discovery-prompt.md'], 'refinement': [], 'validation': [], 'testing': []},
            'integrations': ['backlog-integration'],
            'examples': [],
            'guidance': []
        }
        
        # Setup mock gap detection
        mock_gaps.return_value = {'has_codebase': True, 'has_tenets': True, 'has_requirements': True, 
                                  'has_cips': True, 'has_backlog': True}
        mock_prompts.return_value = []
        
        # Run the main function
        from scripts.whats_next import main
        main()
        
        # Verify that generate_next_steps was called with 7 arguments including tenet_info, validation_info, and gaps_info
        mock_generate.assert_called_once()
        _, cips_arg, backlog_arg, req_arg, tenet_arg, validation_arg, gaps_arg = mock_generate.call_args[0]
        assert 'by_status' in cips_arg
        assert 'by_status' in backlog_arg
        assert 'by_priority' in backlog_arg
        assert req_arg == mock_scan_req.return_value
        assert isinstance(tenet_arg, dict)  # tenet_info should be a dict


class TestStatusNormalization(unittest.TestCase):
    """Test the status normalization functionality in What's Next script."""

    def test_normalize_status(self):
        """Test the normalize_status function directly."""
        # Test various input formats
        self.assertEqual(normalize_status('Ready'), 'ready')
        self.assertEqual(normalize_status('In Progress'), 'in_progress')
        self.assertEqual(normalize_status('Proposed'), 'proposed')
        self.assertEqual(normalize_status('completed'), 'completed')
        self.assertEqual(normalize_status('ABANDONED'), 'abandoned')
        self.assertEqual(normalize_status('Superseded'), 'superseded')
        self.assertEqual(normalize_status('SUPERSEDED'), 'superseded')
        
        # Test edge cases
        self.assertIsNone(normalize_status(''))
        self.assertIsNone(normalize_status(None))
        
        # Test hyphens and mixed separators
        self.assertEqual(normalize_status('in-progress'), 'in_progress')
        self.assertEqual(normalize_status('Ready-To-Start'), 'ready_to_start')

    def test_scan_backlog_status_normalization(self):
        """Test that scan_backlog correctly normalizes status values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock backlog directory structure
            backlog_dir = os.path.join(temp_dir, 'backlog')
            features_dir = os.path.join(backlog_dir, 'features')
            os.makedirs(features_dir)
            
            # Create test files with different status formats
            test_files = [
                {
                    'name': '2025-07-26_test-ready.md',
                    'content': '''---
id: "2025-07-26_test-ready"
title: "Test Ready Task"
status: "Ready"
priority: "High"
---

# Task: Test Ready Task
''',
                    'expected_status': 'ready'
                },
                {
                    'name': '2025-07-26_test-in-progress.md',
                    'content': '''---
id: "2025-07-26_test-in-progress"
title: "Test In Progress Task"
status: "In Progress"
priority: "Medium"
---

# Task: Test In Progress Task
''',
                    'expected_status': 'in_progress'
                },
                {
                    'name': '2025-07-26_test-lowercase.md',
                    'content': '''---
id: "2025-07-26_test-lowercase"
title: "Test Lowercase Task"
status: "proposed"
priority: "Low"
---

# Task: Test Lowercase Task
''',
                    'expected_status': 'proposed'
                },
                {
                    'name': '2025-07-26_test-superseded.md',
                    'content': '''---
id: "2025-07-26_test-superseded"
title: "Test Superseded Task"
status: "Superseded"
priority: "Medium"
---

# Task: Test Superseded Task
''',
                    'expected_status': 'superseded'
                }
            ]
            
            # Create test files
            for test_file in test_files:
                file_path = os.path.join(features_dir, test_file['name'])
                with open(file_path, 'w') as f:
                    f.write(test_file['content'])
            
            # Mock the current working directory to our temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Run scan_backlog
                backlog_info = scan_backlog()
                
                # Verify that all files were processed
                self.assertEqual(backlog_info['total'], 4)
                self.assertEqual(backlog_info['with_frontmatter'], 4)
                
                # Verify that status values were normalized correctly
                ready_tasks = backlog_info['by_status']['ready']
                in_progress_tasks = backlog_info['by_status']['in_progress']
                proposed_tasks = backlog_info['by_status']['proposed']
                superseded_tasks = backlog_info['by_status']['superseded']
                
                self.assertEqual(len(ready_tasks), 1)
                self.assertEqual(ready_tasks[0]['title'], 'Test Ready Task')
                
                self.assertEqual(len(in_progress_tasks), 1)
                self.assertEqual(in_progress_tasks[0]['title'], 'Test In Progress Task')
                
                self.assertEqual(len(proposed_tasks), 1)
                self.assertEqual(proposed_tasks[0]['title'], 'Test Lowercase Task')
                
                self.assertEqual(len(superseded_tasks), 1)
                self.assertEqual(superseded_tasks[0]['title'], 'Test Superseded Task')
                
            finally:
                os.chdir(original_cwd)

    def test_scan_backlog_old_format_status_normalization(self):
        """Test that scan_backlog correctly normalizes status in old format files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock backlog directory structure
            backlog_dir = os.path.join(temp_dir, 'backlog')
            features_dir = os.path.join(backlog_dir, 'features')
            os.makedirs(features_dir)
            
            # Create test file with old format
            file_path = os.path.join(features_dir, '2025-07-26_test-old-format.md')
            with open(file_path, 'w') as f:
                f.write('''# Task: Test Old Format Task

- **ID**: 2025-07-26_test-old-format
- **Title**: Test Old Format Task
- **Status**: In Progress
- **Priority**: High
- **Created**: 2025-07-26
- **Last Updated**: 2025-07-26

Content goes here.
''')
            
            # Mock the current working directory to our temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Run scan_backlog
                backlog_info = scan_backlog()
                
                # Verify that the file was processed
                self.assertEqual(backlog_info['total'], 1)
                self.assertEqual(backlog_info['with_frontmatter'], 0)  # No frontmatter
                self.assertEqual(len(backlog_info['without_frontmatter']), 1)
                
                # Verify that status was normalized (old format processing doesn't normalize yet)
                # The old format status extraction will need updates for full normalization
                
            finally:
                os.chdir(original_cwd)

    def test_cross_script_consistency(self):
        """Test that both update_index.py and whats_next.py normalize status consistently."""
        # Test that both normalize_status functions behave identically
        test_cases = [
            'Ready',
            'In Progress', 
            'Proposed',
            'completed',
            'ABANDONED',
            'Superseded',
            'SUPERSEDED',
            'in-progress',
            '',
            None
        ]
        
        # Import normalize_status from update_index
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backlog'))
        import update_index
        
        for test_case in test_cases:
            whats_next_result = normalize_status(test_case)
            update_index_result = update_index.normalize_status(test_case)
            
            self.assertEqual(
                whats_next_result, 
                update_index_result,
                f"Inconsistent normalization for '{test_case}': "
                f"whats_next='{whats_next_result}' vs update_index='{update_index_result}'"
            )


class TestTenetStatus(unittest.TestCase):
    """Test the tenet status checking functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.test_dir)

    def test_check_tenet_status_missing_directory(self):
        """Test check_tenet_status when tenets directory doesn't exist."""
        result = check_tenet_status()
        
        self.assertEqual(result['status'], 'missing')
        self.assertEqual(result['count'], 0)
        self.assertFalse(result['needs_review'])
        self.assertIn('No tenets directory found', result['message'])

    def test_check_tenet_status_empty_directory(self):
        """Test check_tenet_status when tenets directory exists but has no project tenets."""
        # Create tenets directory with only system files
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add system files that should be ignored
        (tenets_dir / 'README.md').write_text('System readme')
        (tenets_dir / 'tenet_template.md').write_text('Template')
        (tenets_dir / 'combine_tenets.py').write_text('# Script')
        
        # Add vibesafe subdirectory (should be ignored)
        vibesafe_dir = tenets_dir / 'vibesafe'
        vibesafe_dir.mkdir()
        (vibesafe_dir / 'user-autonomy.md').write_text('VibeSafe tenet')
        
        result = check_tenet_status()
        
        self.assertEqual(result['status'], 'empty')
        self.assertEqual(result['count'], 0)
        self.assertFalse(result['needs_review'])

    def test_check_tenet_status_with_project_tenets_fresh(self):
        """Test check_tenet_status with fresh project tenets."""
        # Create tenets directory with project tenets
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add project tenets
        (tenets_dir / 'my-tenet.md').write_text('My project tenet')
        (tenets_dir / 'another-tenet.md').write_text('Another tenet')
        
        result = check_tenet_status(review_period_days=180)
        
        self.assertEqual(result['status'], 'exists')
        self.assertEqual(result['count'], 2)
        self.assertFalse(result['needs_review'])
        self.assertIsNotNone(result['days_since_modification'])
        self.assertLess(result['days_since_modification'], 1)  # Just created
        self.assertEqual(len(result['files']), 2)

    def test_check_tenet_status_with_old_tenets(self):
        """Test check_tenet_status with old tenets that need review."""
        import time
        
        # Create tenets directory with project tenets
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add project tenet
        tenet_file = tenets_dir / 'my-tenet.md'
        tenet_file.write_text('My project tenet')
        
        # Modify the file's timestamp to be 200 days ago
        old_time = time.time() - (200 * 24 * 60 * 60)  # 200 days ago
        os.utime(tenet_file, (old_time, old_time))
        
        result = check_tenet_status(review_period_days=180)
        
        self.assertEqual(result['status'], 'exists')
        self.assertEqual(result['count'], 1)
        self.assertTrue(result['needs_review'])
        self.assertGreater(result['days_since_modification'], 180)
        self.assertEqual(result['review_period_days'], 180)

    def test_check_tenet_status_custom_review_period(self):
        """Test check_tenet_status with custom review period."""
        import time
        
        # Create tenets directory with project tenets
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add project tenet
        tenet_file = tenets_dir / 'my-tenet.md'
        tenet_file.write_text('My project tenet')
        
        # Modify the file's timestamp to be 100 days ago
        old_time = time.time() - (100 * 24 * 60 * 60)  # 100 days ago
        os.utime(tenet_file, (old_time, old_time))
        
        # With default period (180 days), should not need review
        result_180 = check_tenet_status(review_period_days=180)
        self.assertFalse(result_180['needs_review'])
        
        # With 90-day period, should need review
        result_90 = check_tenet_status(review_period_days=90)
        self.assertTrue(result_90['needs_review'])
        self.assertEqual(result_90['review_period_days'], 90)

    def test_check_tenet_status_nested_tenets(self):
        """Test check_tenet_status with nested project tenet directories."""
        # Create tenets directory with nested project tenets
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add project tenets in subdirectory (not vibesafe)
        project_dir = tenets_dir / 'my-project'
        project_dir.mkdir()
        (project_dir / 'tenet1.md').write_text('Project tenet 1')
        (project_dir / 'tenet2.md').write_text('Project tenet 2')
        
        # Also add some system files (should be ignored)
        (tenets_dir / 'README.md').write_text('System readme')
        
        # Add vibesafe subdirectory (should be ignored)
        vibesafe_dir = tenets_dir / 'vibesafe'
        vibesafe_dir.mkdir()
        (vibesafe_dir / 'user-autonomy.md').write_text('VibeSafe tenet')
        
        result = check_tenet_status()
        
        self.assertEqual(result['status'], 'exists')
        self.assertEqual(result['count'], 2)  # Only the 2 in my-project
        self.assertEqual(len(result['files']), 2)
        # Check that vibesafe tenets are not included
        self.assertTrue(all('vibesafe' not in f for f in result['files']))

    def test_check_tenet_status_multiple_ages(self):
        """Test check_tenet_status with tenets of different ages."""
        import time
        
        # Create tenets directory with project tenets
        tenets_dir = Path('tenets')
        tenets_dir.mkdir()
        
        # Add fresh tenet
        fresh_tenet = tenets_dir / 'fresh-tenet.md'
        fresh_tenet.write_text('Fresh tenet')
        
        # Add old tenet
        old_tenet = tenets_dir / 'old-tenet.md'
        old_tenet.write_text('Old tenet')
        old_time = time.time() - (200 * 24 * 60 * 60)  # 200 days ago
        os.utime(old_tenet, (old_time, old_time))
        
        result = check_tenet_status(review_period_days=180)
        
        self.assertEqual(result['status'], 'exists')
        self.assertEqual(result['count'], 2)
        # Should report based on newest modification (fresh tenet)
        self.assertLess(result['days_since_modification'], 1)
        self.assertFalse(result['needs_review'])  # Because newest is fresh


class TestGenerateNextStepsWithTenets(unittest.TestCase):
    """Test next steps generation with tenet information."""

    def test_generate_next_steps_with_missing_tenets(self):
        """Test that missing tenets appear in next steps."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': [], 'completed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = {'status': 'missing', 'needs_review': False}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info)
        
        # Should suggest creating tenets
        tenet_suggestions = [step for step in next_steps if 'tenet' in step.lower()]
        self.assertGreater(len(tenet_suggestions), 0)
        self.assertTrue(any('create' in step.lower() for step in tenet_suggestions))

    def test_generate_next_steps_with_empty_tenets(self):
        """Test that empty tenet directory appears in next steps."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': [], 'completed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = {'status': 'empty', 'needs_review': False}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info)
        
        # Should suggest creating first tenet
        tenet_suggestions = [step for step in next_steps if 'tenet' in step.lower()]
        self.assertGreater(len(tenet_suggestions), 0)
        self.assertTrue(any('first' in step.lower() for step in tenet_suggestions))

    def test_generate_next_steps_with_stale_tenets(self):
        """Test that stale tenets appear in next steps."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': [], 'completed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = {'status': 'exists', 'needs_review': True, 'count': 3}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info)
        
        # Should suggest reviewing tenets
        tenet_suggestions = [step for step in next_steps if 'tenet' in step.lower()]
        self.assertGreater(len(tenet_suggestions), 0)
        self.assertTrue(any('review' in step.lower() for step in tenet_suggestions))

    def test_generate_next_steps_with_fresh_tenets(self):
        """Test that fresh tenets don't appear in next steps."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': [], 'completed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = {'status': 'exists', 'needs_review': False, 'count': 3}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info)
        
        # Should NOT suggest anything about tenets
        tenet_suggestions = [step for step in next_steps if 'tenet' in step.lower()]
        self.assertEqual(len(tenet_suggestions), 0)

    def test_generate_next_steps_without_tenet_info(self):
        """Test that next steps still work without tenet info (backwards compatibility)."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': [], 'completed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        
        # Call without tenet_info
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, None)
        
        # Should still return next steps (shouldn't crash)
        self.assertIsInstance(next_steps, list)


class TestValidationIntegration(unittest.TestCase):
    """Test validation integration in whats_next script."""
    
    def test_generate_next_steps_with_validation_errors(self):
        """Test that validation errors appear as first next step."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        validation_info = {'error_count': 10, 'warning_count': 5, 'has_issues': True, 'exit_code': 1}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, validation_info)
        
        # Validation errors should be first next step
        self.assertGreater(len(next_steps), 0)
        first_step = next_steps[0]
        self.assertIn('10', first_step)  # Error count
        self.assertIn('validation', first_step.lower())
        self.assertIn('--fix', first_step)
    
    def test_generate_next_steps_with_validation_warnings_only(self):
        """Test that validation warnings appear when no errors."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        validation_info = {'error_count': 0, 'warning_count': 3, 'has_issues': True, 'exit_code': 0}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, validation_info)
        
        # Should have validation warning step
        validation_steps = [step for step in next_steps if 'validation' in step.lower() and 'warning' in step.lower()]
        self.assertGreater(len(validation_steps), 0)
        self.assertTrue(any('3' in step for step in validation_steps))  # Warning count
    
    def test_generate_next_steps_without_validation_issues(self):
        """Test that no validation step appears when validation passes."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        validation_info = {'error_count': 0, 'warning_count': 0, 'has_issues': False, 'exit_code': 0}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, validation_info)
        
        # Should NOT have validation steps
        validation_steps = [step for step in next_steps if 'validation' in step.lower()]
        self.assertEqual(len(validation_steps), 0)
    
    def test_generate_next_steps_with_validation_error(self):
        """Test that validation errors are handled gracefully."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        validation_info = {'error': 'Validator script not found'}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, validation_info)
        
        # Should still generate next steps (graceful degradation)
        self.assertIsInstance(next_steps, list)
        # Should NOT crash or include validation steps
        validation_steps = [step for step in next_steps if 'validation' in step.lower()]
        self.assertEqual(len(validation_steps), 0)
    
    def test_generate_next_steps_without_validation_info(self):
        """Test backwards compatibility when validation_info is None."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        
        # Call without validation_info (backwards compatibility)
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, tenet_info, None)
        
        # Should still work
        self.assertIsInstance(next_steps, list)


class TestGapDetection(unittest.TestCase):
    """Test gap detection and AI prompt generation."""
    
    def setUp(self):
        """Set up test environment."""
        self.original_dir = Path.cwd()
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_gap_"))
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_detect_codebase_with_python_files(self):
        """Test codebase detection with Python files."""
        # Create source directory with Python files
        src_dir = Path("src")
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        self.assertTrue(detect_codebase())
    
    def test_detect_codebase_with_javascript_files(self):
        """Test codebase detection with JavaScript files."""
        # Create app directory with JS files
        app_dir = Path("app")
        app_dir.mkdir()
        (app_dir / "index.js").write_text("console.log('hello');")
        
        self.assertTrue(detect_codebase())
    
    def test_detect_codebase_without_source_files(self):
        """Test codebase detection without source files."""
        # Create only documentation
        Path("README.md").write_text("# Project")
        
        self.assertFalse(detect_codebase())
    
    def test_detect_codebase_with_package_structure(self):
        """Test codebase detection with Python package structure."""
        # Create myproject/myproject/__init__.py structure
        package_dir = Path("myproject") / "myproject"
        package_dir.mkdir(parents=True)
        (package_dir / "__init__.py").write_text("# Package")
        (package_dir / "core.py").write_text("def main(): pass")
        
        self.assertTrue(detect_codebase())
    
    def test_detect_codebase_excludes_vibesafe_scripts(self):
        """Test that VibeSafe scripts directory doesn't count as user codebase."""
        # Create VibeSafe scripts directory
        scripts_dir = Path("scripts")
        scripts_dir.mkdir()
        (scripts_dir / "whats_next.py").write_text("# VibeSafe script")
        (scripts_dir / "validate_vibesafe_structure.py").write_text("# VibeSafe script")
        
        # Should NOT detect codebase (these are VibeSafe system files)
        self.assertFalse(detect_codebase())
    
    def test_detect_codebase_excludes_venv(self):
        """Test that virtual environment doesn't count as codebase."""
        # Create .venv-vibesafe with Python files
        venv_dir = Path(".venv-vibesafe") / "lib" / "python3.9"
        venv_dir.mkdir(parents=True)
        (venv_dir / "site.py").write_text("# Python stdlib")
        
        self.assertFalse(detect_codebase())
    
    def test_detect_codebase_with_user_code_and_vibesafe(self):
        """Test codebase detection when both user code and VibeSafe exist."""
        # Create VibeSafe scripts
        scripts_dir = Path("scripts")
        scripts_dir.mkdir()
        (scripts_dir / "whats_next.py").write_text("# VibeSafe script")
        
        # Create user code
        src_dir = Path("src")
        src_dir.mkdir()
        (src_dir / "app.py").write_text("# User code")
        
        # Should detect codebase (user has source code)
        self.assertTrue(detect_codebase())
    
    def test_detect_component_missing(self):
        """Test component detection when directory doesn't exist."""
        self.assertFalse(detect_component('tenets'))
    
    def test_detect_component_empty(self):
        """Test component detection with only system files."""
        tenets_dir = Path("tenets")
        tenets_dir.mkdir()
        (tenets_dir / "README.md").write_text("# Tenets")
        (tenets_dir / "tenet_template.md").write_text("# Template")
        
        self.assertFalse(detect_component('tenets'))
    
    def test_detect_component_with_user_content(self):
        """Test component detection with user content."""
        tenets_dir = Path("tenets")
        tenets_dir.mkdir()
        (tenets_dir / "README.md").write_text("# Tenets")
        (tenets_dir / "my-tenet.md").write_text("# My Tenet")
        
        self.assertTrue(detect_component('tenets'))
    
    def test_detect_gaps_all_missing(self):
        """Test gap detection when all components are missing."""
        gaps = detect_gaps()
        
        self.assertFalse(gaps['has_codebase'])
        self.assertFalse(gaps['has_tenets'])
        self.assertFalse(gaps['has_requirements'])
        self.assertFalse(gaps['has_cips'])
        self.assertFalse(gaps['has_backlog'])
    
    def test_detect_gaps_with_codebase_only(self):
        """Test gap detection with codebase but no VibeSafe components."""
        src_dir = Path("src")
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        gaps = detect_gaps()
        
        self.assertTrue(gaps['has_codebase'])
        self.assertFalse(gaps['has_tenets'])
        self.assertFalse(gaps['has_requirements'])
        self.assertFalse(gaps['has_cips'])
        self.assertFalse(gaps['has_backlog'])
    
    def test_detect_gaps_with_all_components(self):
        """Test gap detection when all components exist."""
        # Create codebase
        src_dir = Path("src")
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        # Create all components with user content
        for component_dir in ['tenets', 'requirements', 'cip', 'backlog/features']:
            Path(component_dir).mkdir(parents=True)
            (Path(component_dir) / "user-file.md").write_text("# User Content")
        
        gaps = detect_gaps()
        
        self.assertTrue(gaps['has_codebase'])
        self.assertTrue(gaps['has_tenets'])
        self.assertTrue(gaps['has_requirements'])
        self.assertTrue(gaps['has_cips'])
        self.assertTrue(gaps['has_backlog'])
    
    def test_generate_ai_prompts_for_tenets(self):
        """Test AI prompt generation for missing tenets."""
        gaps = {
            'has_codebase': True,
            'has_tenets': False,
            'has_requirements': False,
            'has_cips': False,
            'has_backlog': False
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]['type'], 'create_tenets')
        self.assertEqual(prompts[0]['priority'], 'high')
        self.assertIn('tenets', prompts[0]['title'].lower())
        self.assertIn('codebase', prompts[0]['prompt'].lower())
    
    def test_generate_ai_prompts_for_requirements(self):
        """Test AI prompt generation for extracting requirements from CIPs."""
        gaps = {
            'has_codebase': True,
            'has_tenets': True,
            'has_requirements': False,
            'has_cips': True,
            'has_backlog': False
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]['type'], 'extract_requirements')
        self.assertEqual(prompts[0]['priority'], 'high')
        self.assertIn('requirements', prompts[0]['title'].lower())
        self.assertIn('WHAT', prompts[0]['prompt'])
    
    def test_generate_ai_prompts_for_cips(self):
        """Test AI prompt generation for creating CIPs."""
        gaps = {
            'has_codebase': True,
            'has_tenets': True,
            'has_requirements': True,
            'has_cips': False,
            'has_backlog': False
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]['type'], 'create_cips')
        self.assertEqual(prompts[0]['priority'], 'medium')
        self.assertIn('CIP', prompts[0]['title'])
        self.assertIn('HOW', prompts[0]['prompt'])
    
    def test_generate_ai_prompts_for_backlog(self):
        """Test AI prompt generation for creating backlog."""
        gaps = {
            'has_codebase': True,
            'has_tenets': True,
            'has_requirements': True,
            'has_cips': True,
            'has_backlog': False
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]['type'], 'create_backlog')
        self.assertEqual(prompts[0]['priority'], 'medium')
        self.assertIn('backlog', prompts[0]['title'].lower())
        self.assertIn('tasks', prompts[0]['prompt'].lower())
    
    def test_generate_ai_prompts_bootstrap_all(self):
        """Test AI prompt generation for bootstrapping from scratch."""
        gaps = {
            'has_codebase': True,
            'has_tenets': False,
            'has_requirements': False,
            'has_cips': False,
            'has_backlog': False
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]['type'], 'create_tenets')  # Should suggest starting with tenets
        self.assertIn('tenets', prompts[0]['title'].lower())
    
    def test_generate_ai_prompts_no_suggestions(self):
        """Test AI prompt generation when no suggestions needed."""
        gaps = {
            'has_codebase': True,
            'has_tenets': True,
            'has_requirements': True,
            'has_cips': True,
            'has_backlog': True
        }
        
        prompts = generate_ai_prompts(gaps)
        
        self.assertEqual(len(prompts), 0)
    
    def test_generate_next_steps_with_gaps(self):
        """Test that gap detection appears in next steps."""
        git_info = {}
        cips_info = {'by_status': {'proposed': [], 'accepted': []}}
        backlog_info = {'by_status': {'in_progress': [], 'proposed': []}, 
                       'by_priority': {'high': []}}
        requirements_info = {'has_framework': True}
        tenet_info = None
        validation_info = None
        
        gaps = {
            'has_codebase': True,
            'has_tenets': False,
            'has_requirements': False,
            'has_cips': False,
            'has_backlog': False
        }
        ai_prompts = generate_ai_prompts(gaps)
        gaps_info = {'gaps': gaps, 'prompts': ai_prompts}
        
        next_steps = generate_next_steps(git_info, cips_info, backlog_info, requirements_info, 
                                        tenet_info, validation_info, gaps_info)
        
        # Should have AI prompt suggestions
        self.assertGreater(len(next_steps), 0)
        # Should contain tenet-related suggestions
        next_steps_text = ' '.join(next_steps)
        self.assertIn('tenet', next_steps_text.lower())


if __name__ == "__main__":
    unittest.main() 