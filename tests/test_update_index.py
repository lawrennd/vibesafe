#!/usr/bin/env python3
"""
Tests for the backlog/update_index.py script
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load canonical template module under the legacy import name, then import it.
from test_support import load_module_from_path

load_module_from_path(
    "backlog.update_index",
    Path(__file__).resolve().parents[1] / "templates" / "backlog" / "update_index.py",
)

import backlog.update_index as update_index  # pyright: ignore[reportMissingImports]

class TestUpdateIndex(unittest.TestCase):
    """Tests for the backlog/update_index.py script."""

    def setUp(self):
        """Set up temporary test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create a mock backlog structure
        for category in update_index.CATEGORIES:
            os.makedirs(os.path.join(self.test_dir, category), exist_ok=True)
    
    def tearDown(self):
        """Clean up temporary test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_normalize_status(self):
        """Test the normalize_status function directly."""
        # Test various input formats
        self.assertEqual(update_index.normalize_status('Ready'), 'ready')
        self.assertEqual(update_index.normalize_status('In Progress'), 'in_progress')
        self.assertEqual(update_index.normalize_status('Proposed'), 'proposed')
        self.assertEqual(update_index.normalize_status('completed'), 'completed')
        self.assertEqual(update_index.normalize_status('ABANDONED'), 'abandoned')
        self.assertEqual(update_index.normalize_status('Superseded'), 'superseded')
        self.assertEqual(update_index.normalize_status('SUPERSEDED'), 'superseded')
        
        # Test edge cases
        self.assertIsNone(update_index.normalize_status(''))
        self.assertIsNone(update_index.normalize_status(None))
        
        # Test hyphens and mixed separators
        self.assertEqual(update_index.normalize_status('in-progress'), 'in_progress')
        self.assertEqual(update_index.normalize_status('Ready-To-Start'), 'ready_to_start')
    
    def test_extract_yaml_frontmatter(self):
        """Test extraction of YAML frontmatter from task content."""
        # Create a test file with valid YAML frontmatter
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")
        
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"
title: "Test Task"
status: "Ready"
priority: "high"
---

# Task: Test Task

Content goes here.
""")
        
        # Extract metadata
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        
        # Check metadata - status should be normalized
        self.assertEqual(metadata['id'], '2025-05-12_test-task')
        self.assertEqual(metadata['title'], 'Test Task')
        self.assertEqual(metadata['status'], 'ready')  # normalized from 'Ready'
        self.assertEqual(metadata['priority'], 'high')
        
        # Test without frontmatter - should now work, not raise ValueError
        with open(test_file_path, 'w') as f:
            f.write("""# Task: Test Task

Content goes here.
""")
        
        # Should work now (no longer raises ValueError)
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['title'], 'Test Task')
    
    def test_extract_task_metadata_yaml_frontmatter(self):
        """Test extraction of task metadata from files with YAML frontmatter."""
        # Create a test file with YAML frontmatter
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")
        
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"
title: "Test Task with YAML"
status: "Ready"
priority: "high"
created: "2025-05-12"
last_updated: "2025-05-13"
---

# Task: Test Task with YAML

Content goes here.
""")
        
        # Extract metadata
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        
        # Check metadata - status should be normalized
        self.assertEqual(metadata['id'], '2025-05-12_test-task')
        self.assertEqual(metadata['title'], 'Test Task with YAML')
        self.assertEqual(metadata['status'], 'ready')  # normalized from 'Ready'
        self.assertEqual(metadata['priority'], 'high')
        self.assertEqual(metadata['created'], '2025-05-12')
        self.assertEqual(metadata['updated'], '2025-05-13')
        self.assertEqual(metadata['category'], category)
    
    def test_extract_task_metadata_traditional(self):
        """Test extraction of task metadata from files with traditional format (should work now)."""
        # Create a test file with traditional format
        category = "infrastructure"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")

        with open(test_file_path, 'w') as f:
            f.write("""# Task: Test Task Traditional

- **ID**: 2025-05-12_test-task
- **Title**: Test Task Traditional
- **Status**: In Progress
- **Priority**: Medium
- **Created**: 2025-05-12
- **Last Updated**: 2025-05-13

Content goes here.
""")
        
        # Extract metadata should work now (no longer raises ValueError)
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertIsNotNone(metadata)
        
        # Check that old format parsing works
        self.assertEqual(metadata['id'], '2025-05-12_test-task')
        self.assertEqual(metadata['title'], 'Test Task Traditional')
        self.assertEqual(metadata['status'], 'in_progress')  # normalized from 'In Progress'
        self.assertEqual(metadata['priority'], 'Medium')
        self.assertEqual(metadata['created'], '2025-05-12')
        self.assertEqual(metadata['updated'], '2025-05-13')
    
    def test_extract_task_metadata_both_formats(self):
        """Test extraction of task metadata from files with both YAML frontmatter and traditional format."""
        # Create a test file with both formats
        category = "documentation"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")
        
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"
title: "Test Task YAML"
status: "Ready"
priority: "High"
created: "2025-05-12"
last_updated: "2025-05-13"
---

# Task: Test Task Traditional

- **ID**: 2025-05-12_test-task-different
- **Title**: Test Task Traditional
- **Status**: In Progress
- **Priority**: Medium
- **Created**: 2025-05-14
- **Last Updated**: 2025-05-15

Content goes here.
""")
        
        # Extract metadata
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        
        # Check that YAML frontmatter takes precedence
        self.assertEqual(metadata['id'], '2025-05-12_test-task')
        self.assertEqual(metadata['title'], 'Test Task YAML')
        self.assertEqual(metadata['status'], 'ready')  # normalized from 'Ready'
        self.assertEqual(metadata['priority'], 'High')
        self.assertEqual(metadata['created'], '2025-05-12')
        self.assertEqual(metadata['updated'], '2025-05-13')
        self.assertEqual(metadata['category'], category)
    
    def test_extract_task_metadata_updated_field_variants(self):
        """Test that both 'updated' and 'last_updated' field names work."""
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")
        
        # Test with 'updated' field
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"
title: "Test Task"
status: "Ready"
updated: "2025-05-13"
---

# Task: Test Task
""")
        
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertEqual(metadata['updated'], '2025-05-13')
        
        # Test with 'last_updated' field (should also work)
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"  
title: "Test Task"
status: "Ready"
last_updated: "2025-05-14"
---

# Task: Test Task
""")
        
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertEqual(metadata['updated'], '2025-05-14')

    def test_extract_task_metadata_filename_alt_pattern_yyyymmdd_dash(self):
        """Covers YYYYMMDD-description.md naming convention."""
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "20250512-test-task.md")

        with open(test_file_path, "w") as f:
            f.write(
                """---
title: "Alt Pattern Task"
status: "Ready"
priority: "high"
---

# Task: Alt Pattern Task
"""
            )

        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["id"], "20250512-test-task")  # from filename

    def test_extract_task_metadata_falls_back_to_traditional_id_when_missing(self):
        """Covers fallback parsing of **ID** when YAML has no id and filename doesn't match."""
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "task.md")  # doesn't match either pattern

        with open(test_file_path, "w") as f:
            f.write(
                """---
title: "No ID In YAML"
status: "Ready"
priority: "high"
---

# Task: No ID In YAML

- **ID**: fallback-id-123
"""
            )

        metadata = update_index.extract_task_metadata(Path(test_file_path))
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["id"], "fallback-id-123")

    def test_extract_task_metadata_missing_file_returns_none(self):
        missing = Path(self.test_dir) / "features" / "does-not-exist.md"
        metadata = update_index.extract_task_metadata(missing)
        self.assertIsNone(metadata)

    def test_find_all_task_files_and_update_index_writes_index(self):
        """Covers scanning categories and writing index.md."""
        # Point the module's __file__ at our temp dir so Path(__file__).parent == self.test_dir
        old_file = getattr(update_index, "__file__", None)
        update_index.__file__ = os.path.join(self.test_dir, "update_index.py")
        try:
            # Create a couple of task files, plus excluded files.
            with open(os.path.join(self.test_dir, "features", "README.md"), "w") as f:
                f.write("ignored")
            with open(os.path.join(self.test_dir, "features", "index.md"), "w") as f:
                f.write("ignored")
            with open(os.path.join(self.test_dir, "features", "_ignored.md"), "w") as f:
                f.write("ignored")

            task_path = os.path.join(self.test_dir, "features", "2026-01-01_test.md")
            with open(task_path, "w") as f:
                f.write(
                    """---
id: "2026-01-01_test"
title: "Index Write Task"
status: "Ready"
priority: "High"
created: "2026-01-01"
last_updated: "2026-01-01"
---

# Task: Index Write Task
"""
                )

            # Ensure scan finds the task.
            task_files = update_index.find_all_task_files()
            self.assertEqual(len(task_files), 1)
            self.assertEqual(task_files[0].name, "2026-01-01_test.md")

            # Ensure update_index writes an index file in the temp backlog dir.
            update_index.update_index()
            index_path = Path(self.test_dir) / "index.md"
            self.assertTrue(index_path.exists())
            index_text = index_path.read_text(encoding="utf-8")
            self.assertIn("Lynguine Backlog Index", index_text)
            self.assertIn("Index Write Task", index_text)
        finally:
            if old_file is not None:
                update_index.__file__ = old_file

    def test_generate_index_content_with_no_completed_or_abandoned(self):
        """Covers 'no recently completed/abandoned' branches + invalid task skipping."""
        tasks = [
            None,
            {"category": None, "status": "ready"},
            {
                "filepath": Path(os.path.join(self.test_dir, "features", "2026-01-01_task.md")),
                "id": "2026-01-01_task",
                "title": "Only Ready Task",
                "status": "ready",
                "priority": "High",
                "created": "2026-01-01",
                "updated": "2026-01-01",
                "category": "features",
            },
            {
                # invalid status should be skipped
                "filepath": Path(os.path.join(self.test_dir, "features", "2026-01-02_task.md")),
                "id": "2026-01-02_task",
                "title": "Bad Status Task",
                "status": "not_a_status",
                "priority": "High",
                "created": "2026-01-02",
                "updated": "2026-01-02",
                "category": "features",
            },
        ]

        content = update_index.generate_index_content(tasks)
        self.assertIn("*No tasks recently completed.*", content)
        self.assertIn("*No tasks recently abandoned.*", content)
    
    def test_generate_index_content(self):
        """Test generating index content from task metadata."""
        # Create mock task metadata
        tasks = [
            {
                'filepath': Path(os.path.join(self.test_dir, "features", "2025-05-12_task1.md")),
                'id': '2025-05-12_task1',
                'title': 'Feature Task 1',
                'status': 'ready',  # use normalized status
                'priority': 'High',
                'created': '2025-05-12',
                'updated': '2025-05-13',
                'category': 'features'
            },
            {
                'filepath': Path(os.path.join(self.test_dir, "features", "2025-05-13_task2.md")),
                'id': '2025-05-13_task2',
                'title': 'Feature Task 2',
                'status': 'in_progress',  # use normalized status
                'priority': 'Medium',
                'created': '2025-05-13',
                'updated': '2025-05-14',
                'category': 'features'
            },
            {
                'filepath': Path(os.path.join(self.test_dir, "infrastructure", "2025-05-14_task3.md")),
                'id': '2025-05-14_task3',
                'title': 'Infrastructure Task',
                'status': 'completed',  # use normalized status
                'priority': 'Low',
                'created': '2025-05-14',
                'updated': '2025-05-15',
                'category': 'infrastructure'
            },
            {
                'filepath': Path(os.path.join(self.test_dir, "documentation", "2025-05-15_task4.md")),
                'id': '2025-05-15_task4',
                'title': 'Documentation Task',
                'status': 'abandoned',  # use normalized status
                'priority': 'Medium',
                'created': '2025-05-15',
                'updated': '2025-05-16',
                'category': 'documentation'
            },
            {
                'filepath': Path(os.path.join(self.test_dir, "features", "2025-05-16_task5.md")),
                'id': '2025-05-16_task5',
                'title': 'Superseded Feature Task',
                'status': 'superseded',  # use normalized status
                'priority': 'High',
                'created': '2025-05-16',
                'updated': '2025-05-17',
                'category': 'features'
            }
        ]

        content = update_index.generate_index_content(tasks)

        # Basic structure
        self.assertIn("# Lynguine Backlog Index", content)
        self.assertIn("## Features", content)
        self.assertIn("### Ready", content)
        self.assertIn("### In Progress", content)
        self.assertIn("### Proposed", content)
        self.assertIn("## Recently Completed Tasks", content)
        self.assertIn("## Recently Abandoned Tasks", content)

        # Verify links are rendered with relpaths from the template module directory
        base_dir = Path(update_index.__file__).parent
        expected_link_1 = os.path.relpath(tasks[0]["filepath"], base_dir)
        expected_link_2 = os.path.relpath(tasks[1]["filepath"], base_dir)
        expected_link_3 = os.path.relpath(tasks[2]["filepath"], base_dir)
        expected_link_4 = os.path.relpath(tasks[3]["filepath"], base_dir)

        self.assertIn(f"- [{tasks[0]['title']}]({expected_link_1})", content)
        self.assertIn(f"- [{tasks[1]['title']}]({expected_link_2})", content)
        self.assertIn(f"- [{tasks[2]['title']}]({expected_link_3})", content)  # completed section
        self.assertIn(f"- [{tasks[3]['title']}]({expected_link_4})", content)  # abandoned section
    
    def test_case_insensitive_status_matching(self):
        """Test that status values are normalized correctly."""
        # Create a test file with lowercase status
        category = "bugs"
        test_file_path = os.path.join(self.test_dir, category, "2025-05-12_test-task.md")
        
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-05-12_test-task"
title: "Test Task"
status: "ready"
priority: "high"
---

# Task: Test Task

Content goes here.
""")
        
        # Extract metadata
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        
        # Check metadata
        self.assertEqual(metadata['status'], 'ready')  # Should remain as normalized lowercase
        
        # Test that different case inputs normalize correctly
        tasks = [metadata]
        
        # Create a minimal version of generate_index_content for testing status matching
        def test_status_matching(tasks):
            categorized_tasks = {}
            for category in update_index.CATEGORIES:
                categorized_tasks[category] = {}
                for status in update_index.STATUSES:
                    categorized_tasks[category][status] = []
            
            for task in tasks:
                if task is None or 'category' not in task or task['category'] is None or 'status' not in task or task['status'] is None:
                    continue
                
                category = task['category']
                status = update_index.normalize_status(task['status'])  # normalize status
                
                if status and category in categorized_tasks and status in categorized_tasks[category]:
                    categorized_tasks[category][status].append(task)
            
            return categorized_tasks
        
        categorized = test_status_matching(tasks)
        
        # Check that the task was categorized correctly with normalized status
        self.assertEqual(len(categorized['bugs']['ready']), 1)
        self.assertEqual(categorized['bugs']['ready'][0]['id'], '2025-05-12_test-task')

    def test_superseded_status_handling(self):
        """Test that superseded status is handled correctly."""
        # Create a test file with superseded status
        category = "features"
        test_file_path = os.path.join(self.test_dir, category, "2025-07-26_superseded-task.md")
        
        with open(test_file_path, 'w') as f:
            f.write("""---
id: "2025-07-26_superseded-task"
title: "Superseded Task"
status: "Superseded"
priority: "medium"
created: "2025-07-26"
last_updated: "2025-07-26"
---

# Task: Superseded Task

This task has been superseded by a newer approach.
""")
        
        # Extract metadata
        metadata = update_index.extract_task_metadata(Path(test_file_path))
        
        # Check that metadata was extracted correctly
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['status'], 'superseded')  # should be normalized
        self.assertEqual(metadata['title'], 'Superseded Task')
        
        # Test that superseded is in valid statuses
        self.assertIn('superseded', update_index.STATUSES)
        
        # Test categorization
        tasks = [metadata]
        categorized_tasks = {}
        for cat in update_index.CATEGORIES:
            categorized_tasks[cat] = {}
            for status in update_index.STATUSES:
                categorized_tasks[cat][status] = []
        
        for task in tasks:
            if task and 'category' in task and 'status' in task:
                cat = task['category']
                status = update_index.normalize_status(task['status'])
                if status and cat in categorized_tasks and status in categorized_tasks[cat]:
                    categorized_tasks[cat][status].append(task)
        
        # Verify superseded task is categorized correctly
        self.assertEqual(len(categorized_tasks['features']['superseded']), 1)
        self.assertEqual(categorized_tasks['features']['superseded'][0]['id'], '2025-07-26_superseded-task')


if __name__ == '__main__':
    unittest.main() 