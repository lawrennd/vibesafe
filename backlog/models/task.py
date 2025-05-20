"""
Task model for the backlog module.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from backlog.models.constants import STATUSES, PRIORITIES, CATEGORIES


@dataclass
class Task:
    """Represents a backlog task."""
    
    # Required fields
    id: str
    filepath: Path
    category: str
    
    # Optional fields with defaults
    title: Optional[str] = None
    status: str = 'Proposed'
    priority: str = 'Medium'
    created: Optional[str] = None
    updated: Optional[str] = None
    description: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate task data after initialization."""
        # Ensure status is valid
        if self.status not in STATUSES:
            raise ValueError(f"Invalid status: {self.status}. Must be one of {STATUSES}")
        
        # Ensure priority is valid
        if self.priority not in PRIORITIES:
            raise ValueError(f"Invalid priority: {self.priority}. Must be one of {PRIORITIES}")
        
        # Ensure category is valid
        if self.category not in CATEGORIES:
            raise ValueError(f"Invalid category: {self.category}. Must be one of {CATEGORIES}")
        
        # Set created date if not provided
        if self.created is None:
            self.created = datetime.now().strftime('%Y-%m-%d')
        
        # Set updated date if not provided
        if self.updated is None:
            self.updated = self.created
    
    @property
    def relative_path(self) -> str:
        """Get the relative path to the task file."""
        return f"{self.category}/{self.filepath.name}"
    
    @property
    def is_complete(self) -> bool:
        """Check if the task is completed."""
        return self.status.lower() == 'completed'
    
    @property
    def is_abandoned(self) -> bool:
        """Check if the task is abandoned."""
        return self.status.lower() == 'abandoned'
    
    @property
    def is_active(self) -> bool:
        """Check if the task is active (not completed or abandoned)."""
        return not (self.is_complete or self.is_abandoned)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'created': self.created,
            'updated': self.updated,
            'description': self.description,
            'dependencies': self.dependencies,
            'tags': self.tags,
            'metadata': self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], filepath: Path) -> 'Task':
        """Create a task from a dictionary."""
        # Extract required fields
        id_val = data.get('id')
        category = data.get('category')
        
        # Ensure required fields are present
        if id_val is None:
            id_val = filepath.stem
        
        if category is None:
            # Try to extract category from filepath
            for cat in CATEGORIES:
                if cat in str(filepath):
                    category = cat
                    break
        
        # Create task
        return cls(
            id=id_val,
            filepath=filepath,
            category=category,
            title=data.get('title'),
            status=data.get('status', 'Proposed'),
            priority=data.get('priority', 'Medium'),
            created=data.get('created'),
            updated=data.get('updated') or data.get('last_updated'),
            description=data.get('description'),
            dependencies=data.get('dependencies', []),
            tags=data.get('tags', []),
            metadata={k: v for k, v in data.items() if k not in cls.__annotations__},
        ) 