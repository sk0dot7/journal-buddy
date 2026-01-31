# Project Structure

```
journal-buddy/
│
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── setup.sh                   # Automated setup script
├── README.md                  # Full documentation
├── journal-buddy.service     # Systemd service template
├── .gitignore                # Git ignore rules
│
├── docs/
|   ├──STRUCTURE.md
|   ├──QUICKSTART.md
|   ├──NO_TRAY.md
|   ├──GETTING_STARTED.md
|   ├──FIXES.md
|   └──CONTRIBUTING.md
|
├── gui/                      # GUI components
│   ├── __init__.py
│   ├── chat_window.py       # Main chat interface
│   └── settings.py          # Settings dialog
│
├── core/                     # Core functionality
│   ├── __init__.py
│   ├── llm_handler.py       # Ollama LLM integration
│   ├── journal_writer.py   # Markdown file generation
│   └── scheduler.py         # Notification scheduling
│
└── utils/                    # Utilities
    ├── __init__.py
    ├── config.py            # Configuration management
    └── style_analyzer.py    # Writing style analysis

User Data (created at runtime):
~/.journal-buddy/
└── config.json              # User configuration
```

## Component Details

### Main Application (`main.py`)
- System tray integration
- Application lifecycle management
- Component initialization
- Event handling

### GUI Components (`gui/`)

**chat_window.py**
- Chat interface with message history
- Real-time conversation with LLM
- Journal entry generation UI
- Background threading for non-blocking operations

**settings.py**
- Configuration dialog
- Vault path selection
- Notification time picker
- Model selection

### Core Components (`core/`)

**llm_handler.py**
- Ollama API integration
- Conversation management
- Journal entry generation from chat
- Style-aware content creation

**journal_writer.py**
- Markdown file creation
- Template population
- Date formatting
- File management (append vs. create)

**scheduler.py**
- Daily notification scheduling
- APScheduler integration
- Callback management

### Utilities (`utils/`)

**config.py**
- JSON-based configuration storage
- Settings persistence
- Config file management

**style_analyzer.py**
- Existing journal analysis
- Writing pattern detection
- Style instruction generation
- Emoji and formatting detection

## Data Flow

```
User → System Tray → Chat Window
                ↓
            LLM Handler
                ↓
        Journal Generator
                ↓
        Journal Writer
                ↓
        Obsidian Vault
```

## Configuration

User configuration stored in: `~/.journal-buddy/config.json`

```json
{
  "vault_path": "/home/user/Documents/ObsidianVault",
  "notification_time": "21:00",
  "ollama_model": "llama3.1",
  "first_run": false,
  "writing_style_analyzed": true
}
```

## Dependencies

### Python Packages
- **PyQt6**: GUI framework
- **APScheduler**: Job scheduling
- **plyer**: Cross-platform notifications
- **ollama**: Ollama Python client
- **pystray**: System tray icon
- **Pillow**: Image processing

### External Dependencies
- **Ollama**: Local LLM runtime
- **llama3.1** (or other model): AI model

## File Naming Convention

Generated journal files: `YYYY-MM-DD.md`
- Example: `2026-01-28.md` for January 28, 2026

## Threading Model

- **Main Thread**: GUI and event loop
- **Worker Threads**: 
  - LLM chat operations
  - Journal generation
  - Style analysis

This prevents UI freezing during long operations.

## Error Handling

- Ollama connection errors → User notification
- File system errors → Fallback behavior
- Configuration errors → Settings prompt
- Network errors (Dropbox) → Local save still works
