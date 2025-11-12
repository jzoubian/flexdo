use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "flexdo")]
#[command(about = "A flexible command-line task manager with priority-driven focus sessions", long_about = None)]
#[command(version)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Add a new task
    Add {
        /// Task description
        description: String,
        
        /// Urgency level (0-10)
        #[arg(short, long, default_value_t = 5)]
        urgent: u8,
        
        /// Importance level (0-10)
        #[arg(short, long, default_value_t = 5)]
        important: u8,
        
        /// Difficulty level (0-10)
        #[arg(short, long, default_value_t = 5)]
        difficult: u8,
    },
    
    /// List tasks
    List {
        /// Sort by criterion
        #[arg(short, long, default_value = "urgent")]
        sort: String,
        
        /// Show all tasks including completed ones
        #[arg(short, long, default_value_t = false)]
        all: bool,
    },
    
    /// Mark a task as done
    Done {
        /// Task ID (or partial ID)
        task_id: String,
    },
    
    /// Cancel a task
    Cancel {
        /// Task ID (or partial ID)
        task_id: String,
    },
    
    /// Postpone a task
    Postpone {
        /// Task ID (or partial ID)
        task_id: String,
    },
    
    /// Edit a task
    Edit {
        /// Task ID (or partial ID)
        task_id: String,
        
        /// New task description
        #[arg(short, long)]
        description: Option<String>,
        
        /// New urgency level (0-10)
        #[arg(short, long)]
        urgent: Option<u8>,
        
        /// New importance level (0-10)
        #[arg(short, long)]
        important: Option<u8>,
        
        /// New difficulty level (0-10)
        #[arg(short = 'f', long)]
        difficult: Option<u8>,
    },
    
    /// Delete a task permanently
    Delete {
        /// Task ID (or partial ID)
        task_id: String,
    },
    
    /// Start a focus session
    Start {
        /// Session type: mail, urgent, important, or easy
        session_type: String,
    },
}
