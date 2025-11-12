"""Task storage and persistence."""

import json
import os
from pathlib import Path
from typing import List, Optional
from .task import Task


class TaskStorage:
    """Handles task persistence using JSON."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize task storage.
        
        Args:
            storage_path: Optional custom storage path
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            # Use ~/.flexdo/tasks.json as default
            self.storage_path = Path.home() / '.flexdo' / 'tasks.json'
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize config path
        self.config_path = self.storage_path.parent / 'config.json'
        self._ensure_config()
    
    def _ensure_config(self):
        """Ensure config file exists with default values."""
        if not self.config_path.exists():
            default_config = {
                'weights': {
                    'priority': 1.0,
                    'effort': 0.5,
                    'deadline_proximity': 1.5
                },
                'focus_session_duration': 25  # minutes
            }
            self.save_config(default_config)
    
    def load_config(self) -> dict:
        """Load configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'weights': {
                    'priority': 1.0,
                    'effort': 0.5,
                    'deadline_proximity': 1.5
                },
                'focus_session_duration': 25
            }
    
    def save_config(self, config: dict):
        """Save configuration."""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage."""
        if not self.storage_path.exists():
            return []
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_tasks(self, tasks: List[Task]):
        """Save all tasks to storage."""
        with open(self.storage_path, 'w') as f:
            data = [task.to_dict() for task in tasks]
            json.dump(data, f, indent=2)
    
    def add_task(self, task: Task) -> Task:
        """Add a new task."""
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def update_task(self, task: Task):
        """Update an existing task."""
        tasks = self.load_tasks()
        for i, t in enumerate(tasks):
            if t.task_id == task.task_id:
                tasks[i] = task
                break
        self.save_tasks(tasks)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        tasks = self.load_tasks()
        original_length = len(tasks)
        tasks = [t for t in tasks if t.task_id != task_id]
        if len(tasks) < original_length:
            self.save_tasks(tasks)
            return True
        return False
    
    def get_active_tasks(self) -> List[Task]:
        """Get all active (not completed) tasks."""
        tasks = self.load_tasks()
        return [t for t in tasks if not t.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        tasks = self.load_tasks()
        return [t for t in tasks if t.completed]
