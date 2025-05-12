"""
Backlog management package for VibeSafe.
"""

# Import all functions needed by tests
from backlog.update_index import (
    extract_yaml_frontmatter,
    extract_task_metadata,
    find_all_task_files,
    generate_index_content,
    update_index,
    CATEGORIES,
    STATUSES
)

# Define public API
__all__ = [
    'extract_yaml_frontmatter',
    'extract_task_metadata',
    'find_all_task_files',
    'generate_index_content',
    'update_index',
    'CATEGORIES',
    'STATUSES'
] 