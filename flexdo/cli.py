"""Command-line interface for flexdo."""

import click
from datetime import datetime
from .task import Task
from .storage import TaskStorage
from .session import FocusSession


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """flexdo - Flexible daily task management tool.
    
    Plan tasks without fixed times, classify by weighted criteria,
    and manage your day through focused work sessions.
    """
    pass


@cli.command()
@click.argument('title')
@click.option('--description', '-d', default='', help='Task description')
@click.option('--priority', '-p', type=int, default=3, help='Priority (1-5, default: 3)')
@click.option('--effort', '-e', type=int, default=3, help='Effort level (1-5, default: 3)')
@click.option('--deadline', '--due', help='Deadline in YYYY-MM-DD format')
@click.option('--tag', '-t', multiple=True, help='Tags (can be used multiple times)')
def add(title, description, priority, effort, deadline, tag):
    """Add a new task."""
    storage = TaskStorage()
    
    task = Task(
        title=title,
        description=description,
        priority=priority,
        effort=effort,
        deadline=deadline,
        tags=list(tag)
    )
    
    storage.add_task(task)
    click.echo(f"✓ Added task: {task.title}")
    click.echo(f"  ID: {task.task_id}")
    click.echo(f"  Priority: {task.priority}, Effort: {task.effort}")
    if task.deadline:
        click.echo(f"  Deadline: {task.deadline}")


@cli.command('list')
@click.option('--all', '-a', 'show_all', is_flag=True, help='Show completed tasks too')
@click.option('--sort', '-s', type=click.Choice(['score', 'priority', 'deadline', 'created']), 
              default='score', help='Sort order')
def list_tasks(show_all, sort):
    """List all tasks."""
    storage = TaskStorage()
    config = storage.load_config()
    weights = config.get('weights', {})
    
    if show_all:
        tasks = storage.load_tasks()
    else:
        tasks = storage.get_active_tasks()
    
    if not tasks:
        click.echo("No tasks found. Use 'flexdo add' to create one.")
        return
    
    # Sort tasks
    if sort == 'score':
        tasks_with_scores = [(t, t.calculate_score(weights)) for t in tasks]
        tasks_with_scores.sort(key=lambda x: x[1], reverse=True)
        tasks = [t for t, _ in tasks_with_scores]
    elif sort == 'priority':
        tasks.sort(key=lambda t: t.priority, reverse=True)
    elif sort == 'deadline':
        tasks.sort(key=lambda t: t.deadline or '9999-99-99')
    elif sort == 'created':
        tasks.sort(key=lambda t: t.created_at)
    
    click.echo(f"\n{'Status':<8} {'Priority':<9} {'Effort':<7} {'Deadline':<12} {'Title':<40} {'ID':<15}")
    click.echo("=" * 100)
    
    for task in tasks:
        status = "✓ Done" if task.completed else "○ Active"
        deadline_str = task.deadline or "-"
        title = task.title[:37] + "..." if len(task.title) > 40 else task.title
        
        if sort == 'score':
            score = task.calculate_score(weights)
            click.echo(f"{status:<8} P:{task.priority}({score:4.1f}) E:{task.effort:<6} {deadline_str:<12} {title:<40} {task.task_id}")
        else:
            click.echo(f"{status:<8} P:{task.priority:<7} E:{task.effort:<6} {deadline_str:<12} {title:<40} {task.task_id}")
    
    click.echo(f"\nTotal: {len(tasks)} task(s)")


@cli.command()
@click.argument('task_id')
def show(task_id):
    """Show detailed information about a task."""
    storage = TaskStorage()
    task = storage.get_task(task_id)
    
    if not task:
        click.echo(f"Error: Task {task_id} not found.")
        return
    
    click.echo(f"\nTask: {task.title}")
    click.echo("=" * 60)
    click.echo(f"ID:          {task.task_id}")
    click.echo(f"Status:      {'Completed' if task.completed else 'Active'}")
    click.echo(f"Priority:    {task.priority}/5")
    click.echo(f"Effort:      {task.effort}/5")
    if task.deadline:
        click.echo(f"Deadline:    {task.deadline}")
    if task.description:
        click.echo(f"Description: {task.description}")
    if task.tags:
        click.echo(f"Tags:        {', '.join(task.tags)}")
    click.echo(f"Created:     {task.created_at}")
    
    # Show calculated score
    config = storage.load_config()
    weights = config.get('weights', {})
    score = task.calculate_score(weights)
    click.echo(f"Score:       {score:.2f}")


@cli.command()
@click.argument('task_id')
def done(task_id):
    """Mark a task as completed."""
    storage = TaskStorage()
    task = storage.get_task(task_id)
    
    if not task:
        click.echo(f"Error: Task {task_id} not found.")
        return
    
    task.completed = True
    storage.update_task(task)
    click.echo(f"✓ Marked as completed: {task.title}")


@cli.command()
@click.argument('task_id')
def delete(task_id):
    """Delete a task."""
    storage = TaskStorage()
    task = storage.get_task(task_id)
    
    if not task:
        click.echo(f"Error: Task {task_id} not found.")
        return
    
    if click.confirm(f"Delete task '{task.title}'?"):
        storage.delete_task(task_id)
        click.echo(f"✓ Deleted task: {task.title}")


@cli.command()
@click.option('--limit', '-n', type=int, default=5, help='Number of tasks to suggest')
def suggest(limit):
    """Suggest tasks based on weighted criteria."""
    storage = TaskStorage()
    session = FocusSession(storage)
    
    suggestions = session.suggest_tasks(limit=limit)
    
    if not suggestions:
        click.echo("No active tasks found. Use 'flexdo add' to create one.")
        return
    
    click.echo("\n🎯 Suggested tasks (highest priority first):\n")
    click.echo(f"{'Rank':<6} {'Score':<8} {'Priority':<10} {'Effort':<8} {'Deadline':<12} {'Title'}")
    click.echo("=" * 80)
    
    for i, (task, score) in enumerate(suggestions, 1):
        deadline_str = task.deadline or "-"
        title = task.title[:40] + "..." if len(task.title) > 43 else task.title
        click.echo(f"#{i:<5} {score:<7.1f} P:{task.priority:<8} E:{task.effort:<7} {deadline_str:<12} {title}")
        click.echo(f"       ID: {task.task_id}")
        if task.description:
            desc = task.description[:70] + "..." if len(task.description) > 73 else task.description
            click.echo(f"       {desc}")
        click.echo()


@cli.command()
@click.argument('task_id', required=False)
@click.option('--duration', '-d', type=int, help='Session duration in minutes')
@click.option('--top', is_flag=True, help='Start session with top suggested task')
def focus(task_id, duration, top):
    """Start a focus session for a task."""
    storage = TaskStorage()
    session_mgr = FocusSession(storage)
    
    # Get the task
    if top:
        suggestions = session_mgr.suggest_tasks(limit=1)
        if not suggestions:
            click.echo("No active tasks found.")
            return
        task = suggestions[0][0]
    elif task_id:
        task = storage.get_task(task_id)
        if not task:
            click.echo(f"Error: Task {task_id} not found.")
            return
    else:
        click.echo("Error: Provide a task ID or use --top to work on the top suggested task.")
        click.echo("Use 'flexdo suggest' to see suggested tasks.")
        return
    
    # Start the session
    session_info = session_mgr.start_session(task, duration)
    
    click.echo(f"\n🎯 Focus session started!")
    click.echo(f"Task: {task.title}")
    click.echo(f"Duration: {session_info['duration_minutes']} minutes")
    click.echo(f"End time: {session_info['end_time'].strftime('%H:%M')}")
    click.echo(f"\nStay focused! Use 'flexdo status' to check progress.")
    click.echo(f"When done, use 'flexdo end' to finish the session.")


@cli.command()
def status():
    """Show current focus session status."""
    storage = TaskStorage()
    session_mgr = FocusSession(storage)
    
    status = session_mgr.get_session_status()
    
    if not status:
        click.echo("No active focus session.")
        click.echo("Use 'flexdo focus' to start one.")
        return
    
    task = status['task']
    elapsed = status['elapsed_minutes']
    remaining = status['remaining_minutes']
    
    click.echo(f"\n⏱️  Focus Session Status")
    click.echo("=" * 60)
    click.echo(f"Task:      {task.title}")
    click.echo(f"Elapsed:   {int(elapsed)} minutes")
    click.echo(f"Remaining: {int(remaining)} minutes")
    
    if status['is_complete']:
        click.echo("\n✓ Session complete! Use 'flexdo end' to finish.")
    else:
        # Show progress bar
        total = elapsed + remaining
        progress = int((elapsed / total) * 20) if total > 0 else 0
        bar = "█" * progress + "░" * (20 - progress)
        click.echo(f"Progress:  [{bar}] {int(elapsed)}/{int(total)} min")


@cli.command()
@click.option('--complete', '-c', is_flag=True, help='Mark task as completed')
def end(complete):
    """End the current focus session."""
    storage = TaskStorage()
    session_mgr = FocusSession(storage)
    
    summary = session_mgr.end_session(mark_complete=complete)
    
    if 'error' in summary:
        click.echo("No active focus session.")
        return
    
    task = summary['task']
    elapsed = int(summary['elapsed_minutes'])
    
    click.echo(f"\n✓ Focus session ended!")
    click.echo(f"Task: {task.title}")
    click.echo(f"Duration: {elapsed} minutes")
    
    if summary['completed']:
        click.echo(f"Status: Marked as completed ✓")
    else:
        click.echo(f"Status: Still active (use 'flexdo done {task.task_id}' to mark as complete)")


@cli.command()
@click.option('--priority', '-p', type=float, help='Weight for priority (default: 1.0)')
@click.option('--effort', '-e', type=float, help='Weight for effort (default: 0.5)')
@click.option('--deadline', '-d', type=float, help='Weight for deadline proximity (default: 1.5)')
@click.option('--session-duration', '-s', type=int, help='Default focus session duration in minutes')
@click.option('--show', is_flag=True, help='Show current configuration')
def config(priority, effort, deadline, session_duration, show):
    """Configure weights for task scoring."""
    storage = TaskStorage()
    current_config = storage.load_config()
    
    if show:
        click.echo("\nCurrent Configuration:")
        click.echo("=" * 60)
        click.echo("Weights for task scoring:")
        weights = current_config.get('weights', {})
        click.echo(f"  Priority:           {weights.get('priority', 1.0)}")
        click.echo(f"  Effort:             {weights.get('effort', 0.5)}")
        click.echo(f"  Deadline Proximity: {weights.get('deadline_proximity', 1.5)}")
        click.echo(f"\nFocus session duration: {current_config.get('focus_session_duration', 25)} minutes")
        return
    
    # Update configuration
    weights = current_config.get('weights', {})
    
    if priority is not None:
        weights['priority'] = priority
    if effort is not None:
        weights['effort'] = effort
    if deadline is not None:
        weights['deadline_proximity'] = deadline
    
    current_config['weights'] = weights
    
    if session_duration is not None:
        current_config['focus_session_duration'] = session_duration
    
    storage.save_config(current_config)
    click.echo("✓ Configuration updated!")
    
    # Show updated config
    click.echo("\nUpdated Configuration:")
    click.echo("=" * 60)
    click.echo("Weights for task scoring:")
    click.echo(f"  Priority:           {weights.get('priority', 1.0)}")
    click.echo(f"  Effort:             {weights.get('effort', 0.5)}")
    click.echo(f"  Deadline Proximity: {weights.get('deadline_proximity', 1.5)}")
    click.echo(f"\nFocus session duration: {current_config.get('focus_session_duration', 25)} minutes")


if __name__ == '__main__':
    cli()
