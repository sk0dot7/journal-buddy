#!/usr/bin/env python3
import sys
import signal
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import Config
from utils.style_analyzer import StyleAnalyzer
from core.llm_handler import LLMHandler
from core.journal_writer import JournalWriter
from core.scheduler import NotificationScheduler
from gui.chat_window import ChatWindow
from gui.settings import SettingsDialog


class JournalBuddyApp:
    def __init__(self):
        try:
            self.app = QApplication(sys.argv)
            self.app.setApplicationName('Journal Buddy')
            
            # Initialize components
            self.config = Config()
            self.llm_handler = None
            self.journal_writer = None
            self.scheduler = None
            self.chat_window = None
            self.tray_icon = None
            
            # Check if system tray is available
            self.has_tray = QSystemTrayIcon.isSystemTrayAvailable()
            
            if self.has_tray:
                # Create system tray icon if available
                self.app.setQuitOnLastWindowClosed(False)  # Keep running in tray
                self.create_tray_icon()
            else:
                # No tray - app quits when windows close
                print("Note: Running without system tray")
                self.app.setQuitOnLastWindowClosed(True)
            
            # Check if first run
            if self.config.get('first_run', True):
                self.show_settings()
            else:
                self.initialize_components()
                # If no tray, open chat window directly
                if not self.has_tray:
                    print("Opening chat window (no system tray available)")
                    self.open_chat_window()
                    
        except Exception as e:
            print(f"Initialization error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def create_tray_icon(self):
        """Create system tray icon"""
        try:
            # Check if system tray is available
            if not QSystemTrayIcon.isSystemTrayAvailable():
                print("Warning: System tray is not available on this system")
                print("The app will run but without a tray icon")
                # Still create a minimal tray icon for menu access
            
            # Create a simple icon (green circle with pen)
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw green circle
            painter.setBrush(QColor('#4CAF50'))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(4, 4, 56, 56)
            
            # Draw white pen/pencil symbol
            painter.setPen(QColor('white'))
            painter.setFont(painter.font())
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, '📝')
            
            painter.end()
            
            icon = QIcon(pixmap)
            
            # Create tray icon
            self.tray_icon = QSystemTrayIcon(icon, self.app)
            
            # Create menu
            menu = QMenu()
            
            journal_action = menu.addAction('✍️ Open Journal')
            journal_action.triggered.connect(self.open_chat_window)
            
            settings_action = menu.addAction('⚙️ Settings')
            settings_action.triggered.connect(self.show_settings)
            
            menu.addSeparator()
            
            quit_action = menu.addAction('❌ Quit')
            quit_action.triggered.connect(self.quit_app)
            
            self.tray_icon.setContextMenu(menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
            
            # Show welcome message
            if QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon.showMessage(
                    'Journal Buddy',
                    'Journal Buddy is running in the background',
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"Tray icon error (non-fatal): {e}")
            # App can still run without tray icon
    
    def tray_icon_activated(self, reason):
        """Handle tray icon click"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_chat_window()
    
    def initialize_components(self):
        """Initialize LLM, journal writer, and scheduler"""
        vault_path = self.config.get_vault_path()
        
        if not vault_path or not Path(vault_path).exists():
            QMessageBox.warning(
                None,
                'Configuration Required',
                'Please configure your Obsidian vault path in settings'
            )
            self.show_settings()
            return
        
        # Initialize LLM handler
        model = self.config.get('ollama_model', 'llama3.1')
        self.llm_handler = LLMHandler(model=model)
        
        # Analyze writing style if not done yet
        if not self.config.get('writing_style_analyzed', False):
            try:
                analyzer = StyleAnalyzer(vault_path)
                style_profile = analyzer.analyze_existing_journals()
                style_instructions = analyzer.get_style_instructions()
                self.llm_handler.set_style_instructions(style_instructions)
                self.config.set('writing_style_analyzed', True)
            except Exception as e:
                print(f"Style analysis error: {e}")
        
        # Initialize journal writer
        self.journal_writer = JournalWriter(vault_path)
        
        # Initialize scheduler
        self.scheduler = NotificationScheduler(callback=self.open_chat_window)
        notification_time = self.config.get_notification_time()
        self.scheduler.start(notification_time)
    
    def open_chat_window(self):
        """Open the chat window for journaling"""
        if not self.llm_handler or not self.journal_writer:
            self.initialize_components()
            if not self.llm_handler:  # Still not initialized
                return
        
        # Check if Ollama is running
        try:
            import ollama
            ollama.list()  # Test connection
        except Exception as e:
            QMessageBox.critical(
                None,
                'Ollama Not Running',
                f'Please start Ollama first:\n\nRun: ollama serve\n\nError: {str(e)}'
            )
            return
        
        # Create and show chat window
        self.chat_window = ChatWindow(self.llm_handler, self.journal_writer)
        
        # Add menu bar for systems without tray
        if not self.has_tray:
            from PyQt6.QtWidgets import QMenuBar
            menubar = self.chat_window.menuBar()
            
            # File menu
            file_menu = menubar.addMenu('&File')
            
            settings_action = file_menu.addAction('⚙️ Settings')
            settings_action.triggered.connect(self.show_settings)
            
            file_menu.addSeparator()
            
            quit_action = file_menu.addAction('❌ Quit')
            quit_action.triggered.connect(self.quit_app)
        
        self.chat_window.show()
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.config)
        if dialog.exec():
            # Reinitialize components with new settings
            if self.scheduler:
                self.scheduler.stop()
            self.initialize_components()
    
    def quit_app(self):
        """Quit the application"""
        if self.scheduler:
            self.scheduler.stop()
        if self.tray_icon:
            self.tray_icon.hide()
        self.app.quit()
    
    def run(self):
        """Run the application"""
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = JournalBuddyApp()
    app.run()
