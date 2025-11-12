# Changelog

All notable changes to FlexDo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-12

### Added

#### Core Features
- **Task Management System**
  - Create tasks with title, description, priority (1-5), effort (1-5), deadline, and tags
  - Mark tasks as completed
  - Delete tasks
  - View detailed task information
  - List tasks with multiple sorting options (score, priority, deadline, created)

- **Intelligent Task Scoring**
  - Multi-criteria scoring based on weighted factors
  - Priority-based scoring (higher priority = higher score)
  - Effort-based scoring (lower effort = higher score for quick wins)
  - Deadline proximity scoring (sooner deadlines = higher score)
  - Automatic calculation of overdue, due today, and approaching deadline priorities

- **Task Suggestions**
  - Get intelligent task recommendations based on weighted scoring
  - Configurable suggestion limits
  - Automatically excludes completed tasks

- **Focus Session Management**
  - Start timed focus sessions with tasks
  - Customizable session duration (default: 25 minutes)
  - Session status tracking with progress indicators
  - Option to mark tasks complete when ending sessions
  - Quick start with top-suggested task

- **Configuration System**
  - Customizable weights for priority, effort, and deadline proximity
  - Adjustable default focus session duration
  - Persistent configuration storage
  - Easy configuration viewing and updating

#### CLI Commands
- `flexdo add TITLE [OPTIONS]` - Add a new task
- `flexdo list [OPTIONS]` - List all tasks
- `flexdo show TASK_ID` - Show detailed task information
- `flexdo done TASK_ID` - Mark task as completed
- `flexdo delete TASK_ID` - Delete a task
- `flexdo suggest [OPTIONS]` - Get task suggestions
- `flexdo focus [TASK_ID|--top] [OPTIONS]` - Start a focus session
- `flexdo status` - Check current focus session status
- `flexdo end [OPTIONS]` - End current focus session
- `flexdo config [OPTIONS]` - Configure weights and settings

#### Storage & Persistence
- JSON-based local storage in `~/.flexdo/`
- Tasks stored in `~/.flexdo/tasks.json`
- Configuration stored in `~/.flexdo/config.json`
- No external database required
- Automatic directory creation on first use

#### Testing
- Comprehensive unit test suite
- 20 tests covering all core functionality
- Tests for task model, storage, and session management
- All tests passing

#### Documentation
- Complete README with installation and usage instructions
- Detailed usage examples for various scenarios
- Contributing guide for developers
- Command reference table
- Inline code documentation with docstrings

### Technical Details

#### Dependencies
- Python 3.7+
- Click 8.0.0+ for CLI framework

#### Architecture
- Modular design with separate concerns:
  - `task.py` - Task model and scoring logic
  - `storage.py` - Persistence layer
  - `session.py` - Focus session management
  - `cli.py` - Command-line interface

#### Default Configuration
- Priority weight: 1.0
- Effort weight: 0.5
- Deadline proximity weight: 1.5
- Focus session duration: 25 minutes

### Security
- No known vulnerabilities
- Clean CodeQL security scan
- No external API calls or network dependencies
- All data stored locally

[0.1.0]: https://github.com/jzoubian/flexdo/releases/tag/v0.1.0
