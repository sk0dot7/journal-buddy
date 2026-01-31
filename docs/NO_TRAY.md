# Running Without System Tray

If your system doesn't have a working system tray (common on i3, Sway, or minimal window managers), use the **direct launcher** instead.

## Quick Start

```bash
python3 journal-direct.py
```

This will:
1. Show settings dialog on first run
2. Open the chat window directly
3. Add a menu bar with Settings and Quit options

## What's Different?

**Regular launcher** (`main.py`):
- Runs in system tray
- Accessible via tray icon
- Stays in background
- Good for: GNOME, KDE, XFCE, Cinnamon

**Direct launcher** (`journal-direct.py`):
- Opens chat window immediately
- No tray icon needed
- Quits when window closes
- Good for: i3, Sway, dwm, or any system without tray

## Usage

### First Run
```bash
python3 journal-direct.py
```
- Configure vault path
- Set notification time (won't work without tray)
- Click Save

### Daily Use
```bash
python3 journal-direct.py
```
- Opens chat window
- Journal with the bot
- Close window when done

### Accessing Settings
While the chat window is open:
- Click **File → Settings** in the menu bar

## Auto-notifications

Daily notifications require a system tray, so they won't work with the direct launcher.

### Alternative: Use cron

Add to your crontab:
```bash
# Open at 9 PM daily
0 21 * * * DISPLAY=:0 /usr/bin/python3 /path/to/journal-buddy/journal-direct.py
```

### Or: Use systemd timer

Create `~/.config/systemd/user/journal-buddy.timer`:
```ini
[Unit]
Description=Daily Journal Reminder

[Timer]
OnCalendar=21:00
Persistent=true

[Install]
WantedBy=timers.target
```

Create `~/.config/systemd/user/journal-buddy.service`:
```ini
[Unit]
Description=Journal Buddy Direct

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/journal-buddy/journal-direct.py
Environment="DISPLAY=:0"
```

Enable:
```bash
systemctl --user enable --now journal-buddy.timer
```

## Comparison

| Feature | main.py (Tray) | journal-direct.py |
|---------|---------------|-------------------|
| System Tray | Required | Not needed |
| Auto-notifications | ✅ Yes | ❌ No |
| Background running | ✅ Yes | ❌ No |
| Direct access | Via tray icon | Immediate |
| Menu bar | No | Yes |
| Setup complexity | Low | Lower |

## Which Should You Use?

**Use `main.py` if:**
- You have GNOME, KDE, XFCE, or similar
- You want background notifications
- You like tray icons

**Use `journal-direct.py` if:**
- You use i3, Sway, dwm, or minimal WM
- System tray doesn't work
- You prefer direct window access
- You'll run it manually when needed

## Troubleshooting

### "System tray is not available"
This is expected - just use `journal-direct.py` instead.

### Window doesn't appear
```bash
# Check if it's running
ps aux | grep journal

# Run with debug
python3 journal-direct.py 2>&1 | tee debug.log
```

### Still crashes
```bash
# Test components first
python3 test.py

# Check Ollama
ollama serve
```
