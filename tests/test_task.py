"""Tests for task model."""

import unittest
from datetime import datetime, timedelta
from flexdo.task import Task


class TestTask(unittest.TestCase):
    """Test Task class."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(
            title="Test Task",
            description="Test description",
            priority=4,
            effort=3
        )
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.priority, 4)
        self.assertEqual(task.effort, 3)
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.task_id)
    
    def test_priority_clamping(self):
        """Test that priority is clamped to 1-5 range."""
        task1 = Task(title="Test", priority=10)
        self.assertEqual(task1.priority, 5)
        
        task2 = Task(title="Test", priority=0)
        self.assertEqual(task2.priority, 1)
        
        task3 = Task(title="Test", priority=3)
        self.assertEqual(task3.priority, 3)
    
    def test_effort_clamping(self):
        """Test that effort is clamped to 1-5 range."""
        task1 = Task(title="Test", effort=10)
        self.assertEqual(task1.effort, 5)
        
        task2 = Task(title="Test", effort=-1)
        self.assertEqual(task2.effort, 1)
    
    def test_score_calculation_basic(self):
        """Test basic score calculation without deadline."""
        task = Task(title="Test", priority=5, effort=1)
        weights = {'priority': 1.0, 'effort': 0.5, 'deadline_proximity': 1.0}
        
        score = task.calculate_score(weights)
        
        # Priority: 5 * 1.0 = 5.0
        # Effort: (6-1) * 0.5 = 2.5
        # Total: 7.5
        self.assertEqual(score, 7.5)
    
    def test_score_calculation_with_deadline(self):
        """Test score calculation with deadline."""
        # Task due tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        task = Task(title="Test", priority=3, effort=3, deadline=tomorrow)
        weights = {'priority': 1.0, 'effort': 0.5, 'deadline_proximity': 1.0}
        
        score = task.calculate_score(weights)
        
        # Should have deadline proximity boost
        self.assertGreater(score, 4.5)  # Priority + effort without deadline
    
    def test_task_to_dict(self):
        """Test task serialization."""
        task = Task(
            title="Test Task",
            priority=4,
            effort=2,
            deadline="2025-12-31"
        )
        
        data = task.to_dict()
        
        self.assertEqual(data['title'], "Test Task")
        self.assertEqual(data['priority'], 4)
        self.assertEqual(data['effort'], 2)
        self.assertEqual(data['deadline'], "2025-12-31")
        self.assertFalse(data['completed'])
    
    def test_task_from_dict(self):
        """Test task deserialization."""
        data = {
            'task_id': '12345',
            'title': 'Test Task',
            'description': 'Test',
            'priority': 5,
            'effort': 3,
            'deadline': '2025-12-31',
            'tags': ['test'],
            'created_at': '2025-01-01T00:00:00',
            'completed': False
        }
        
        task = Task.from_dict(data)
        
        self.assertEqual(task.task_id, '12345')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.effort, 3)
        self.assertEqual(task.deadline, '2025-12-31')
        self.assertEqual(task.tags, ['test'])


if __name__ == '__main__':
    unittest.main()
