mod task;
mod storage;
mod cli;
mod commands;
mod session;
mod config;

use clap::Parser;
use cli::{Cli, Commands};
use anyhow::Result;

fn main() -> Result<()> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Add { description, urgent, important, difficult } => {
            commands::add_task(description, urgent, important, difficult)?;
        }
        Commands::List { sort, all } => {
            commands::list_tasks(&sort, all)?;
        }
        Commands::Done { task_id } => {
            commands::mark_task_done(&task_id)?;
        }
        Commands::Cancel { task_id } => {
            commands::mark_task_cancelled(&task_id)?;
        }
        Commands::Postpone { task_id } => {
            commands::mark_task_postponed(&task_id)?;
        }
        Commands::Edit { task_id, description, urgent, important, difficult } => {
            commands::edit_task(&task_id, description, urgent, important, difficult)?;
        }
        Commands::Delete { task_id } => {
            commands::delete_task(&task_id)?;
        }
        Commands::Start { session_type } => {
            commands::start_session(&session_type)?;
        }
    }
    
    Ok(())
}
