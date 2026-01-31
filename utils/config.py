import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / '.journal-buddy'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'vault_path': '',
                'notification_time': '21:00',  # 9 PM default
                'ollama_model': 'tinyllama',
                'first_run': True,
                'writing_style_analyzed': False
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.data[key] = value
        self.save_config()
    
    def get_vault_path(self):
        """Get Obsidian vault path"""
        return self.data.get('vault_path', '')
    
    def set_vault_path(self, path):
        """Set Obsidian vault path"""
        self.data['vault_path'] = path
        self.save_config()
    
    def get_notification_time(self):
        """Get notification time (HH:MM format)"""
        return self.data.get('notification_time', '21:00')
    
    def set_notification_time(self, time):
        """Set notification time"""
        self.data['notification_time'] = time
        self.save_config()
