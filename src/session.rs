use crate::config::Config;
use crate::storage::Storage;
use crate::task::SortCriterion;
use anyhow::Result;
use colored::Colorize;
use crossterm::event::{self, Event, KeyCode, KeyEvent};
use std::io::{self, Write};
use std::thread;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy)]
pub enum SessionType {
    Mail,
    Urgent,
    Important,
    Easy,
}

impl SessionType {
    fn name(&self) -> &str {
        match self {
            SessionType::Mail => "Mail/Update",
            SessionType::Urgent => "Urgent Focus",
            SessionType::Important => "Important Focus",
            SessionType::Easy => "Easy Focus",
        }
    }
    
    fn duration_minutes(&self, config: &Config) -> u32 {
        match self {
            SessionType::Mail => config.sessions.mail_duration_minutes,
            _ => config.sessions.focus_duration_minutes,
        }
    }
    
    fn sort_criterion(&self) -> Option<SortCriterion> {
        match self {
            SessionType::Mail => None,
            SessionType::Urgent => Some(SortCriterion::Urgent),
            SessionType::Important => Some(SortCriterion::Important),
            SessionType::Easy => Some(SortCriterion::Easy),
        }
    }
}

pub struct Session {
    session_type: SessionType,
    config: Config,
}

impl Session {
    pub fn new(session_type: SessionType, config: Config) -> Self {
        Self {
            session_type,
            config,
        }
    }
    
    pub fn run(&self, storage: &Storage) -> Result<()> {
        println!("\n{}", format!("🎯 Starting {} Session", self.session_type.name()).bold().cyan());
        println!("{}", format!("Duration: {} minutes", self.session_type.duration_minutes(&self.config)).bright_black());
        println!("{}", "─".repeat(80));
        
        if let SessionType::Mail = self.session_type {
            // Mail session - just run timer
            self.run_timer(self.session_type.duration_minutes(&self.config), "Mail/Update Time")?;
            println!("\n{}", "✓ Mail session completed!".green().bold());
            return Ok(());
        }
        
        // Focus session - select and work on tasks
        loop {
            let mut tasks = storage.get_active_tasks()?;
            
            if tasks.is_empty() {
                println!("\n{}", "No active tasks available. Great job! 🎉".green());
                break;
            }
            
            // Sort tasks by session criterion
            if let Some(criterion) = self.session_type.sort_criterion() {
                criterion.sort_tasks(&mut tasks);
            }
            
            // Display tasks
            println!("\n{}", "Available tasks:".bold());
            println!("{}", "─".repeat(80));
            for (idx, task) in tasks.iter().enumerate() {
                println!("{} {}. {}", 
                         "●".green(),
                         (idx + 1).to_string().bold(),
                         task.description);
                println!("   Urgent: {} | Important: {} | Difficult: {}", 
                         task.urgent, task.important, task.difficult);
            }
            println!("{}", "─".repeat(80));
            
            // Task selection
            println!("\nSelect a task (1-{}) or 'q' to quit: ", tasks.len());
            io::stdout().flush()?;
            
            let mut input = String::new();
            io::stdin().read_line(&mut input)?;
            let input = input.trim();
            
            if input.to_lowercase() == "q" {
                println!("{}", "Session ended.".yellow());
                break;
            }
            
            let task_idx: usize = match input.parse::<usize>() {
                Ok(n) if n > 0 && n <= tasks.len() => n - 1,
                _ => {
                    println!("{}", "Invalid selection. Please try again.".red());
                    continue;
                }
            };
            
            let selected_task = &tasks[task_idx];
            println!("\n{}", format!("Working on: {}", selected_task.description).bold().green());
            
            // Run timer for the task
            self.run_timer(self.session_type.duration_minutes(&self.config), &selected_task.description)?;
            
            // Ask if task is complete
            println!("\n{}", "Is this task complete? (y/n/q to quit session): ".bold());
            io::stdout().flush()?;
            
            let mut response = String::new();
            io::stdin().read_line(&mut response)?;
            let response = response.trim().to_lowercase();
            
            if response == "y" || response == "yes" {
                let mut task_clone = selected_task.clone();
                task_clone.mark_done();
                storage.update_task(selected_task.id, task_clone)?;
                println!("{}", "✓ Task marked as done!".green());
            } else if response == "q" || response == "quit" {
                println!("{}", "Session ended.".yellow());
                break;
            }
            
            println!("\n{}", "Continue with another task? (y/n): ".bold());
            io::stdout().flush()?;
            
            let mut continue_response = String::new();
            io::stdin().read_line(&mut continue_response)?;
            
            if continue_response.trim().to_lowercase() != "y" {
                println!("{}", "Session ended.".yellow());
                break;
            }
        }
        
        Ok(())
    }
    
    fn run_timer(&self, duration_minutes: u32, _task_name: &str) -> Result<()> {
        let duration = Duration::from_secs((duration_minutes * 60) as u64);
        let start = Instant::now();
        
        println!("\n{}", format!("⏱  Timer started: {} minutes", duration_minutes).cyan().bold());
        println!("{}", "Press 'p' to pause, 'r' to resume, 'q' to quit".bright_black());
        println!("{}", "─".repeat(80));
        
        let mut paused = false;
        let mut pause_time = Duration::from_secs(0);
        let mut pause_start: Option<Instant> = None;
        
        loop {
            let now = Instant::now();
            
            // Calculate elapsed time
            let elapsed = if paused {
                now - start - pause_time
            } else if let Some(ps) = pause_start {
                pause_time += now - ps;
                pause_start = Some(now);
                now - start - pause_time
            } else {
                now - start - pause_time
            };
            
            let remaining = if elapsed < duration {
                duration - elapsed
            } else {
                Duration::from_secs(0)
            };
            
            // Display timer
            let mins = remaining.as_secs() / 60;
            let secs = remaining.as_secs() % 60;
            print!("\r⏱  {:02}:{:02} remaining", mins, secs);
            if paused {
                print!(" {}", "[PAUSED]".yellow());
            }
            io::stdout().flush()?;
            
            // Check for completion
            if remaining.as_secs() == 0 {
                println!("\n\n{}", "⏰ Time's up!".green().bold());
                if self.config.sound.enabled {
                    self.play_sound();
                }
                break;
            }
            
            // Check for key input (non-blocking)
            if event::poll(Duration::from_millis(100))? {
                if let Event::Key(KeyEvent { code, .. }) = event::read()? {
                    match code {
                        KeyCode::Char('p') | KeyCode::Char('P') => {
                            if !paused {
                                paused = true;
                                pause_start = Some(Instant::now());
                                println!("\n{}", "⏸  Timer paused".yellow());
                            }
                        }
                        KeyCode::Char('r') | KeyCode::Char('R') => {
                            if paused {
                                if let Some(ps) = pause_start {
                                    pause_time += Instant::now() - ps;
                                    pause_start = None;
                                }
                                paused = false;
                                println!("\n{}", "▶  Timer resumed".green());
                            }
                        }
                        KeyCode::Char('q') | KeyCode::Char('Q') => {
                            println!("\n{}", "Timer stopped.".yellow());
                            return Ok(());
                        }
                        _ => {}
                    }
                }
            }
            
            thread::sleep(Duration::from_millis(100));
        }
        
        Ok(())
    }
    
    fn play_sound(&self) {
        // Try to play a system bell sound
        print!("\x07"); // ASCII bell character
        io::stdout().flush().ok();
        
        // If a custom sound file is configured, try to play it
        if let Some(sound_file) = &self.config.sound.sound_file {
            if let Ok(_) = std::fs::metadata(sound_file) {
                // Try to play the sound file with rodio
                if let Ok((_stream, handle)) = rodio::OutputStream::try_default() {
                    if let Ok(file) = std::fs::File::open(sound_file) {
                        if let Ok(source) = rodio::Decoder::new(std::io::BufReader::new(file)) {
                            let sink = rodio::Sink::try_new(&handle).ok();
                            if let Some(sink) = sink {
                                sink.append(source);
                                sink.sleep_until_end();
                            }
                        }
                    }
                }
            }
        }
    }
}
