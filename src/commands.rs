use crate::storage::Storage;
use crate::task::{SortCriterion, Task, TaskStatus};
use crate::session::{Session, SessionType};
use crate::config::Config;
use anyhow::{anyhow, Result};
use colored::Colorize;
use uuid::Uuid;

pub fn add_task(description: String, urgent: u8, important: u8, difficult: u8) -> Result<()> {
    // Validate input ranges
    if urgent > 10 || important > 10 || difficult > 10 {
        return Err(anyhow!("All values must be between 0 and 10"));
    }
    
    let task = Task::new(description, urgent, important, difficult);
    let storage = Storage::new(None);
    
    storage.add_task(task.clone())?;
    
    println!("{}", "✓ Task added successfully!".green());
    println!("  ID: {}", task.id.to_string().bright_black());
    println!("  Description: {}", task.description);
    println!("  Urgent: {} | Important: {} | Difficult: {}", 
             task.urgent, task.important, task.difficult);
    
    Ok(())
}

pub fn list_tasks(sort: &str, all: bool) -> Result<()> {
    let storage = Storage::new(None);
    let mut tasks = if all {
        storage.get_all_tasks()?
    } else {
        storage.get_active_tasks()?
    };
    
    if tasks.is_empty() {
        println!("{}", "No tasks found.".yellow());
        return Ok(());
    }
    
    let criterion = match sort.to_lowercase().as_str() {
        "urgent" => SortCriterion::Urgent,
        "important" => SortCriterion::Important,
        "difficult" => SortCriterion::Difficult,
        "easy" => SortCriterion::Easy,
        _ => return Err(anyhow!("Invalid sort criterion. Use: urgent, important, difficult, or easy")),
    };
    
    criterion.sort_tasks(&mut tasks);
    
    println!("\n{}", format!("Tasks (sorted by {}):", sort).bold());
    println!("{}", "─".repeat(80));
    
    for (idx, task) in tasks.iter().enumerate() {
        let status_str = match task.status {
            TaskStatus::Active => "●".green(),
            TaskStatus::Done => "✓".bright_black(),
            TaskStatus::Cancelled => "✗".red(),
            TaskStatus::Postponed => "⏸".yellow(),
        };
        
        println!("\n{} {}. {}", 
                 status_str,
                 (idx + 1).to_string().bold(),
                 task.description.bold());
        println!("   ID: {}", task.id.to_string().bright_black());
        println!("   Urgent: {} | Important: {} | Difficult: {}", 
                 colorize_value(task.urgent), 
                 colorize_value(task.important), 
                 colorize_value(task.difficult));
        println!("   Status: {:?} | Created: {}", 
                 task.status, 
                 task.created_at.format("%Y-%m-%d %H:%M"));
    }
    
    println!("\n{}", "─".repeat(80));
    println!("Total: {} tasks\n", tasks.len());
    
    Ok(())
}

pub fn mark_task_done(task_id: &str) -> Result<()> {
    update_task_status(task_id, TaskStatus::Done, "done")
}

pub fn mark_task_cancelled(task_id: &str) -> Result<()> {
    update_task_status(task_id, TaskStatus::Cancelled, "cancelled")
}

pub fn mark_task_postponed(task_id: &str) -> Result<()> {
    update_task_status(task_id, TaskStatus::Postponed, "postponed")
}

pub fn edit_task(
    task_id: &str,
    description: Option<String>,
    urgent: Option<u8>,
    important: Option<u8>,
    difficult: Option<u8>,
) -> Result<()> {
    let storage = Storage::new(None);
    let uuid = find_task_by_partial_id(&storage, task_id)?;
    
    let mut task = storage.get_task(uuid)?
        .ok_or_else(|| anyhow!("Task not found"))?;
    
    task.update(description, urgent, important, difficult);
    storage.update_task(uuid, task.clone())?;
    
    println!("{}", "✓ Task updated successfully!".green());
    println!("  Description: {}", task.description);
    println!("  Urgent: {} | Important: {} | Difficult: {}", 
             task.urgent, task.important, task.difficult);
    
    Ok(())
}

pub fn delete_task(task_id: &str) -> Result<()> {
    let storage = Storage::new(None);
    let uuid = find_task_by_partial_id(&storage, task_id)?;
    
    let task = storage.get_task(uuid)?
        .ok_or_else(|| anyhow!("Task not found"))?;
    
    println!("Are you sure you want to delete this task?");
    println!("  {}", task.description);
    println!("Type 'yes' to confirm: ");
    
    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;
    
    if input.trim().to_lowercase() == "yes" {
        storage.delete_task(uuid)?;
        println!("{}", "✓ Task deleted successfully!".green());
    } else {
        println!("{}", "Delete cancelled.".yellow());
    }
    
    Ok(())
}

pub fn start_session(session_type: &str) -> Result<()> {
    let config = Config::load()?;
    let storage = Storage::new(None);
    
    let session_type = match session_type.to_lowercase().as_str() {
        "mail" => SessionType::Mail,
        "urgent" => SessionType::Urgent,
        "important" => SessionType::Important,
        "easy" => SessionType::Easy,
        _ => return Err(anyhow!("Invalid session type. Use: mail, urgent, important, or easy")),
    };
    
    let session = Session::new(session_type, config);
    session.run(&storage)?;
    
    Ok(())
}

// Helper functions

fn update_task_status(task_id: &str, status: TaskStatus, status_name: &str) -> Result<()> {
    let storage = Storage::new(None);
    let uuid = find_task_by_partial_id(&storage, task_id)?;
    
    let mut task = storage.get_task(uuid)?
        .ok_or_else(|| anyhow!("Task not found"))?;
    
    match status {
        TaskStatus::Done => task.mark_done(),
        TaskStatus::Cancelled => task.mark_cancelled(),
        TaskStatus::Postponed => task.mark_postponed(),
        _ => {}
    }
    
    storage.update_task(uuid, task.clone())?;
    
    println!("{}", format!("✓ Task marked as {}!", status_name).green());
    println!("  {}", task.description);
    
    Ok(())
}

fn find_task_by_partial_id(storage: &Storage, partial_id: &str) -> Result<Uuid> {
    // Try to parse as full UUID first
    if let Ok(uuid) = Uuid::parse_str(partial_id) {
        return Ok(uuid);
    }
    
    // Otherwise search for partial match
    let tasks = storage.get_all_tasks()?;
    let matches: Vec<&Task> = tasks.iter()
        .filter(|t| t.id.to_string().starts_with(partial_id))
        .collect();
    
    match matches.len() {
        0 => Err(anyhow!("No task found with ID starting with '{}'", partial_id)),
        1 => Ok(matches[0].id),
        _ => Err(anyhow!("Ambiguous ID '{}'. Multiple tasks match. Please provide more characters.", partial_id)),
    }
}

fn colorize_value(value: u8) -> colored::ColoredString {
    let s = value.to_string();
    match value {
        0..=3 => s.green(),
        4..=6 => s.yellow(),
        7..=10 => s.red(),
        _ => s.normal(),
    }
}
