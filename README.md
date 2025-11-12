# flexdo

Command-line tool for flexible daily task management, focusing on adaptive scheduling and priority-driven focus sessions.

## Overview

`flexdo` helps you manage tasks when your schedule changes daily. Instead of assigning fixed times to tasks, it uses weighted criteria to intelligently suggest what to work on next and helps you stay focused through timed work sessions.

## Features

- **Flexible Task Planning**: Add tasks without assigning them fixed time slots
- **Multi-Criteria Classification**: Tasks are scored based on weighted criteria:
  - Priority (1-5)
  - Effort level (1-5)
  - Deadline proximity (automatic calculation)
- **Smart Task Suggestions**: Get task recommendations based on your current configuration
- **Focus Sessions**: Manage your day through timed focus sessions with progress tracking
- **Customizable Weights**: Adjust how much each criterion affects task scoring

## Installation

```bash
# Clone the repository
git clone https://github.com/jzoubian/flexdo.git
cd flexdo

# Install the package
pip install -e .
```

## Quick Start

### Add a Task

```bash
# Simple task
flexdo add "Write documentation"

# Task with details
flexdo add "Fix critical bug" --priority 5 --effort 2 --deadline 2025-11-15 --tag urgent

# Using short options
flexdo add "Code review" -p 3 -e 1 -t review
```

### List Tasks

```bash
# List active tasks (default: sorted by score)
flexdo list

# List all tasks including completed
flexdo list --all

# Sort by different criteria
flexdo list --sort priority
flexdo list --sort deadline
```

### Get Task Suggestions

```bash
# Get top 5 suggested tasks
flexdo suggest

# Get top 3 tasks
flexdo suggest --limit 3
```

### Start a Focus Session

```bash
# Start session with a specific task
flexdo focus <task_id>

# Start with the top suggested task
flexdo focus --top

# Custom duration (default: 25 minutes)
flexdo focus --top --duration 45
```

### Manage Tasks

```bash
# View task details
flexdo show <task_id>

# Mark task as completed
flexdo done <task_id>

# Delete a task
flexdo delete <task_id>
```

### Configure Weights

```bash
# View current configuration
flexdo config --show

# Adjust weights for task scoring
flexdo config --priority 2.0 --effort 0.8 --deadline 1.5

# Change default focus session duration
flexdo config --session-duration 30
```

## Task Scoring

Tasks are scored using a weighted formula:

```
Score = (Priority × priority_weight) + 
        ((6 - Effort) × effort_weight) + 
        (Deadline_Proximity × deadline_weight)
```

**Default Weights:**
- Priority: 1.0
- Effort: 0.5 (lower effort = higher score for quick wins)
- Deadline Proximity: 1.5

**Deadline Proximity Scoring:**
- Overdue: 10.0
- Due today: 8.0
- Due within 3 days: 6.0
- Due within 7 days: 4.0
- Due later: diminishing score

## Examples

### Daily Workflow

```bash
# Morning: Review your tasks
flexdo list

# Get suggestions for what to tackle first
flexdo suggest

# Start a focus session with the top priority task
flexdo focus --top --duration 25

# After completing the session
flexdo end --complete

# Add new tasks as they come up
flexdo add "Review pull request" -p 4 -e 1 --tag review
```

### Project Planning

```bash
# Add project tasks with varying priorities
flexdo add "Design database schema" -p 5 -e 4 --deadline 2025-11-20
flexdo add "Set up CI/CD pipeline" -p 4 -e 3 --deadline 2025-11-22
flexdo add "Write API documentation" -p 3 -e 2 --deadline 2025-11-25

# View sorted by deadline
flexdo list --sort deadline

# Focus on the most important task
flexdo suggest --limit 1
```

### Custom Configuration

```bash
# Prioritize urgent deadlines over everything else
flexdo config --deadline 3.0 --priority 1.0 --effort 0.3

# Prefer quick wins (low effort tasks)
flexdo config --effort 1.5 --priority 1.0 --deadline 1.0
```

## Data Storage

- Tasks are stored in `~/.flexdo/tasks.json`
- Configuration is stored in `~/.flexdo/config.json`
- All data is kept locally on your machine

## Command Reference

| Command | Description |
|---------|-------------|
| `flexdo add TITLE [OPTIONS]` | Add a new task |
| `flexdo list [OPTIONS]` | List tasks |
| `flexdo show TASK_ID` | Show task details |
| `flexdo done TASK_ID` | Mark task as completed |
| `flexdo delete TASK_ID` | Delete a task |
| `flexdo suggest [OPTIONS]` | Get task suggestions |
| `flexdo focus [TASK_ID\|--top] [OPTIONS]` | Start a focus session |
| `flexdo status` | Check current focus session |
| `flexdo end [OPTIONS]` | End focus session |
| `flexdo config [OPTIONS]` | Configure weights and settings |

## Development

### Run Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Project Structure

```
flexdo/
├── flexdo/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── task.py         # Task model and scoring
│   ├── storage.py      # Data persistence
│   └── session.py      # Focus session management
├── tests/
│   ├── test_task.py
│   ├── test_storage.py
│   └── test_session.py
├── setup.py
├── requirements.txt
└── README.md
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
