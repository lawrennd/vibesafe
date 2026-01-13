#!/usr/bin/env python3
"""
Comprehensive tests for validate_vibesafe_structure.py

Tests validation logic, auto-fix functionality, and edge cases.
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

# Add repo root to path so we can import test_support
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load canonical template module under the legacy import name.
from test_support import load_module_from_path

load_module_from_path(
    "scripts.validate_vibesafe_structure",
    Path(__file__).resolve().parents[1]
    / "templates"
    / "scripts"
    / "validate_vibesafe_structure.py",
)

from scripts.validate_vibesafe_structure import (
    extract_frontmatter,
    write_frontmatter,
    auto_fix_frontmatter,
    validate_file_naming,
    validate_yaml_frontmatter,
    validate_cross_references,
    fix_reverse_links,
    ValidationResult,
    COMPONENT_SPECS,
)


class TestValidationResult(unittest.TestCase):
    """Test ValidationResult class."""
    
    def test_initialization(self):
        result = ValidationResult()
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(len(result.info), 0)
        self.assertEqual(len(result.fixes), 0)
    
    def test_add_error(self):
        result = ValidationResult()
        result.add_error("Test error", "/path/to/file.md")
        self.assertEqual(len(result.errors), 1)
        self.assertTrue(result.has_errors())
    
    def test_add_warning(self):
        result = ValidationResult()
        result.add_warning("Test warning")
        self.assertEqual(len(result.warnings), 1)
        self.assertTrue(result.has_warnings())
    
    def test_add_fix(self):
        result = ValidationResult()
        result.add_fix("Fixed something", "/path/to/file.md")
        self.assertEqual(len(result.fixes), 1)
        self.assertTrue(result.has_fixes())


class TestFileNaming(unittest.TestCase):
    """Test file naming validation."""
    
    def test_requirement_naming_valid(self):
        result = ValidationResult()
        self.assertTrue(validate_file_naming('requirement', 'req0001_test.md', result))
        self.assertFalse(result.has_errors())
    
    def test_requirement_naming_invalid(self):
        result = ValidationResult()
        self.assertFalse(validate_file_naming('requirement', 'REQ-001_test.md', result))
        self.assertTrue(result.has_errors())
    
    def test_cip_naming_valid(self):
        result = ValidationResult()
        self.assertTrue(validate_file_naming('cip', 'cip0011.md', result))
        self.assertTrue(validate_file_naming('cip', 'cip0011_component-management.md', result))
        self.assertFalse(result.has_errors())
    
    def test_cip_naming_invalid(self):
        result = ValidationResult()
        self.assertFalse(validate_file_naming('cip', 'CIP-0011.md', result))
        self.assertTrue(result.has_errors())
    
    def test_backlog_naming_valid(self):
        result = ValidationResult()
        self.assertTrue(validate_file_naming('backlog', '2026-01-03_test-task.md', result))
        self.assertFalse(result.has_errors())
    
    def test_backlog_naming_invalid(self):
        result = ValidationResult()
        self.assertFalse(validate_file_naming('backlog', '01-03-2026_test-task.md', result))
        self.assertTrue(result.has_errors())
    
    def test_tenet_naming_valid(self):
        result = ValidationResult()
        self.assertTrue(validate_file_naming('tenet', 'simplicity-of-use.md', result))
        self.assertFalse(result.has_errors())


class TestFrontmatterExtraction(unittest.TestCase):
    """Test YAML frontmatter extraction."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_extract_valid_frontmatter(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "Proposed"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        self.assertIsNotNone(frontmatter)
        self.assertEqual(frontmatter['id'], '0001')
        self.assertEqual(frontmatter['title'], 'Test')
    
    def test_extract_missing_frontmatter(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = "# Test Content\n\nNo frontmatter here."
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        self.assertIsNone(frontmatter)
    
    def test_extract_invalid_yaml(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001
title: "Test
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        self.assertIsNone(frontmatter)


class TestAutoFix(unittest.TestCase):
    """Test auto-fix functionality."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_fix_status_capitalization(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "proposed"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        # Test dry-run (should not modify file)
        auto_fix_frontmatter('requirement', test_file, frontmatter, result, dry_run=True)
        self.assertTrue(result.has_fixes())
        
        # Verify file wasn't modified
        new_frontmatter = extract_frontmatter(test_file)
        self.assertEqual(new_frontmatter['status'], 'proposed')
        
        # Test actual fix
        result2 = ValidationResult()
        auto_fix_frontmatter('requirement', test_file, frontmatter, result2, dry_run=False)
        self.assertTrue(result2.has_fixes())
        
        # Verify file was modified
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertEqual(fixed_frontmatter['status'], 'Proposed')
    
    def test_fix_priority_capitalization(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "high"
category: "features"
related_cips: []
owner: "Test Human"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        auto_fix_frontmatter('backlog', test_file, frontmatter, result, dry_run=False)
        
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertEqual(fixed_frontmatter['priority'], 'High')
    
    def test_add_missing_last_updated(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "Proposed"
created: "2026-01-03"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        auto_fix_frontmatter('requirement', test_file, frontmatter, result, dry_run=False)
        
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertIn('last_updated', fixed_frontmatter)
        self.assertEqual(fixed_frontmatter['last_updated'], '2026-01-03')
    
    def test_add_missing_category(self):
        test_file = os.path.join(self.temp_dir, 'features', 'test.md')
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: []
owner: "Test Human"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        auto_fix_frontmatter('backlog', test_file, frontmatter, result, dry_run=False)
        
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertEqual(fixed_frontmatter['category'], 'features')
    
    def test_add_missing_related_cips(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "High"
category: "features"
created: "2026-01-03"
last_updated: "2026-01-03"
owner: "Test Human"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        auto_fix_frontmatter('backlog', test_file, frontmatter, result, dry_run=False)
        
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertIn('related_cips', fixed_frontmatter)
        self.assertEqual(fixed_frontmatter['related_cips'], [])
    
    def test_add_missing_related_tenets(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
stakeholders: ["test"]
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        frontmatter = extract_frontmatter(test_file)
        result = ValidationResult()
        
        auto_fix_frontmatter('requirement', test_file, frontmatter, result, dry_run=False)
        
        fixed_frontmatter = extract_frontmatter(test_file)
        self.assertIn('related_tenets', fixed_frontmatter)
        self.assertEqual(fixed_frontmatter['related_tenets'], [])


class TestYAMLValidation(unittest.TestCase):
    """Test YAML frontmatter validation."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_missing_required_field(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        result = ValidationResult()
        validate_yaml_frontmatter('requirement', test_file, result)
        
        self.assertTrue(result.has_errors())
        # Should have errors for missing required fields
        error_messages = [msg for msg, _ in result.errors]
        self.assertTrue(any('status' in msg for msg in error_messages))
    
    def test_invalid_status_value(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "InvalidStatus"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: []
stakeholders: []
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        result = ValidationResult()
        validate_yaml_frontmatter('requirement', test_file, result)
        
        self.assertTrue(result.has_errors())
        error_messages = [msg for msg, _ in result.errors]
        self.assertTrue(any('Invalid status' in msg for msg in error_messages))
    
    def test_invalid_date_format(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "0001"
title: "Test"
status: "Proposed"
priority: "High"
created: "01/03/2026"
last_updated: "2026-01-03"
related_tenets: []
stakeholders: []
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        result = ValidationResult()
        validate_yaml_frontmatter('requirement', test_file, result)
        
        self.assertTrue(result.has_errors())
        error_messages = [msg for msg, _ in result.errors]
        self.assertTrue(any('Invalid date format' in msg for msg in error_messages))
    
    def test_backlog_related_requirements_requires_no_cip_reason(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "High"
category: "features"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: []
owner: "Test Human"
related_requirements: ["0001"]
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)
        
        result = ValidationResult()
        validate_yaml_frontmatter('backlog', test_file, result)
        
        self.assertTrue(result.has_errors())
        error_messages = [msg for msg, _ in result.errors]
        self.assertTrue(any("no_cip_reason" in msg for msg in error_messages))

    def test_backlog_related_requirements_valid_exception(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "High"
category: "features"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: []
owner: "Test Human"
related_requirements: ["0001"]
no_cip_reason: "Trivial bugfix: narrow change, no design decision needed"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)

        result = ValidationResult()
        validate_yaml_frontmatter('backlog', test_file, result)

        self.assertFalse(result.has_errors())

    def test_invalid_owner_multi_name(self):
        test_file = os.path.join(self.temp_dir, 'test.md')
        content = """---
id: "2026-01-03_test"
title: "Test"
status: "Proposed"
priority: "High"
category: "features"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: []
owner: "Alice and Bob"
---

# Test Content
"""
        with open(test_file, 'w') as f:
            f.write(content)

        result = ValidationResult()
        validate_yaml_frontmatter('backlog', test_file, result)

        self.assertTrue(result.has_errors())
        error_messages = [msg for msg, _ in result.errors]
        self.assertTrue(any("single primary accountable human" in msg for msg in error_messages))


class TestCrossReferences(unittest.TestCase):
    """Test cross-reference validation."""
    
    def test_valid_cross_reference(self):
        all_ids = {
            'requirement': {'0001', '0002'},
            'cip': {'0011'},
            'backlog': set(),
            'tenet': {'simplicity-of-use'}
        }
        
        frontmatter = {
            'id': '0001',
            'related_tenets': ['simplicity-of-use']
        }
        
        result = ValidationResult()
        validate_cross_references('requirement', '/fake/path.md', frontmatter, all_ids, result)
        
        self.assertFalse(result.has_warnings())
    
    def test_broken_cross_reference(self):
        all_ids = {
            'requirement': {'0001'},
            'cip': set(),
            'backlog': set(),
            'tenet': set()
        }
        
        frontmatter = {
            'id': '0001',
            'related_tenets': ['nonexistent-tenet']
        }
        
        result = ValidationResult()
        validate_cross_references('requirement', '/fake/path.md', frontmatter, all_ids, result)
        
        self.assertTrue(result.has_warnings())
        warning_messages = [msg for msg, _ in result.warnings]
        self.assertTrue(any('Broken reference' in msg for msg in warning_messages))


class TestComponentSpecs(unittest.TestCase):
    """Test component specifications are correctly defined."""
    
    def test_all_components_defined(self):
        self.assertIn('requirement', COMPONENT_SPECS)
        self.assertIn('cip', COMPONENT_SPECS)
        self.assertIn('backlog', COMPONENT_SPECS)
        self.assertIn('tenet', COMPONENT_SPECS)
    
    def test_required_fields_present(self):
        for component_type, spec in COMPONENT_SPECS.items():
            self.assertIn('dir', spec)
            self.assertIn('pattern', spec)
            self.assertIn('required_fields', spec)
            self.assertIn('links_to', spec)
            self.assertIn('should_not_have', spec)
    
    def test_bottom_up_linking(self):
        # Requirements link to tenets
        self.assertIn('related_tenets', COMPONENT_SPECS['requirement']['links_to'])
        
        # CIPs link to requirements
        self.assertIn('related_requirements', COMPONENT_SPECS['cip']['links_to'])
        
        # Backlog links to CIPs
        self.assertIn('related_cips', COMPONENT_SPECS['backlog']['links_to'])
        
        # Tenets don't link upward (foundation)
        self.assertEqual(COMPONENT_SPECS['tenet']['links_to'], [])


class TestReverseLinkFix(unittest.TestCase):
    """Test reverse link fixing functionality."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create component directories
        os.makedirs(os.path.join(self.temp_dir, 'requirements'))
        os.makedirs(os.path.join(self.temp_dir, 'cip'))
        os.makedirs(os.path.join(self.temp_dir, 'backlog', 'features'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'tenets'))
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_fix_requirement_to_cip_reverse_link(self):
        """Test fixing requirement → CIP reverse link (should be CIP → requirement)."""
        # Create requirement with reverse link (related_cips - wrong direction)
        req_file = os.path.join(self.temp_dir, 'requirements', 'req0001_test.md')
        req_content = """---
id: "0001"
title: "Test Requirement"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: ["0011"]
related_tenets: []
stakeholders: []
---

# Test Requirement
"""
        with open(req_file, 'w') as f:
            f.write(req_content)
        
        # Create CIP without link
        cip_file = os.path.join(self.temp_dir, 'cip', 'cip0011.md')
        cip_content = """---
id: "0011"
title: "Test CIP"
status: "Proposed"
created: "2026-01-03"
last_updated: "2026-01-03"
author: "Test Human"
---

# Test CIP
"""
        with open(cip_file, 'w') as f:
            f.write(cip_content)
        
        # Import fix_reverse_links
        from scripts.validate_vibesafe_structure import fix_reverse_links, ValidationResult
        
        # Fix reverse links
        result = ValidationResult()
        fixes = fix_reverse_links(self.temp_dir, result, dry_run=False)
        
        # Verify fix was applied
        self.assertGreater(fixes, 0)
        
        # Check requirement no longer has related_cips
        req_fm = extract_frontmatter(req_file)
        self.assertNotIn('related_cips', req_fm)
        
        # Check CIP now has related_requirements
        cip_fm = extract_frontmatter(cip_file)
        self.assertIn('related_requirements', cip_fm)
        self.assertIn('0001', cip_fm['related_requirements'])
    
    def test_fix_tenet_to_requirement_reverse_link(self):
        """Test fixing tenet → requirement reverse link (should be requirement → tenet)."""
        # Create tenet with reverse link
        tenet_file = os.path.join(self.temp_dir, 'tenets', 'test-tenet.md')
        tenet_content = """---
id: "test-tenet"
title: "Test Tenet"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
related_requirements: ["0001"]
---

# Test Tenet
"""
        with open(tenet_file, 'w') as f:
            f.write(tenet_content)
        
        # Create requirement without link
        req_file = os.path.join(self.temp_dir, 'requirements', 'req0001_test.md')
        req_content = """---
id: "0001"
title: "Test Requirement"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: []
stakeholders: []
---

# Test Requirement
"""
        with open(req_file, 'w') as f:
            f.write(req_content)
        
        from scripts.validate_vibesafe_structure import fix_reverse_links, ValidationResult
        
        result = ValidationResult()
        fixes = fix_reverse_links(self.temp_dir, result, dry_run=False)
        
        self.assertGreater(fixes, 0)
        
        # Check tenet no longer has related_requirements
        tenet_fm = extract_frontmatter(tenet_file)
        self.assertNotIn('related_requirements', tenet_fm)
        
        # Check requirement now has related_tenets
        req_fm = extract_frontmatter(req_file)
        self.assertIn('test-tenet', req_fm['related_tenets'])
    
    def test_dry_run_doesnt_modify_files(self):
        """Test that dry-run doesn't actually modify files."""
        req_file = os.path.join(self.temp_dir, 'requirements', 'req0001_test.md')
        req_content = """---
id: "0001"
title: "Test Requirement"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_cips: ["0011"]
related_tenets: []
stakeholders: []
---

# Test Requirement
"""
        with open(req_file, 'w') as f:
            f.write(req_content)
        
        cip_file = os.path.join(self.temp_dir, 'cip', 'cip0011.md')
        cip_content = """---
id: "0011"
title: "Test CIP"
status: "Proposed"
created: "2026-01-03"
last_updated: "2026-01-03"
author: "Test Human"
---

# Test CIP
"""
        with open(cip_file, 'w') as f:
            f.write(cip_content)
        
        from scripts.validate_vibesafe_structure import fix_reverse_links, ValidationResult
        
        result = ValidationResult()
        fix_reverse_links(self.temp_dir, result, dry_run=True)
        
        # Verify files weren't modified
        req_fm = extract_frontmatter(req_file)
        self.assertIn('related_cips', req_fm)
        
        cip_fm = extract_frontmatter(cip_file)
        self.assertNotIn('related_requirements', cip_fm)


if __name__ == '__main__':
    unittest.main()

