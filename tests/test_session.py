"""Tests for focus session management."""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from flexdo.task import Task
from flexdo.storage import TaskStorage
from flexdo.session import FocusSession


class TestFocusSession(unittest.TestCase):
    """Test FocusSession class."""
    
    def setUp(self):
        """Set up test storage and session."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage_path = os.path.join(self.temp_dir, 'test_tasks.json')
        self.storage = TaskStorage(self.storage_path)
        self.session = FocusSession(self.storage)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
        from pathlib import Path
        config_path = Path(self.storage_path).parent / 'config.json'
        if config_path.exists():
            os.remove(config_path)
        os.rmdir(self.temp_dir)
    
    def test_suggest_tasks(self):
        """Test task suggestion based on scoring."""
        # Add tasks with different priorities
        task1 = Task(title="Low Priority", priority=1, effort=3)
        task2 = Task(title="High Priority", priority=5, effort=2)
        task3 = Task(title="Medium Priority", priority=3, effort=1)
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        self.storage.add_task(task3)
        
        suggestions = self.session.suggest_tasks(limit=3)
        
        self.assertEqual(len(suggestions), 3)
        # High priority task should be first
        self.assertEqual(suggestions[0][0].title, "High Priority")
    
    def test_suggest_tasks_with_deadline(self):
        """Test that tasks with closer deadlines are prioritized."""
        today = datetime.now().strftime('%Y-%m-%d')
        future = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        task1 = Task(title="Due Soon", priority=3, effort=2, deadline=today)
        task2 = Task(title="Due Later", priority=4, effort=2, deadline=future)
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        
        suggestions = self.session.suggest_tasks(limit=2)
        
        # Task with closer deadline should score higher despite lower priority
        self.assertEqual(suggestions[0][0].title, "Due Soon")
    
    def test_start_session(self):
        """Test starting a focus session."""
        task = Task(title="Test Task")
        self.storage.add_task(task)
        
        session_info = self.session.start_session(task, duration_minutes=25)
        
        self.assertEqual(session_info['task'], task)
        self.assertEqual(session_info['duration_minutes'], 25)
        self.assertIsNotNone(session_info['start_time'])
        self.assertIsNotNone(session_info['end_time'])
    
    def test_session_status(self):
        """Test getting session status."""
        task = Task(title="Test Task")
        self.storage.add_task(task)
        
        self.session.start_session(task, duration_minutes=25)
        status = self.session.get_session_status()
        
        self.assertIsNotNone(status)
        self.assertEqual(status['task'], task)
        self.assertGreaterEqual(status['elapsed_minutes'], 0)
        self.assertLessEqual(status['remaining_minutes'], 25)
    
    def test_end_session(self):
        """Test ending a focus session."""
        task = Task(title="Test Task")
        self.storage.add_task(task)
        
        self.session.start_session(task, duration_minutes=1)
        summary = self.session.end_session(mark_complete=True)
        
        self.assertEqual(summary['task'].title, "Test Task")
        self.assertTrue(summary['completed'])
        self.assertGreaterEqual(summary['elapsed_minutes'], 0)
        
        # Verify task was marked complete
        retrieved = self.storage.get_task(task.task_id)
        self.assertTrue(retrieved.completed)
    
    def test_suggest_excludes_completed(self):
        """Test that completed tasks are not suggested."""
        task1 = Task(title="Active Task", priority=5)
        task2 = Task(title="Completed Task", priority=5)
        task2.completed = True
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        
        suggestions = self.session.suggest_tasks(limit=10)
        
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0][0].title, "Active Task")


if __name__ == '__main__':
    unittest.main()
