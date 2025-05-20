"""
Constants used throughout the backlog module.
"""

# Categories to organize backlog items
CATEGORIES = ['documentation', 'infrastructure', 'features', 'bugs']

# Statuses for tasks
STATUSES = ['Proposed', 'Ready', 'In Progress', 'Completed', 'Abandoned']

# Priority levels
PRIORITIES = ['High', 'Medium', 'Low']

# Naming conventions for task files
NAMING_CONVENTIONS = [
    r'(\d{4}-\d{2}-\d{2})_(.+)\.md',  # YYYY-MM-DD_description.md
    r'(\d{8})-(.+)\.md',               # YYYYMMDD-description.md
] 