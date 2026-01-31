from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QTextCursor
import sys

class ChatWorker(QThread):
    """Worker thread for LLM operations to prevent UI freezing"""
    response_ready = pyqtSignal(str, bool)
    
    def __init__(self, llm_handler, message):
        super().__init__()
        self.llm_handler = llm_handler
        self.message = message
    
    def run(self):
        response, is_done = self.llm_handler.chat(self.message)
        self.response_ready.emit(response, is_done)


class JournalGeneratorWorker(QThread):
    """Worker thread for generating journal entry"""
    entry_ready = pyqtSignal(str)
    
    def __init__(self, llm_handler):
        super().__init__()
        self.llm_handler = llm_handler
    
    def run(self):
        entry = self.llm_handler.generate_journal_entry()
        self.entry_ready.emit(entry)


class ChatWindow(QMainWindow):
    def __init__(self, llm_handler, journal_writer):
        super().__init__()
        self.llm_handler = llm_handler
        self.journal_writer = journal_writer
        self.conversation_ended = False
        
        self.init_ui()
        self.start_conversation()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Journal Buddy')
        self.setGeometry(100, 100, 600, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('📝 Journal Buddy')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText('Type your message...')
        self.message_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton('Send')
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: #666; font-size: 12px;')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
    
    def start_conversation(self):
        """Start a new conversation"""
        greeting = self.llm_handler.start_conversation()
        self.add_message('Assistant', greeting)
        self.message_input.setFocus()
    
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        if sender == 'Assistant':
            formatted = f'<div style="margin: 10px 0;"><b style="color: #4CAF50;">🤖 Assistant:</b><br/>{message}</div>'
        else:
            formatted = f'<div style="margin: 10px 0;"><b style="color: #2196F3;">👤 You:</b><br/>{message}</div>'
        
        self.chat_display.append(formatted)
        
        # Auto-scroll to bottom
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)
    
    def send_message(self):
        """Send user message and get response"""
        if self.conversation_ended:
            return
        
        message = self.message_input.text().strip()
        if not message:
            return
        
        # Add user message to display
        self.add_message('You', message)
        self.message_input.clear()
        
        # Disable input while processing
        self.message_input.setEnabled(False)
        self.send_button.setEnabled(False)
        self.status_label.setText('Thinking...')
        
        # Process in background thread
        self.worker = ChatWorker(self.llm_handler, message)
        self.worker.response_ready.connect(self.handle_response)
        self.worker.start()
    
    def handle_response(self, response, is_done):
        """Handle the LLM response"""
        self.add_message('Assistant', response)
        
        # Re-enable input
        self.message_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.status_label.setText('')
        self.message_input.setFocus()
        
        if is_done:
            self.conversation_ended = True
            self.generate_journal_entry()
    
    def generate_journal_entry(self):
        """Generate and save the journal entry"""
        self.status_label.setText('Generating journal entry...')
        self.message_input.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # Generate in background thread
        self.generator = JournalGeneratorWorker(self.llm_handler)
        self.generator.entry_ready.connect(self.save_journal_entry)
        self.generator.start()
    
    def save_journal_entry(self, entry):
        """Save the generated journal entry"""
        try:
            filepath = self.journal_writer.create_journal_entry(entry)
            self.status_label.setText(f'✅ Journal saved to: {filepath.name}')
            self.add_message('System', f'<b>Journal entry created successfully!</b><br/>Saved to: {filepath}')
            
            # Add close button
            close_button = QPushButton('Close')
            close_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 10px 20px;
                    font-size: 14px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            close_button.clicked.connect(self.close)
            
            # Add button to layout
            self.centralWidget().layout().addWidget(close_button)
            
        except Exception as e:
            self.status_label.setText(f'❌ Error saving journal: {str(e)}')
            self.message_input.setEnabled(True)
            self.send_button.setEnabled(True)
