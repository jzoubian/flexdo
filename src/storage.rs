use crate::task::{Task, TaskStatus};
use anyhow::{Context, Result};
use std::fs;
use std::path::PathBuf;
use uuid::Uuid;

const FLEXDO_DIR: &str = ".flexdo";
const DEFAULT_STORAGE_FILE: &str = "tasks.json";

pub struct Storage {
    file_path: PathBuf,
}

impl Storage {
    pub fn new(file_path: Option<PathBuf>) -> Self {
        let file_path = file_path.unwrap_or_else(|| {
            let mut path = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
            path.push(FLEXDO_DIR);
            
            // Create .flexdo directory if it doesn't exist
            if !path.exists() {
                fs::create_dir_all(&path).ok();
            }
            
            path.push(DEFAULT_STORAGE_FILE);
            path
        });
        
        Self { file_path }
    }

    pub fn load_tasks(&self) -> Result<Vec<Task>> {
        if !self.file_path.exists() {
            return Ok(Vec::new());
        }

        let contents = fs::read_to_string(&self.file_path)
            .context("Failed to read tasks file")?;
        
        let tasks: Vec<Task> = serde_json::from_str(&contents)
            .context("Failed to parse tasks JSON")?;
        
        Ok(tasks)
    }

    pub fn save_tasks(&self, tasks: &[Task]) -> Result<()> {
        let json = serde_json::to_string_pretty(tasks)
            .context("Failed to serialize tasks")?;
        
        fs::write(&self.file_path, json)
            .context("Failed to write tasks file")?;
        
        Ok(())
    }

    pub fn add_task(&self, task: Task) -> Result<()> {
        let mut tasks = self.load_tasks()?;
        tasks.push(task);
        self.save_tasks(&tasks)
    }

    pub fn get_task(&self, id: Uuid) -> Result<Option<Task>> {
        let tasks = self.load_tasks()?;
        Ok(tasks.into_iter().find(|t| t.id == id))
    }

    pub fn update_task(&self, id: Uuid, updated_task: Task) -> Result<bool> {
        let mut tasks = self.load_tasks()?;
        
        if let Some(pos) = tasks.iter().position(|t| t.id == id) {
            tasks[pos] = updated_task;
            self.save_tasks(&tasks)?;
            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub fn delete_task(&self, id: Uuid) -> Result<bool> {
        let mut tasks = self.load_tasks()?;
        let original_len = tasks.len();
        
        tasks.retain(|t| t.id != id);
        
        if tasks.len() < original_len {
            self.save_tasks(&tasks)?;
            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub fn get_active_tasks(&self) -> Result<Vec<Task>> {
        let tasks = self.load_tasks()?;
        Ok(tasks.into_iter()
            .filter(|t| t.status == TaskStatus::Active)
            .collect())
    }

    pub fn get_all_tasks(&self) -> Result<Vec<Task>> {
        self.load_tasks()
    }
}
