# Contributing to FlexDo

Thank you for your interest in contributing to FlexDo! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git

### Setting Up Your Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/flexdo.git
   cd flexdo
   ```

2. **Install in Development Mode**
   ```bash
   pip install -e .
   ```

3. **Verify Installation**
   ```bash
   flexdo --help
   ```

## Project Structure

```
flexdo/
├── flexdo/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface (Click-based)
│   ├── task.py          # Task model and scoring logic
│   ├── storage.py       # JSON-based persistence layer
│   └── session.py       # Focus session management
├── tests/
│   ├── __init__.py
│   ├── test_task.py     # Task model tests
│   ├── test_storage.py  # Storage and persistence tests
│   └── test_session.py  # Focus session tests
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies
├── README.md            # Main documentation
├── USAGE_EXAMPLES.md    # Practical usage examples
└── CONTRIBUTING.md      # This file
```

## Running Tests

### All Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Specific Test File

```bash
python3 -m unittest tests.test_task -v
```

### Individual Test

```bash
python3 -m unittest tests.test_task.TestTask.test_task_creation -v
```

## Code Style

### Python Style Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Documentation

- Add docstrings to all functions, classes, and modules
- Use Google-style docstrings:
  ```python
  def function_name(param1, param2):
      """Brief description.
      
      More detailed description if needed.
      
      Args:
          param1: Description of param1
          param2: Description of param2
      
      Returns:
          Description of return value
      """
  ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/feature-name` for new features
- `bugfix/bug-description` for bug fixes
- `docs/what-changed` for documentation updates

### Commit Messages

Write clear, concise commit messages:
```
Add task filtering by tags

- Implement tag-based filtering in list command
- Add tests for tag filtering
- Update documentation with examples
```

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run Tests**
   ```bash
   python3 -m unittest discover -s tests -p "test_*.py" -v
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Describe what changes you made
   - Reference any related issues
   - Include examples if applicable

## Adding New Features

### Adding a New CLI Command

1. **Add command to `cli.py`**
   ```python
   @cli.command()
   @click.argument('arg_name')
   @click.option('--option', help='Option description')
   def new_command(arg_name, option):
       """Command description."""
       # Implementation
   ```

2. **Add tests in `tests/`**
   ```python
   def test_new_command(self):
       """Test new command functionality."""
       # Test implementation
   ```

3. **Update documentation**
   - Add to README.md command reference
   - Add examples to USAGE_EXAMPLES.md

### Adding Task Criteria

To add a new criterion for task scoring:

1. **Update Task Model** (`task.py`)
   ```python
   def __init__(self, ..., new_criterion=default_value):
       self.new_criterion = new_criterion
   ```

2. **Update Scoring Logic** (`task.py`)
   ```python
   def calculate_score(self, weights):
       # Add new criterion calculation
       score += self.new_criterion * weights.get('new_criterion', 1.0)
   ```

3. **Update Storage** (`storage.py`)
   - Ensure serialization/deserialization handles new field

4. **Update CLI** (`cli.py`)
   - Add option to `add` command
   - Add to `config` command if it's a weight

5. **Add Tests**
   - Test new criterion in scoring
   - Test persistence

## Testing Guidelines

### Writing Tests

- Each test should test one specific behavior
- Use descriptive test names: `test_description_of_what_is_tested`
- Include both positive and negative test cases
- Clean up any test data in `tearDown()`

### Test Structure

```python
class TestFeature(unittest.TestCase):
    """Test suite for feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize test data
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files, etc.
    
    def test_normal_case(self):
        """Test normal operation."""
        # Arrange
        # Act
        # Assert
    
    def test_edge_case(self):
        """Test edge case."""
        # Test implementation
```

## Documentation

### Updating README.md

When adding features, update:
- Features list
- Quick Start if command usage changed
- Command Reference table
- Examples if applicable

### Code Comments

- Use comments sparingly - prefer self-documenting code
- Comment "why" not "what"
- Update comments when changing code

## Reporting Issues

### Bug Reports

Include:
- FlexDo version (`flexdo --version`)
- Python version (`python3 --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests

Include:
- Clear description of the feature
- Use case / problem it solves
- Proposed implementation (optional)
- Examples of how it would work

## Code Review

All contributions will be reviewed for:
- Functionality: Does it work as intended?
- Tests: Are there adequate tests?
- Style: Does it follow project conventions?
- Documentation: Is it properly documented?

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Clarification on contributing process
- Discussion of potential features

## License

By contributing to FlexDo, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make FlexDo better for everyone. We appreciate your time and effort! 🎯
