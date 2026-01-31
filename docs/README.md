# 📝 Journal Buddy

> An AI-powered conversational journaling assistant for Obsidian. Never stare at a blank page again.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red.svg)](https://github.com/sk0dot7/journal-buddy.git)

Journal Buddy transforms journaling from a chore into a natural conversation. Chat with an AI about your day, and it generates beautifully formatted Obsidian journal entries that sound like *you* wrote them.

## ✨ Features

- 🤖 **Conversational AI** - Just chat naturally about your day
- 🎨 **Your Writing Style** - Learns from your existing journals to match your voice
- 📅 **Auto-Formatted** - Generates proper Obsidian markdown (YYYY-MM-DD.md)
- ⏰ **Daily Reminders** - Optional notifications at your chosen time
- 🔒 **100% Private** - Runs locally using Ollama (no cloud, no API costs)
- 💾 **Obsidian Integration** - Saves directly to your vault
- ☁️ **Dropbox Sync** - Works with synced vaults
- 🆓 **Completely Free** - No subscriptions, no API fees

## 🎬 Demo

```
Bot: Hey! How was your day?

You: Had a really awkward moment today 😭

Bot: Oh no! What happened?

You: I ran into my crush at the college gate...
     [conversation continues naturally]

You: That's all for today

Bot: Got it! Generating your journal entry...

✅ Journal saved: 2026-01-30.md
```

The AI then generates an entry in YOUR writing style, complete with your tone, emoji usage, and storytelling flow.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed
- An Obsidian vault

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/journal-buddy.git
cd journal-buddy

# Run setup (installs dependencies & downloads AI model)
chmod +x setup.sh
./setup.sh

# Start the app
python3 main.py
```

**Or for systems without system tray:**
```bash
python3 journal-direct.py
```

### First Run

1. Configure your Obsidian vault path
2. Set your preferred notification time
3. Choose your AI model (default: tinyllama)
4. Click Save

The app will analyze your existing journals to learn your writing style!

## 📖 Usage

### With System Tray (GNOME, KDE, XFCE)

1. App runs in background (📝 tray icon)
2. Get daily notification at set time
3. Or double-click tray icon anytime
4. Chat about your day
5. Say "that's all" when done
6. Journal auto-saves to Obsidian

### Without System Tray (i3, Sway, minimal WMs)

```bash
python3 journal-direct.py
```

Opens chat window directly. See [NO_TRAY.md](NO_TRAY.md) for details.

## 🛠️ Configuration

### Settings

- **Vault Path**: Where to save journal entries
- **Notification Time**: When to remind you daily (HH:MM format)
- **AI Model**: Which Ollama model to use

Access via: System tray → Settings, or File → Settings in direct mode

### AI Models

Recommended models by size:

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| tinyllama | 637 MB | ⚡⚡⚡ | Good | `ollama pull tinyllama` |
| gemma:2b | 1.4 GB | ⚡⚡ | Better | `ollama pull gemma:2b` |
| phi3:mini | 2.3 GB | ⚡⚡ | Excellent | `ollama pull phi3:mini` |
| llama3.1 | 4.7 GB | ⚡ | Best | `ollama pull llama3.1` |

## 🎨 How It Works

1. **Analyzes Your Style** - Reads your existing journals to understand:
   - Your tone (casual, formal, etc.)
   - Emoji usage patterns
   - Formatting preferences (bold, highlights, quotes)
   - Storytelling structure

2. **Natural Conversation** - Chats with you using context-aware follow-ups

3. **Generates Entry** - Transforms the conversation into a journal entry that sounds like you

4. **Auto-Saves** - Creates/updates YYYYMMDD.md in your Obsidian vault

## 📁 File Format

Generated files use your Obsidian template structure:

```
vault/
├── 2026-01-28.md
├── 2026-01-29.md
└── 2026-01-30.md
```

Each entry includes:
- YAML frontmatter (habits, metadata)
- Formatted date headers
- Task queries
- Your journal content under "# Logs"

## 🔧 Troubleshooting

### Common Issues

**"Ollama Not Running"**
```bash
ollama serve
```

**Missing Imports / Crashes**
```bash
python3 test.py  # Run diagnostics
```

**System Tray Not Available**
```bash
python3 journal-direct.py  # Use direct launcher
```

**No Models Found**
```bash
ollama pull tinyllama
```

See [FIXES.md](FIXES.md) for detailed troubleshooting.

## 🏗️ Project Structure

```
journal-buddy/
├── main.py              # Main app (system tray version)
├── journal-direct.py    # Direct launcher (no tray)
├── gui/                 # User interface components
├── core/                # Business logic (LLM, journaling)
├── utils/               # Utilities (config, style analysis)
└── docs/                # Documentation
```

See [STRUCTURE.md](STRUCTURE.md) for details.

## 🤝 Contributing

Contributions are welcome! This project was built to solve a real problem - help make it better.

### Areas for Contribution

- 🎤 Voice input support
- 📱 Mobile companion app
- 🌍 Multi-language support
- 📊 Analytics dashboard
- 🎨 UI/UX improvements
- 🐛 Bug fixes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🗺️ Roadmap

- [ ] Voice journaling
- [ ] Mobile app (React Native)
- [ ] Mood tracking & analytics
- [ ] Multiple journal templates
- [ ] Plugin system
- [ ] Export formats (PDF, email digest)

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.com/) for local AI
- Designed for [Obsidian](https://obsidian.md/) users
- Inspired by the struggle to journal consistently

## 💬 Support

- 🐛 [Report a bug](https://github.com/Skteam07/Journal-Buddy/issues)
- 💡 [Request a feature](https://github.com/Skteam07/Journal-Buddy/issues)
- 💬 [Discussions](https://github.com/Skteam07/Journal-Buddy/discussions)

## ⭐ Star History

If you find this helpful, please consider starring the repo!

---

**Made with ❤️ for consistent journaling**

*No more blank page anxiety. No more missed entries. Just conversations that become beautiful journals.*
