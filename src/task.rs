use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum TaskStatus {
    Active,
    Done,
    Cancelled,
    Postponed,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: Uuid,
    pub description: String,
    pub urgent: u8,
    pub important: u8,
    pub difficult: u8,
    pub status: TaskStatus,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Task {
    pub fn new(description: String, urgent: u8, important: u8, difficult: u8) -> Self {
        let now = Utc::now();
        Self {
            id: Uuid::new_v4(),
            description,
            urgent,
            important,
            difficult,
            status: TaskStatus::Active,
            created_at: now,
            updated_at: now,
        }
    }

    pub fn mark_done(&mut self) {
        self.status = TaskStatus::Done;
        self.updated_at = Utc::now();
    }

    pub fn mark_cancelled(&mut self) {
        self.status = TaskStatus::Cancelled;
        self.updated_at = Utc::now();
    }

    pub fn mark_postponed(&mut self) {
        self.status = TaskStatus::Postponed;
        self.updated_at = Utc::now();
    }

    pub fn update(&mut self, description: Option<String>, urgent: Option<u8>, important: Option<u8>, difficult: Option<u8>) {
        if let Some(desc) = description {
            self.description = desc;
        }
        if let Some(u) = urgent {
            self.urgent = u;
        }
        if let Some(i) = important {
            self.important = i;
        }
        if let Some(d) = difficult {
            self.difficult = d;
        }
        self.updated_at = Utc::now();
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SortCriterion {
    Urgent,
    Important,
    Difficult,
    Easy,
}

impl SortCriterion {
    pub fn sort_tasks(&self, tasks: &mut Vec<Task>) {
        match self {
            SortCriterion::Urgent => {
                tasks.sort_by(|a, b| b.urgent.cmp(&a.urgent));
            }
            SortCriterion::Important => {
                tasks.sort_by(|a, b| b.important.cmp(&a.important));
            }
            SortCriterion::Difficult => {
                tasks.sort_by(|a, b| b.difficult.cmp(&a.difficult));
            }
            SortCriterion::Easy => {
                tasks.sort_by(|a, b| a.difficult.cmp(&b.difficult));
            }
        }
    }
}
