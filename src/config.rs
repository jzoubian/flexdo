use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

const DEFAULT_CONFIG_FILE: &str = "flexdo_config.toml";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    #[serde(default = "default_sessions")]
    pub sessions: SessionsConfig,
    
    #[serde(default = "default_sound")]
    pub sound: SoundConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionsConfig {
    #[serde(default = "default_mail_duration")]
    pub mail_duration_minutes: u32,
    
    #[serde(default = "default_focus_duration")]
    pub focus_duration_minutes: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SoundConfig {
    #[serde(default = "default_sound_enabled")]
    pub enabled: bool,
    
    #[serde(default)]
    pub sound_file: Option<String>,
}

fn default_sessions() -> SessionsConfig {
    SessionsConfig {
        mail_duration_minutes: 30,
        focus_duration_minutes: 120,
    }
}

fn default_mail_duration() -> u32 {
    30
}

fn default_focus_duration() -> u32 {
    120
}

fn default_sound() -> SoundConfig {
    SoundConfig {
        enabled: true,
        sound_file: None,
    }
}

fn default_sound_enabled() -> bool {
    true
}

impl Default for Config {
    fn default() -> Self {
        Self {
            sessions: default_sessions(),
            sound: default_sound(),
        }
    }
}

impl Config {
    pub fn load() -> Result<Self> {
        let config_path = Self::get_config_path();
        
        if !config_path.exists() {
            let config = Config::default();
            config.save()?;
            return Ok(config);
        }
        
        let contents = fs::read_to_string(&config_path)
            .context("Failed to read config file")?;
        
        let config: Config = toml::from_str(&contents)
            .context("Failed to parse config file")?;
        
        Ok(config)
    }
    
    pub fn save(&self) -> Result<()> {
        let config_path = Self::get_config_path();
        let toml = toml::to_string_pretty(self)
            .context("Failed to serialize config")?;
        
        fs::write(&config_path, toml)
            .context("Failed to write config file")?;
        
        Ok(())
    }
    
    fn get_config_path() -> PathBuf {
        let mut path = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
        path.push(DEFAULT_CONFIG_FILE);
        path
    }
}
