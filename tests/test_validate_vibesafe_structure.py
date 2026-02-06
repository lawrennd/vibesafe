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
import io
from contextlib import redirect_stdout
from unittest import mock
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

from scripts.validate_vibesafe_structure import (  # pyright: ignore[reportMissingImports]
    extract_frontmatter,
    write_frontmatter,
    auto_fix_frontmatter,
    validate_file_naming,
    validate_yaml_frontmatter,
    validate_cross_references,
    check_system_file_drift,
    validate_human_attribution,
    check_governance_drift,
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
        
        result = ValidationResult()
        fix_reverse_links(self.temp_dir, result, dry_run=True)
        
        # Verify files weren't modified
        req_fm = extract_frontmatter(req_file)
        self.assertIn('related_cips', req_fm)
        
        cip_fm = extract_frontmatter(cip_file)
        self.assertNotIn('related_requirements', cip_fm)


class TestHumanAttribution(unittest.TestCase):
    """Tests for REQ-0010 attribution validation."""

    def test_rejects_non_string(self):
        result = ValidationResult()
        validate_human_attribution("cip", "cip/cip0001.md", "author", None, result)
        self.assertTrue(result.has_errors())

    def test_rejects_ai_and_placeholders(self):
        bad_values = [
            "AI",
            "assistant",
            "Unknown",
            "N/A",
            "[Author Name]",
            "Your Name Here",
            "OpenAI",
        ]
        for v in bad_values:
            result = ValidationResult()
            validate_human_attribution("cip", "cip/cip0001.md", "author", v, result)
            self.assertTrue(result.has_errors(), msg=f"Expected error for value: {v}")

    def test_rejects_multiple_owners(self):
        result = ValidationResult()
        validate_human_attribution("backlog", "backlog/features/x.md", "owner", "Alice, Bob", result)
        self.assertTrue(result.has_errors())

    def test_accepts_single_human_name(self):
        result = ValidationResult()
        validate_human_attribution("cip", "cip/cip0001.md", "author", "Neil Lawrence", result)
        self.assertFalse(result.has_errors())


class TestYamlFrontmatterValidationAdditional(unittest.TestCase):
    """Extra tests to cover value validation and backlog exception paths."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def _write(self, rel_path: str, content: str) -> str:
        path = os.path.join(self.temp_dir, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_autofix_backlog_capitalizes_and_adds_fields(self):
        backlog_file = self._write(
            "backlog/features/2026-01-01_test.md",
            """---
id: "2026-01-01_test"
title: "Test Task"
status: "ready"
priority: "high"
created: "2026-01-01"
owner: "Neil Lawrence"
---

# Task: Test Task
""",
        )

        result = ValidationResult()
        fm = validate_yaml_frontmatter("backlog", backlog_file, result, auto_fix=True, dry_run=False)

        # Should be fixed in-file, and re-read should reflect fixes.
        self.assertIsNotNone(fm)
        self.assertEqual(fm.get("status"), "Ready")
        self.assertEqual(fm.get("priority"), "High")
        self.assertEqual(fm.get("category"), "features")
        self.assertEqual(fm.get("related_cips"), [])
        self.assertEqual(fm.get("last_updated"), "2026-01-01")
        self.assertTrue(result.has_fixes())

    def test_invalid_status_priority_and_date_format(self):
        req_file = self._write(
            "requirements/req0001_test.md",
            """---
id: "0001"
title: "Test Requirement"
status: "BadStatus"
priority: "Urgent"
created: "20260101"
last_updated: "2026-01-01"
related_tenets: []
stakeholders: []
related_cips: ["0011"]
---

# Test Requirement
""",
        )

        result = ValidationResult()
        validate_yaml_frontmatter("requirement", req_file, result, auto_fix=False, dry_run=False)

        self.assertTrue(result.has_errors())
        errors = "\n".join(msg for msg, _p in result.errors)
        self.assertIn("Invalid status", errors)
        self.assertIn("Invalid priority", errors)
        self.assertIn("Invalid date format", errors)

        self.assertTrue(result.has_warnings())
        warnings = "\n".join(msg for msg, _p in result.warnings)
        self.assertIn("Violates bottom-up pattern", warnings)

    def test_backlog_related_requirements_exception_validation(self):
        backlog_file = self._write(
            "backlog/features/2026-01-02_test.md",
            """---
id: "2026-01-02_test"
title: "Test Task"
status: "Ready"
priority: "High"
created: "2026-01-02"
last_updated: "2026-01-02"
category: "features"
owner: "Neil Lawrence"
related_requirements: ["0001"]
related_cips: ["0011"]
---

# Task: Test Task
""",
        )

        result = ValidationResult()
        validate_yaml_frontmatter("backlog", backlog_file, result, auto_fix=False, dry_run=False)

        # related_requirements exception violated because related_cips is non-empty and no_cip_reason missing
        self.assertTrue(result.has_errors())
        errors = "\n".join(msg for msg, _p in result.errors)
        self.assertIn("Invalid exception", errors)

class TestGovernanceDriftWarnings(unittest.TestCase):
    """Tests for git-based governance drift warnings."""

    def test_warns_when_impl_changed_without_planning(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        # Simulate changes to implementation without CIP/backlog updates
        with unittest.mock.patch.object(
            v, "_get_git_changed_paths", return_value=["templates/scripts/whats_next.py"]
        ):
            check_governance_drift("/tmp", result)

        self.assertTrue(result.has_warnings())
        messages = [m for m, _p in result.warnings]
        self.assertTrue(any("Governance drift" in m for m in messages))

    def test_warns_when_requirements_and_impl_changed_without_planning(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        with unittest.mock.patch.object(
            v,
            "_get_git_changed_paths",
            return_value=["requirements/req0001_x.md", "templates/scripts/whats_next.py"],
        ):
            check_governance_drift("/tmp", result)

        messages = [m for m, _p in result.warnings]
        self.assertTrue(any("Traceability gap" in m for m in messages))

class TestSystemFileDrift(unittest.TestCase):
    """Tests for template/runtime drift detection (VibeSafe repo / dogfood installs)."""

    def _write(self, root: str, rel: str, content: str) -> str:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _touch(self, path: str, mtime: float) -> None:
        os.utime(path, (mtime, mtime))

    def _write_all_templates(self, root: str) -> None:
        # The drift check iterates a fixed set of pairs; create all template sources.
        self._write(root, "templates/scripts/whats_next.py", "# template whats-next\n")
        self._write(root, "templates/scripts/validate_vibesafe_structure.py", "# template validator\n")
        self._write(root, "templates/backlog/update_index.py", "# template backlog index\n")
        self._write(root, "templates/tenets/combine_tenets.py", "# template tenets combiner\n")

    def test_skips_when_no_templates_dir(self):
        """Downstream projects won't have templates/, so drift check should skip."""
        with tempfile.TemporaryDirectory() as tmp:
            result = ValidationResult()
            check_system_file_drift(tmp, result)
            self.assertFalse(result.has_errors())
            self.assertFalse(result.has_warnings())

    def test_no_error_when_templates_exist_but_runtime_missing(self):
        """Runtime copies may be absent; templates are canonical and should still validate."""
        with tempfile.TemporaryDirectory() as tmp:
            self._write_all_templates(tmp)

            result = ValidationResult()
            check_system_file_drift(tmp, result)
            self.assertFalse(result.has_errors())

    def test_runtime_ahead_of_templates_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Canonical template files
            self._write_all_templates(tmp)
            template_path = os.path.join(tmp, "templates/scripts/whats_next.py")
            self._write(tmp, "templates/scripts/whats_next.py", "print('template')\n")

            # Runtime copy exists + differs
            runtime_path = self._write(tmp, "scripts/whats_next.py", "print('runtime edited')\n")

            # Make runtime newer than template
            self._touch(template_path, 10.0)
            self._touch(runtime_path, 20.0)

            result = ValidationResult()
            check_system_file_drift(tmp, result)

            self.assertTrue(result.has_errors())
            combined = "\n".join(msg for msg, _path in result.errors)
            self.assertIn("runtime AHEAD of templates", combined)
            self.assertIn("scripts/whats_next.py", combined)

    def test_runtime_differs_but_not_ahead_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_all_templates(tmp)
            template_path = os.path.join(tmp, "templates/scripts/whats_next.py")
            self._write(tmp, "templates/scripts/whats_next.py", "print('template')\n")

            runtime_path = self._write(tmp, "scripts/whats_next.py", "print('runtime stale')\n")

            # Make runtime older than template
            self._touch(template_path, 20.0)
            self._touch(runtime_path, 10.0)

            result = ValidationResult()
            check_system_file_drift(tmp, result)

            self.assertTrue(result.has_errors())
            combined = "\n".join(msg for msg, _path in result.errors)
            self.assertIn("runtime differs from templates", combined)

    def test_runtime_identical_to_template_is_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_all_templates(tmp)
            # Install an identical runtime copy
            self._write(tmp, "templates/scripts/whats_next.py", "print('same')\n")
            self._write(tmp, "scripts/whats_next.py", "print('same')\n")

            result = ValidationResult()
            check_system_file_drift(tmp, result)
            self.assertFalse(result.has_errors())

    def test_getmtime_failure_falls_back_to_generic_drift_error(self):
        """Covers the getmtime exception path (template/runtime drift still errors)."""
        with tempfile.TemporaryDirectory() as tmp:
            self._write_all_templates(tmp)
            self._write(tmp, "templates/scripts/whats_next.py", "print('template')\n")
            self._write(tmp, "scripts/whats_next.py", "print('runtime')\n")

            from scripts import validate_vibesafe_structure as v

            with mock.patch.object(v.os.path, "getmtime", side_effect=OSError("nope")):
                result = ValidationResult()
                check_system_file_drift(tmp, result)

            self.assertTrue(result.has_errors())
            combined = "\n".join(msg for msg, _path in result.errors)
            self.assertIn("runtime differs from templates", combined)

    def test_missing_template_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            # templates/ exists but required template file is missing
            os.makedirs(os.path.join(tmp, "templates", "scripts"), exist_ok=True)

            result = ValidationResult()
            check_system_file_drift(tmp, result)

            self.assertTrue(result.has_errors())
            combined = "\n".join(msg for msg, _path in result.errors)
            self.assertIn("Missing template system file", combined)

    def test_read_error_adds_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_all_templates(tmp)
            # runtime exists so drift check tries to read it
            runtime_path = self._write(tmp, "scripts/whats_next.py", "print('runtime')\n")

            from scripts import validate_vibesafe_structure as v

            real_open = open

            def open_side_effect(path, *args, **kwargs):
                if str(path).endswith("scripts/whats_next.py"):
                    raise OSError("boom")
                return real_open(path, *args, **kwargs)

            with mock.patch.object(v, "open", side_effect=open_side_effect):
                result = ValidationResult()
                check_system_file_drift(tmp, result)

            self.assertTrue(result.has_warnings())
            combined = "\n".join(msg for msg, _path in result.warnings)
            self.assertIn("Could not read system file drift pair", combined)

class TestGitChangedPaths(unittest.TestCase):
    """Unit tests for _get_git_changed_paths parsing logic."""

    def test_returns_none_when_not_git_repo(self):
        from scripts import validate_vibesafe_structure as v

        with mock.patch("subprocess.run") as m:
            m.return_value = mock.Mock(returncode=1, stdout="false\n")
            self.assertIsNone(v._get_git_changed_paths("/repo"))

    def test_returns_none_when_git_status_fails(self):
        from scripts import validate_vibesafe_structure as v

        with mock.patch("subprocess.run") as m:
            m.side_effect = [
                mock.Mock(returncode=0, stdout="true\n"),
                mock.Mock(returncode=2, stdout=""),
            ]
            self.assertIsNone(v._get_git_changed_paths("/repo"))

    def test_parses_renames_and_skips_blanks(self):
        from scripts import validate_vibesafe_structure as v

        with mock.patch("subprocess.run") as m:
            # First call: rev-parse
            m.side_effect = [
                mock.Mock(returncode=0, stdout="true\n"),
                mock.Mock(
                    returncode=0,
                    stdout="\n".join(
                        [
                            " M templates/scripts/whats_next.py",
                            "R  old/name.txt -> new/name.txt",
                            "?? untracked.file",
                            "  ",
                        ]
                    ),
                ),
            ]

            changed = v._get_git_changed_paths("/repo")

        self.assertEqual(
            changed,
            ["templates/scripts/whats_next.py", "new/name.txt", "untracked.file"],
        )


class TestGovernanceDriftMore(unittest.TestCase):
    def test_tenet_to_implementation_gap_warning(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        with mock.patch.object(
            v, "_get_git_changed_paths", return_value=["templates/scripts/x.py", "tenets/vibesafe/simplicity-of-use.md"]
        ):
            v.check_governance_drift("/repo", result)

        self.assertTrue(result.has_warnings())
        messages = "\n".join(m for m, _p in result.warnings)
        self.assertIn("Tenet→implementation gap", messages)


class TestValidatorHelpers(unittest.TestCase):
    def test_colored_wraps_text_and_resets(self):
        from scripts.validate_vibesafe_structure import Colors, colored  # pyright: ignore[reportMissingImports]

        Colors.BLUE = "<B>"
        Colors.END = "<E>"
        self.assertEqual(colored("x", Colors.BLUE), "<B>x<E>")

    def test_find_component_file_by_id_returns_none_when_dir_missing(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(v.find_component_file_by_id(tmp, "requirement", "0001"))

    def test_find_component_file_by_id_skips_non_md_and_missing_id(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "requirements"), exist_ok=True)
            with open(os.path.join(tmp, "requirements", "note.txt"), "w", encoding="utf-8") as f:
                f.write("nope")
            with open(os.path.join(tmp, "requirements", "req0001_test.md"), "w", encoding="utf-8") as f:
                f.write("---\nid: \"FFFF\"\n---\n")

            self.assertIsNone(v.find_component_file_by_id(tmp, "requirement", "0001"))

    def test_validate_component_skips_after_bad_filename(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        all_ids = {"requirement": set(), "cip": set(), "backlog": set(), "tenet": set()}
        with mock.patch.object(v, "validate_yaml_frontmatter") as m_yaml:
            v.validate_component(
                "/root",
                "requirement",
                "/root/requirements/not-a-req-file.md",  # doesn't match req pattern
                all_ids,
                result,
                auto_fix=False,
                dry_run=False,
            )
            m_yaml.assert_not_called()
        self.assertTrue(result.has_errors())

    def test_validate_yaml_frontmatter_handles_missing_frontmatter(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        with mock.patch.object(v, "extract_frontmatter", return_value=None):
            self.assertIsNone(v.validate_yaml_frontmatter("requirement", "requirements/req0001_test.md", result))
        self.assertTrue(result.has_errors())

    def test_validate_yaml_frontmatter_backlog_exception_type_errors(self):
        """Covers related_requirements type check, missing related_cips, and non-list related_cips."""
        from scripts import validate_vibesafe_structure as v

        backlog_file = "backlog/features/2026-01-03_test.md"

        result1 = ValidationResult()
        with mock.patch.object(
            v,
            "extract_frontmatter",
            return_value={
                "id": "2026-01-03_test",
                "title": "t",
                "status": "Ready",
                "priority": "High",
                "created": "2026-01-03",
                "last_updated": "2026-01-03",
                "owner": "Neil Lawrence",
                "category": "features",
                "related_requirements": "0001",  # wrong type
                # related_cips missing triggers error
            },
        ):
            v.validate_yaml_frontmatter("backlog", backlog_file, result1)
        self.assertTrue(result1.has_errors())
        errors1 = "\n".join(m for m, _p in result1.errors)
        self.assertIn("Invalid 'related_requirements'", errors1)
        self.assertIn("missing required field 'related_cips'", errors1)

        result2 = ValidationResult()
        with mock.patch.object(
            v,
            "extract_frontmatter",
            return_value={
                "id": "2026-01-03_test",
                "title": "t",
                "status": "Ready",
                "priority": "High",
                "created": "2026-01-03",
                "last_updated": "2026-01-03",
                "owner": "Neil Lawrence",
                "category": "features",
                "related_requirements": ["0001"],
                "related_cips": "cip0001",  # wrong type
                "no_cip_reason": "Because",
            },
        ):
            v.validate_yaml_frontmatter("backlog", backlog_file, result2)
        self.assertTrue(result2.has_errors())
        errors2 = "\n".join(m for m, _p in result2.errors)
        self.assertIn("Invalid 'related_cips': expected list", errors2)

    def test_validate_cross_references_coerces_scalar_to_list(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        all_ids = {"requirement": {"0001"}, "cip": set(), "backlog": set(), "tenet": set()}
        v.validate_cross_references(
            "requirement",
            "requirements/req0001_test.md",
            {"related_tenets": "user-autonomy"},
            all_ids,
            result,
        )
        self.assertTrue(result.has_warnings())


class TestFixReverseLinksWithMocks(unittest.TestCase):
    def test_fix_reverse_links_covers_missing_and_no_frontmatter_paths(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()

        def fake_find_component_files(_root, component_type):
            return {
                "tenet": ["tenets/t1.md", "tenets/t2.md"],
                "requirement": ["requirements/r1.md"],
                "cip": ["cip/c1.md"],
                "backlog": ["backlog/b1.md"],
            }[component_type]

        def fake_find_by_id(_root, component_type, target_id):
            mapping = {
                ("requirement", "0001"): "requirements/r1.md",
                ("requirement", "REQ_NO_FM"): "requirements/no.md",
                ("requirement", "MISSING_REQ"): None,
                ("cip", "CIP1"): "cip/c1.md",
                ("cip", "CIP_NO_FM"): "cip/no.md",
                ("cip", "MISSING_CIP"): None,
                ("backlog", "B1"): "backlog/b1.md",
                ("backlog", "MISSING_BACKLOG"): None,
            }
            return mapping.get((component_type, target_id))

        def fake_extract_frontmatter(path):
            fm = {
                "tenets/t1.md": {"id": "TENET1", "related_requirements": ["0001", "REQ_NO_FM", "MISSING_REQ"]},
                "tenets/t2.md": {"id": "TENET2"},  # triggers early continue
                "requirements/r1.md": {"id": "0001", "related_cips": ["CIP1", "CIP_NO_FM", "MISSING_CIP"]},
                "requirements/no.md": None,
                "cip/c1.md": {"id": "CIP1", "related_backlog": ["B1", "MISSING_BACKLOG"]},
                "cip/no.md": None,
                # Omit related_cips so the fixer adds an empty list.
                "backlog/b1.md": {"id": "B1", "related_requirements": ["0001"]},
            }
            return fm.get(path)

        with (
            mock.patch.object(v, "find_component_files", side_effect=fake_find_component_files),
            mock.patch.object(v, "find_component_file_by_id", side_effect=fake_find_by_id),
            mock.patch.object(v, "extract_frontmatter", side_effect=fake_extract_frontmatter),
            mock.patch.object(v, "write_frontmatter", return_value=True),
        ):
            fixes = v.fix_reverse_links("/root", result, dry_run=True)

        # Some fixes should have been applied, and several warnings emitted.
        self.assertGreaterEqual(fixes, 1)
        self.assertTrue(result.has_warnings())
        warnings = "\n".join(m for m, _p in result.warnings)
        self.assertIn("Cannot fix reverse link: requirement", warnings)
        self.assertIn("Cannot fix reverse link: CIP", warnings)
        self.assertIn("Cannot fix reverse link: backlog", warnings)


class TestFindFilesAndIdCollection(unittest.TestCase):
    def test_find_component_files_skips_templates_and_excluded_files(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            # Create backlog directory plus a "templates" subdir (must be skipped).
            os.makedirs(os.path.join(tmp, "backlog", "features"), exist_ok=True)
            os.makedirs(os.path.join(tmp, "backlog", "features", "templates"), exist_ok=True)

            # Valid-looking task file.
            good = os.path.join(tmp, "backlog", "features", "2026-01-01_test.md")
            with open(good, "w", encoding="utf-8") as f:
                f.write("---\nid: \"2026-01-01_test\"\n---\n")

            # Excluded files.
            with open(os.path.join(tmp, "backlog", "features", "index.md"), "w", encoding="utf-8") as f:
                f.write("ignored")
            with open(os.path.join(tmp, "backlog", "features", "README.md"), "w", encoding="utf-8") as f:
                f.write("ignored")

            # Would match pattern but should be skipped because it's under a templates directory.
            bad = os.path.join(tmp, "backlog", "features", "templates", "2026-01-02_test.md")
            with open(bad, "w", encoding="utf-8") as f:
                f.write("---\nid: \"2026-01-02_test\"\n---\n")

            files = v.find_component_files(tmp, "backlog")
            self.assertIn(good, files)
            self.assertNotIn(bad, files)

    def test_collect_all_ids_picks_up_ids_when_present(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "requirements"), exist_ok=True)
            os.makedirs(os.path.join(tmp, "tenets", "vibesafe"), exist_ok=True)

            with open(os.path.join(tmp, "requirements", "req0001_test.md"), "w", encoding="utf-8") as f:
                f.write(
                    """---
id: "0001"
title: "Req"
status: "Ready"
priority: "High"
created: "2026-01-01"
last_updated: "2026-01-01"
related_tenets: []
stakeholders: []
---
"""
                )

            with open(os.path.join(tmp, "tenets", "vibesafe", "simplicity-of-use.md"), "w", encoding="utf-8") as f:
                f.write("---\nid: \"simplicity-of-use\"\n---\n")

            all_ids = v.collect_all_ids(tmp)
            self.assertIn("0001", all_ids["requirement"])
            self.assertIn("simplicity-of-use", all_ids["tenet"])


class TestWriteFrontmatterAndAutoFix(unittest.TestCase):
    def test_write_frontmatter_returns_false_on_exception(self):
        from scripts import validate_vibesafe_structure as v

        with mock.patch.object(v.frontmatter, "load", side_effect=Exception("boom")):
            self.assertFalse(v.write_frontmatter("x.md", {"id": "0001"}, dry_run=False))

    def test_auto_fix_frontmatter_none_returns_false(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        self.assertFalse(v.auto_fix_frontmatter("requirement", "requirements/req0001_test.md", None, result))


class TestPrintResultsAndMainCli(unittest.TestCase):
    def test_print_results_exercises_branches(self):
        from scripts import validate_vibesafe_structure as v

        result = ValidationResult()
        result.add_info("hello")
        result.add_fix("fixed thing", "file.md")
        result.add_warning("warn thing", "file.md")
        result.add_error("error thing", "file.md")

        buf = io.StringIO()
        with redirect_stdout(buf):
            v.print_results(result, strict=True, dry_run=True)

        out = buf.getvalue()
        self.assertIn("Validation FAILED", out)
        self.assertIn("DRY RUN", out)

    def test_main_exits_0_when_clean_and_skips_governance_when_requested(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            with (
                mock.patch.object(sys, "argv", ["prog", "--root", tmp, "--no-governance-drift"]),
                mock.patch.object(v, "collect_all_ids", return_value={"requirement": set(), "cip": set(), "backlog": set(), "tenet": set()}),
                mock.patch.object(v, "find_component_files", return_value=[]),
                mock.patch.object(v, "check_system_file_drift"),
                mock.patch.object(v, "check_governance_drift", side_effect=AssertionError("should not run")),
                mock.patch.object(v, "print_results"),
            ):
                with self.assertRaises(SystemExit) as se:
                    v.main()
                self.assertEqual(se.exception.code, 0)

    def test_main_strict_exits_1_on_warning(self):
        from scripts import validate_vibesafe_structure as v

        def add_warning(_root, _ctype, _file, _all_ids, result, *_a, **_k):
            result.add_warning("w", _file)

        with tempfile.TemporaryDirectory() as tmp:
            with (
                mock.patch.object(sys, "argv", ["prog", "--root", tmp, "--strict", "--component", "req", "--no-governance-drift"]),
                mock.patch.object(v, "collect_all_ids", return_value={"requirement": set(), "cip": set(), "backlog": set(), "tenet": set()}),
                mock.patch.object(v, "find_component_files", return_value=["requirements/req0001_test.md"]),
                mock.patch.object(v, "validate_component", side_effect=add_warning),
                mock.patch.object(v, "check_system_file_drift"),
                mock.patch.object(v, "print_results"),
            ):
                with self.assertRaises(SystemExit) as se:
                    v.main()
                self.assertEqual(se.exception.code, 1)

    def test_main_no_color_calls_disable_and_fix_links_calls_fixer(self):
        from scripts import validate_vibesafe_structure as v

        with tempfile.TemporaryDirectory() as tmp:
            with (
                mock.patch.object(sys, "argv", ["prog", "--root", tmp, "--no-color", "--fix-links", "--no-governance-drift"]),
                mock.patch.object(v.Colors, "disable") as m_disable,
                mock.patch.object(v, "fix_reverse_links", return_value=2) as m_fix,
                mock.patch.object(v, "collect_all_ids", return_value={"requirement": set(), "cip": set(), "backlog": set(), "tenet": set()}),
                mock.patch.object(v, "find_component_files", return_value=[]),
                mock.patch.object(v, "check_system_file_drift"),
                mock.patch.object(v, "print_results"),
            ):
                with self.assertRaises(SystemExit):
                    v.main()

        m_disable.assert_called_once()
        m_fix.assert_called_once()


class TestColors(unittest.TestCase):
    def test_disable_clears_codes(self):
        from scripts.validate_vibesafe_structure import Colors  # pyright: ignore[reportMissingImports]

        Colors.disable()
        self.assertEqual(Colors.GREEN, "")
        self.assertEqual(Colors.END, "")


if __name__ == '__main__':
    unittest.main()

