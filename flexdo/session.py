"""Focus session management."""

import time
from datetime import datetime, timedelta
from typing import List, Optional
from .task import Task
from .storage import TaskStorage


class FocusSession:
    """Manages focus sessions for task completion."""
    
    def __init__(self, storage: TaskStorage):
        """
        Initialize focus session manager.
        
        Args:
            storage: TaskStorage instance
        """
        self.storage = storage
        self.current_task = None
        self.start_time = None
        self.duration_minutes = None
    
    def suggest_tasks(self, limit: int = 5) -> List[tuple]:
        """
        Suggest tasks based on weighted criteria.
        
        Args:
            limit: Maximum number of tasks to suggest
        
        Returns:
            List of tuples (task, score)
        """
        tasks = self.storage.get_active_tasks()
        config = self.storage.load_config()
        weights = config.get('weights', {
            'priority': 1.0,
            'effort': 0.5,
            'deadline_proximity': 1.5
        })
        
        # Calculate scores for all tasks
        scored_tasks = []
        for task in tasks:
            score = task.calculate_score(weights)
            scored_tasks.append((task, score))
        
        # Sort by score (descending)
        scored_tasks.sort(key=lambda x: x[1], reverse=True)
        
        return scored_tasks[:limit]
    
    def start_session(self, task: Task, duration_minutes: Optional[int] = None) -> dict:
        """
        Start a focus session for a task.
        
        Args:
            task: Task to work on
            duration_minutes: Optional custom duration
        
        Returns:
            Session info dictionary
        """
        config = self.storage.load_config()
        self.current_task = task
        self.start_time = datetime.now()
        self.duration_minutes = duration_minutes or config.get('focus_session_duration', 25)
        
        end_time = self.start_time + timedelta(minutes=self.duration_minutes)
        
        return {
            'task': task,
            'start_time': self.start_time,
            'duration_minutes': self.duration_minutes,
            'end_time': end_time
        }
    
    def get_session_status(self) -> Optional[dict]:
        """
        Get current session status.
        
        Returns:
            Session status dictionary or None if no active session
        """
        if not self.current_task or not self.start_time:
            return None
        
        now = datetime.now()
        elapsed = (now - self.start_time).total_seconds() / 60  # minutes
        remaining = max(0, self.duration_minutes - elapsed)
        
        return {
            'task': self.current_task,
            'elapsed_minutes': elapsed,
            'remaining_minutes': remaining,
            'is_complete': remaining == 0
        }
    
    def end_session(self, mark_complete: bool = False) -> dict:
        """
        End the current focus session.
        
        Args:
            mark_complete: Whether to mark the task as complete
        
        Returns:
            Session summary dictionary
        """
        if not self.current_task or not self.start_time:
            return {'error': 'No active session'}
        
        end_time = datetime.now()
        elapsed = (end_time - self.start_time).total_seconds() / 60
        
        session_summary = {
            'task': self.current_task,
            'start_time': self.start_time,
            'end_time': end_time,
            'elapsed_minutes': elapsed,
            'completed': mark_complete
        }
        
        if mark_complete:
            self.current_task.completed = True
            self.storage.update_task(self.current_task)
        
        # Clear session
        self.current_task = None
        self.start_time = None
        self.duration_minutes = None
        
        return session_summary
