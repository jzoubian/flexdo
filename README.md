# FlexDo — Flexible CLI Task Manager

## Project Goal
Develop a command-line tool for flexible daily task management, focusing on adaptive scheduling and priority-driven focus sessions.

## Core Concepts
My schedule changes daily, but I always know the tasks I need to complete. The tool must help me:
- Plan tasks without assigning them fixed times in advance.
- Classify tasks by multiple weighted criteria.
- Manage my day through focused work sessions.

## Features

### Task Management
- **Add / remove / edit tasks**
- **Mark tasks** as `done`, `cancelled`, or `postponed`
- **List tasks** ordered by chosen criteria (urgent, important, difficult)
- **Tasks stored locally** in a JSON or SQLite database

### Classification
Each task has 3 attributes:
- `Urgent`
- `Important`
- `Difficult`
→ These attributes should be numeric or categorical and **parametrizable**.

### Sessions
I want **3 focus sessions per day**, each 2h long:
1. Urgent session — focus on urgent tasks
2. Important session — focus on important tasks
3. Easy session — focus on less difficult tasks

Each session:
- Starts with a **mail/update session** (30min)
- Lists tasks ordered by the session’s focus criterion
- Allows selecting one task
- Starts a **timer**
- Supports **pause/resume**
- If the task is done before time is up → list tasks again and choose the next
- Plays a **sound** when the timer ends

All durations and focus types must be configurable.

### Commands
| Command | Description |
|----------|-------------|
| `flexdo add "task description" --urgent 3 --important 5 --difficult 2` | Add a task |
| `flexdo list --sort important` | List tasks sorted by criterion |
| `flexdo done <task_id>` | Mark a task done |
| `flexdo cancel <task_id>` | Cancel a task |
| `flexdo postpone <task_id>` | Postpone a task |
| `flexdo start mail` | Start a 30min mail/update session |
| `flexdo start urgent` | Start a 2h urgent session |
| `flexdo start important` | Start a 2h important session |
| `flexdo start easy` | Start a 2h easy session |

### Technical Goals
- Implemented in **Python** (e.g. using `click` or `typer` for CLI)
- Local **JSON or SQLite** database for persistence
- **Config file (YAML or TOML)** for session parameters
- Use **asyncio** or threading for timers
- Optionally play sounds with `playsound` or similar library

### Stretch Goals
- Export daily logs to Markdown or CSV
- Show daily report or stats (time spent per criterion)
- Support interactive TUI (e.g. with `textual` or `rich`)

---

## Development Steps
1. Initialize Python project with CLI framework (`typer` preferred)
2. Implement task model + local storage
3. Implement commands (`add`, `list`, `done`, etc.)
4. Implement session logic with timers and sound alerts
5. Add configuration file for durations and weights
6. Polish CLI help and formatting
7. Add tests and docs

---

## Example
```bash
# Add a task
flexdo add "Write project report" --urgent 4 --important 5 --difficult 3

# List tasks by urgency
flexdo list --sort urgent

# Start an urgent session
flexdo start urgent
```
