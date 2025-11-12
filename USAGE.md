# FlexDo - Flexible CLI Task Manager

A command-line tool for flexible daily task management, focusing on adaptive scheduling and priority-driven focus sessions.

## Installation

### Set up environment with Nix

```bash
# Enter the development environment
nix-shell
```

If you don't have Nix installed, follow the instructions at https://nixos.org/download.html or install the dependency manually.

### Build and Install with Cargo

```bash
# Build the project
cargo build --release

# Install
cargo install --path .

# Set up your shell to find the installed binary
export PATH="$HOME/.cargo/bin:$PATH"

# Verify installation
flexdo --help
```

## Usage

### Task Management

#### Add a new task
```bash
flexdo add "Write project report" --urgent 4 --important 5 --difficult 3
```

Parameters:
- `--urgent` or `-u`: Urgency level (0-10, default: 5)
- `--important` or `-i`: Importance level (0-10, default: 5)
- `--difficult` or `-d`: Difficulty level (0-10, default: 5)

#### List tasks
```bash
# List active tasks sorted by urgency
flexdo list --sort urgent

# List all tasks (including completed) sorted by importance
flexdo list --all --sort important

# Available sort options: urgent, important, difficult, easy
```

#### Mark a task as done
```bash
# Use full or partial task ID
flexdo done c0d64910
```

#### Cancel a task
```bash
flexdo cancel 8b44c5d8
```

#### Postpone a task
```bash
flexdo postpone 05f22712
```

#### Edit a task
```bash
flexdo edit c0d64910 --description "Updated description" --urgent 7
```

#### Delete a task permanently
```bash
flexdo delete c0d64910
```

### Focus Sessions

FlexDo helps you manage your day through focused work sessions:

#### Mail/Update Session (30 min default)
```bash
flexdo start mail
```
A short session for checking emails and updates.

#### Urgent Session (2 hours default)
```bash
flexdo start urgent
```
Focus on urgent tasks, sorted by urgency level.

#### Important Session (2 hours default)
```bash
flexdo start important
```
Focus on important tasks, sorted by importance level.

#### Easy Session (2 hours default)
```bash
flexdo start easy
```
Focus on easier tasks, sorted by difficulty (lowest first).

### Session Features

During a focus session:
- **Task Selection**: Choose which task to work on from a prioritized list
- **Timer**: Built-in timer with visual countdown
- **Pause/Resume**: Press 'p' to pause, 'r' to resume
- **Sound Alert**: Get notified when time is up (configurable)
- **Task Completion**: Mark tasks as done within the session
- **Continue or Exit**: Choose to work on another task or end the session

## Configuration

FlexDo creates a configuration directory in your home directory: `~/.flexdo/`

The configuration file is stored at: `~/.flexdo/config.toml`

Example configuration:

```toml
[sessions]
mail_duration_minutes = 30
focus_duration_minutes = 120

[sound]
enabled = true
# sound_file = "/path/to/custom/sound.mp3"  # Optional
```

You can edit this file to customize:
- Session durations
- Sound alerts on/off
- Custom sound file for timer alerts

## Data Storage

Tasks are stored in `~/.flexdo/tasks.json` as a JSON file. This makes it easy to:
- Backup your tasks
- Sync across machines
- Export or analyze your task history

## Examples

### Typical Daily Workflow

```bash
# Morning: Add your tasks for the day
flexdo add "Fix critical bug in production" --urgent 9 --important 8 --difficult 6
flexdo add "Review pull requests" --urgent 5 --important 6 --difficult 3
flexdo add "Update documentation" --urgent 3 --important 4 --difficult 2
flexdo add "Plan next sprint" --urgent 4 --important 7 --difficult 4

# Start with a mail session
flexdo start mail

# First focus session: tackle urgent tasks
flexdo start urgent

# Second focus session: work on important tasks
flexdo start important

# Third focus session: complete easier tasks
flexdo start easy

# Review what's left
flexdo list
```

### Check Your Progress

```bash
# See all tasks including completed ones
flexdo list --all

# See only active tasks sorted by difficulty
flexdo list --sort difficult
```

## Features

✅ Flexible task management without fixed schedules  
✅ Multi-criteria task classification (urgent, important, difficult)  
✅ Timed focus sessions with pause/resume  
✅ Sound notifications  
✅ Task status tracking (active, done, cancelled, postponed)  
✅ Partial ID matching for quick commands  
✅ Colored terminal output for better visibility  
✅ JSON-based storage for easy backup and portability  
✅ TOML configuration for customization  

## Requirements

- Rust 1.70 or later
- ALSA libraries (Linux) for sound support
- NixOS or Nix package manager (optional, recommended)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details.

## Authors

This code was developed by Julien Zoubian with the assistance of GitHub Copilot Agent and Claude AI for editing, structure, and formatting — under Julien Zoubian's full supervision and revision.
