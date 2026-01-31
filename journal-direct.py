#!/usr/bin/env python3
"""
Direct launcher for Journal Buddy - opens chat window immediately
Use this if your system doesn't have a working system tray
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMessageBox
from utils.config import Config
from core.llm_handler import LLMHandler
from core.journal_writer import JournalWriter
from gui.chat_window import ChatWindow
from gui.settings import SettingsDialog
from utils.style_analyzer import StyleAnalyzer

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Journal Buddy')
    
    # Load config
    config = Config()
    
    # Check if first run
    if config.get('first_run', True):
        print("First run - showing settings...")
        dialog = SettingsDialog(config)
        if not dialog.exec():
            print("Settings cancelled, exiting")
            return
    
    # Check vault path
    vault_path = config.get_vault_path()
    if not vault_path or not Path(vault_path).exists():
        QMessageBox.critical(None, 'Error', 'Please configure vault path in settings')
        return
    
    # Initialize components
    print("Initializing components...")
    model = config.get('ollama_model', 'tinyllama')
    llm_handler = LLMHandler(model=model)
    
    # Analyze writing style if needed
    if not config.get('writing_style_analyzed', False):
        print("Analyzing your writing style...")
        try:
            analyzer = StyleAnalyzer(vault_path)
            style_profile = analyzer.analyze_existing_journals()
            style_instructions = analyzer.get_style_instructions()
            llm_handler.set_style_instructions(style_instructions)
            config.set('writing_style_analyzed', True)
            print("Writing style analyzed!")
        except Exception as e:
            print(f"Style analysis error (non-fatal): {e}")
    
    # Initialize journal writer
    journal_writer = JournalWriter(vault_path)
    
    # Check if Ollama is running
    try:
        import ollama
        ollama.list()
    except Exception as e:
        QMessageBox.critical(
            None,
            'Ollama Not Running',
            f'Please start Ollama first:\n\nRun: ollama serve\n\nError: {str(e)}'
        )
        return
    
    # Create and show chat window
    print("Opening chat window...")
    chat_window = ChatWindow(llm_handler, journal_writer)
    
    # Add menu bar
    from PyQt6.QtWidgets import QMenuBar
    menubar = chat_window.menuBar()
    
    file_menu = menubar.addMenu('&File')
    
    settings_action = file_menu.addAction('⚙️ Settings')
    settings_action.triggered.connect(lambda: SettingsDialog(config).exec())
    
    file_menu.addSeparator()
    
    quit_action = file_menu.addAction('❌ Quit')
    quit_action.triggered.connect(app.quit)
    
    chat_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
