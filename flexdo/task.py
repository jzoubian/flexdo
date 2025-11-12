"""Task model and classification logic."""

from datetime import datetime, timedelta
from typing import Dict, Optional
import json


class Task:
    """Represents a task with weighted criteria for classification."""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: int = 3,
        effort: int = 3,
        deadline: Optional[str] = None,
        tags: Optional[list] = None,
        task_id: Optional[str] = None
    ):
        """
        Initialize a task.
        
        Args:
            title: Task title
            description: Task description
            priority: Priority level (1-5, 5 being highest)
            effort: Estimated effort (1-5, 5 being highest)
            deadline: Optional deadline in ISO format (YYYY-MM-DD)
            tags: Optional list of tags
            task_id: Optional unique identifier
        """
        self.task_id = task_id or self._generate_id()
        self.title = title
        self.description = description
        self.priority = max(1, min(5, priority))  # Clamp to 1-5
        self.effort = max(1, min(5, effort))  # Clamp to 1-5
        self.deadline = deadline
        self.tags = tags or []
        self.created_at = datetime.now().isoformat()
        self.completed = False
    
    def _generate_id(self) -> str:
        """Generate a unique task ID."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def calculate_score(self, weights: Dict[str, float]) -> float:
        """
        Calculate weighted score for task prioritization.
        
        Args:
            weights: Dictionary with keys 'priority', 'effort', 'deadline_proximity'
        
        Returns:
            Weighted score for the task
        """
        score = 0.0
        
        # Priority contribution (higher priority = higher score)
        score += self.priority * weights.get('priority', 1.0)
        
        # Effort contribution (lower effort = higher score for quick wins)
        # Invert effort so lower effort gets higher score
        score += (6 - self.effort) * weights.get('effort', 0.5)
        
        # Deadline proximity contribution (sooner deadline = higher score)
        if self.deadline:
            try:
                deadline_date = datetime.fromisoformat(self.deadline)
                days_until = (deadline_date - datetime.now()).days
                
                # Closer deadlines get higher scores
                if days_until < 0:
                    # Overdue - very high score
                    proximity_score = 10.0
                elif days_until == 0:
                    # Due today
                    proximity_score = 8.0
                elif days_until <= 3:
                    # Due within 3 days
                    proximity_score = 6.0
                elif days_until <= 7:
                    # Due within a week
                    proximity_score = 4.0
                else:
                    # Due later - diminishing score
                    proximity_score = max(1.0, 10.0 / (days_until / 7))
                
                score += proximity_score * weights.get('deadline_proximity', 1.0)
            except (ValueError, TypeError):
                pass
        
        return score
    
    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'effort': self.effort,
            'deadline': self.deadline,
            'tags': self.tags,
            'created_at': self.created_at,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create task from dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 3),
            effort=data.get('effort', 3),
            deadline=data.get('deadline'),
            tags=data.get('tags', []),
            task_id=data.get('task_id')
        )
        task.created_at = data.get('created_at', task.created_at)
        task.completed = data.get('completed', False)
        return task
    
    def __str__(self) -> str:
        """String representation of task."""
        deadline_str = f" [Due: {self.deadline}]" if self.deadline else ""
        tags_str = f" {{{', '.join(self.tags)}}}" if self.tags else ""
        status = "✓" if self.completed else " "
        return f"[{status}] {self.title}{deadline_str}{tags_str}"
