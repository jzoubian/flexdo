"""Tests for task storage."""

import unittest
import tempfile
import os
from pathlib import Path
from flexdo.task import Task
from flexdo.storage import TaskStorage


class TestTaskStorage(unittest.TestCase):
    """Test TaskStorage class."""
    
    def setUp(self):
        """Set up test storage."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage_path = os.path.join(self.temp_dir, 'test_tasks.json')
        self.storage = TaskStorage(self.storage_path)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
        config_path = Path(self.storage_path).parent / 'config.json'
        if config_path.exists():
            os.remove(config_path)
        os.rmdir(self.temp_dir)
    
    def test_add_task(self):
        """Test adding a task."""
        task = Task(title="Test Task", priority=4)
        
        added_task = self.storage.add_task(task)
        
        self.assertEqual(added_task.title, "Test Task")
        self.assertEqual(added_task.priority, 4)
    
    def test_load_tasks(self):
        """Test loading tasks."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        
        tasks = self.storage.load_tasks()
        
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")
    
    def test_get_task(self):
        """Test getting a specific task."""
        task = Task(title="Test Task", priority=5)
        self.storage.add_task(task)
        
        retrieved = self.storage.get_task(task.task_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Test Task")
        self.assertEqual(retrieved.priority, 5)
    
    def test_update_task(self):
        """Test updating a task."""
        task = Task(title="Original Title")
        self.storage.add_task(task)
        
        task.title = "Updated Title"
        task.completed = True
        self.storage.update_task(task)
        
        retrieved = self.storage.get_task(task.task_id)
        self.assertEqual(retrieved.title, "Updated Title")
        self.assertTrue(retrieved.completed)
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = Task(title="Task to Delete")
        self.storage.add_task(task)
        
        result = self.storage.delete_task(task.task_id)
        
        self.assertTrue(result)
        self.assertIsNone(self.storage.get_task(task.task_id))
    
    def test_get_active_tasks(self):
        """Test getting only active tasks."""
        task1 = Task(title="Active Task")
        task2 = Task(title="Completed Task")
        task2.completed = True
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        
        active = self.storage.get_active_tasks()
        
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].title, "Active Task")
    
    def test_config_persistence(self):
        """Test configuration save and load."""
        config = {
            'weights': {
                'priority': 2.0,
                'effort': 1.0,
                'deadline_proximity': 3.0
            },
            'focus_session_duration': 45
        }
        
        self.storage.save_config(config)
        loaded = self.storage.load_config()
        
        self.assertEqual(loaded['weights']['priority'], 2.0)
        self.assertEqual(loaded['focus_session_duration'], 45)


if __name__ == '__main__':
    unittest.main()
