# FlexDo Usage Examples

This document provides practical examples of using flexdo for various scenarios.

## Scenario 1: Busy Developer with Changing Priorities

### Morning: Planning Your Day

```bash
# Start fresh - check what's on your plate
$ flexdo list

# Add urgent tasks as they come in
$ flexdo add "Fix production bug" -p 5 -e 2 --deadline 2025-11-12 --tag urgent --tag bugfix
$ flexdo add "Review team's PRs" -p 3 -e 1 --tag review
$ flexdo add "Update API documentation" -p 4 -e 3 --deadline 2025-11-15 --tag docs

# Get smart suggestions on what to tackle first
$ flexdo suggest --limit 3
```

### Working Through Tasks

```bash
# Start a focus session with the top priority task
$ flexdo focus --top --duration 25

# Check progress during the session
$ flexdo status

# Complete the session and mark task as done
$ flexdo end --complete

# Next task
$ flexdo suggest --limit 1
$ flexdo focus <task_id> --duration 30
```

### End of Day

```bash
# See what you accomplished
$ flexdo list --all

# Add tomorrow's tasks
$ flexdo add "Team standup prep" -p 3 -e 1 --deadline 2025-11-13
```

## Scenario 2: Project Manager Juggling Multiple Projects

### Setting Up Projects

```bash
# Project A - High Priority
$ flexdo add "Design system architecture" -p 5 -e 4 --deadline 2025-11-20 --tag project-a --tag architecture
$ flexdo add "Define API endpoints" -p 5 -e 3 --deadline 2025-11-22 --tag project-a --tag api

# Project B - Medium Priority
$ flexdo add "Update project roadmap" -p 3 -e 2 --deadline 2025-11-25 --tag project-b --tag planning
$ flexdo add "Client meeting prep" -p 4 -e 1 --deadline 2025-11-18 --tag project-b --tag meeting

# Administrative Tasks
$ flexdo add "Approve timesheets" -p 2 -e 1 --deadline 2025-11-15 --tag admin
```

### Viewing by Different Criteria

```bash
# See everything by deadline
$ flexdo list --sort deadline

# See by priority alone
$ flexdo list --sort priority

# Get intelligent suggestions (considers all factors)
$ flexdo suggest
```

## Scenario 3: Optimizing for Quick Wins

### Adjust Configuration for Quick Tasks

```bash
# Configure to heavily favor low-effort tasks
$ flexdo config --effort 2.0 --priority 1.0 --deadline 0.5

# Now quick tasks will rank higher
$ flexdo suggest --limit 5
```

## Scenario 4: Deadline-Driven Work

### Configure for Deadline Focus

```bash
# Heavily prioritize approaching deadlines
$ flexdo config --deadline 3.0 --priority 1.0 --effort 0.3

# Add tasks with various deadlines
$ flexdo add "Urgent report" -p 3 -e 3 --deadline 2025-11-13
$ flexdo add "Weekly review" -p 4 -e 2 --deadline 2025-11-20
$ flexdo add "Monthly planning" -p 3 -e 4 --deadline 2025-11-30

# Suggestions will prioritize by deadline proximity
$ flexdo suggest
```

## Scenario 5: Daily Routine with Focus Sessions

### Morning Routine

```bash
# Review yesterday's incomplete tasks
$ flexdo list

# Plan focus blocks for the day
$ flexdo suggest --limit 5

# First 25-minute pomodoro
$ flexdo focus --top --duration 25

# After the session
$ flexdo end --complete

# Short break, then continue
$ flexdo focus --top --duration 25
```

### Tracking Progress

```bash
# Check active session
$ flexdo status

# View completed vs pending
$ flexdo list --all
```

## Scenario 6: Handling Interruptions

```bash
# Working on a task when something urgent comes up
$ flexdo end  # End current session without marking complete

# Add the urgent task
$ flexdo add "Emergency production fix" -p 5 -e 1 --deadline 2025-11-12 --tag urgent

# Start new session with urgent task
$ flexdo suggest --limit 1
$ flexdo focus --top --duration 15

# When done, return to previous workflow
$ flexdo suggest
```

## Scenario 7: Weekly Planning

```bash
# Monday: Add all weekly tasks
$ flexdo add "Design review meeting" -p 4 -e 1 --deadline 2025-11-13 --tag meeting
$ flexdo add "Code sprint tasks" -p 5 -e 5 --deadline 2025-11-15 --tag development
$ flexdo add "Write blog post" -p 3 -e 3 --deadline 2025-11-17 --tag content
$ flexdo add "Team 1-on-1s" -p 4 -e 2 --deadline 2025-11-16 --tag meeting

# Get a weekly overview
$ flexdo list --sort deadline

# Each day, get fresh suggestions
$ flexdo suggest
```

## Pro Tips

### 1. Using Task IDs Efficiently

```bash
# List to see IDs
$ flexdo list

# Copy-paste the ID for operations
$ flexdo show 20251112112037055102
$ flexdo done 20251112112037055102
```

### 2. Customizing Focus Duration

```bash
# Short focused bursts
$ flexdo focus --top --duration 15

# Deep work session
$ flexdo focus --top --duration 90

# Change default for all sessions
$ flexdo config --session-duration 30
```

### 3. Finding the Right Weight Balance

```bash
# View current weights
$ flexdo config --show

# Experiment with different values
$ flexdo config --priority 1.5 --effort 0.8 --deadline 2.0
$ flexdo suggest  # See how rankings change

# Reset to defaults by setting values explicitly
$ flexdo config --priority 1.0 --effort 0.5 --deadline 1.5
```

### 4. Task Management Best Practices

```bash
# Be specific with priorities (1=lowest, 5=highest)
# - 5: Critical, blocks others
# - 4: High priority, due soon
# - 3: Normal work
# - 2: Nice to have
# - 1: Backlog

# Estimate effort realistically (1=very easy, 5=very hard)
# - 1: < 30 minutes
# - 2: 30min - 1 hour  
# - 3: 1-2 hours
# - 4: 2-4 hours
# - 5: > 4 hours or multi-day

# Use tags for categorization
$ flexdo add "Task" --tag frontend --tag bugfix --tag urgent
```

## Integration Examples

### With Git Workflow

```bash
# Start work on an issue
$ git checkout -b feature/new-feature
$ flexdo add "Implement new feature" -p 4 -e 4 --tag feature
$ flexdo focus --top --duration 45

# After completing a focus session
$ git add . && git commit -m "Feature progress"
$ flexdo end

# Task not complete? Continue later
$ flexdo focus <task_id> --duration 30

# Task complete?
$ flexdo end --complete
$ git push origin feature/new-feature
```

### End of Sprint Review

```bash
# See all completed tasks
$ flexdo list --all | grep "✓ Done"

# Or count completions
$ flexdo list --all | grep -c "✓ Done"

# Review what's still pending
$ flexdo list
```
