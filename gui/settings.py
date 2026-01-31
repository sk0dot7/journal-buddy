from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QFileDialog, QTimeEdit, QMessageBox)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont
from pathlib import Path

class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        """Initialize the settings UI"""
        self.setWindowTitle('Settings - Journal Buddy')
        self.setGeometry(200, 200, 500, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel('⚙️ Settings')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Vault path
        vault_label = QLabel('Obsidian Vault Path:')
        vault_label.setStyleSheet('font-weight: bold; font-size: 13px;')
        layout.addWidget(vault_label)
        
        vault_layout = QHBoxLayout()
        self.vault_path_input = QLineEdit()
        self.vault_path_input.setText(self.config.get_vault_path())
        self.vault_path_input.setPlaceholderText('/home/user/Dropbox/ObsidianVault')
        self.vault_path_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        vault_layout.addWidget(self.vault_path_input)
        
        browse_button = QPushButton('Browse')
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        browse_button.clicked.connect(self.browse_vault)
        vault_layout.addWidget(browse_button)
        
        layout.addLayout(vault_layout)
        
        # Notification time
        time_label = QLabel('Daily Notification Time:')
        time_label.setStyleSheet('font-weight: bold; font-size: 13px;')
        layout.addWidget(time_label)
        
        self.time_edit = QTimeEdit()
        current_time = self.config.get_notification_time()
        hour, minute = map(int, current_time.split(':'))
        self.time_edit.setTime(QTime(hour, minute))
        self.time_edit.setDisplayFormat('HH:mm')
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 8px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.time_edit)
        
        # Ollama model
        model_label = QLabel('Ollama Model:')
        model_label.setStyleSheet('font-weight: bold; font-size: 13px;')
        layout.addWidget(model_label)
        
        self.model_input = QLineEdit()
        self.model_input.setText(self.config.get('ollama_model', 'llama3.1'))
        self.model_input.setPlaceholderText('llama3.1, mistral, gemma2, etc.')
        self.model_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.model_input)
        
        # Info text
        info = QLabel('ℹ️ Make sure Ollama is installed and running')
        info.setStyleSheet('color: #666; font-size: 12px; font-style: italic;')
        layout.addWidget(info)
        
        # Spacer
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('Save')
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 24px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def browse_vault(self):
        """Open file dialog to select vault directory"""
        try:
            start_dir = self.vault_path_input.text() or str(Path.home())
            
            directory = QFileDialog.getExistingDirectory(
                self,
                'Select Obsidian Vault Directory',
                start_dir
            )
            
            if directory:
                self.vault_path_input.setText(directory)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Browse error: {str(e)}')
    
    def save_settings(self):
        """Save settings and close dialog"""
        try:
            vault_path = self.vault_path_input.text().strip()
            
            if not vault_path:
                QMessageBox.warning(self, 'Error', 'Please set the Obsidian vault path')
                return
            
            if not Path(vault_path).exists():
                QMessageBox.warning(self, 'Error', 'The vault path does not exist')
                return
            
            # Save configuration
            self.config.set_vault_path(vault_path)
            
            time = self.time_edit.time()
            time_str = f"{time.hour():02d}:{time.minute():02d}"
            self.config.set_notification_time(time_str)
            
            model = self.model_input.text().strip() or 'tinyllama'
            self.config.set('ollama_model', model)
            
            self.config.set('first_run', False)
            
            QMessageBox.information(self, 'Success', 'Settings saved successfully!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save settings: {str(e)}')
