# 🎉 Journal Buddy - Complete Installation Guide

## What You're Getting

A complete AI-powered journaling app that:
- ✅ Runs on Linux
- ✅ Uses FREE local AI (Ollama)
- ✅ Learns YOUR writing style
- ✅ Sends daily reminders
- ✅ Saves to Obsidian vault (Dropbox synced)
- ✅ Generates YYYY-MM-DD.md formatted files
- ✅ Works in system tray (always available)

## Installation Steps

### Step 1: Extract the Project

```bash
# Extract to your preferred location
cd ~/
unzip journal-buddy.zip
cd journal-buddy
```

### Step 2: Run the Setup Script

```bash
# This installs everything automatically
chmod +x setup.sh
./setup.sh
```

The script will:
1. Check your Python version (needs 3.10+)
2. Install Ollama if not present
3. Download the llama3.1 AI model (~4GB)
4. Install Python dependencies
5. Make scripts executable

⏱️ **Time**: 10-15 minutes (depending on internet speed for model download)

### Step 3: Start the App

```bash
python3 main.py
```

### Step 4: Configure Settings

On first run, you'll see a Settings dialog:

1. **Obsidian Vault Path**
   - Click "Browse"
   - Navigate to your Dropbox Obsidian vault
   - Example: `/home/yourname/Dropbox/ObsidianVault/`

2. **Notification Time**
   - Set your preferred daily journal time
   - Example: `21:00` for 9 PM

3. **Ollama Model**
   - Keep default: `llama3.1`
   - (You can change this later if needed)

4. Click **Save**

🎉 **You're done!** The app is now running in your system tray.

## How to Use

### Finding the App

Look for the 📝 icon in your system tray (top-right or bottom-right of screen).

### Starting a Journal Session

**Option 1: Scheduled Time**
- Wait for the notification at your set time
- Click the notification
- Chat window opens

**Option 2: Anytime**
- Double-click the 📝 tray icon
- OR right-click → "Open Journal"
- Chat window opens

### The Conversation Flow

1. **Bot greets you**:
   ```
   "Hey! How was your day?"
   ```

2. **You respond naturally**:
   ```
   "Today was crazy! I ran into my crush at college..."
   ```

3. **Bot asks follow-ups**:
   ```
   "Oh really? What happened?"
   ```

4. **You continue sharing**:
   - Tell the story in your own words
   - Include details, emotions, thoughts
   - Use emojis if you want
   - Be yourself!

5. **When finished**:
   ```
   "That's all for today"
   ```

6. **Bot generates your journal**:
   - Creates entry in YOUR writing style
   - Saves as `YYYY-MM-DD.md`
   - Syncs via Dropbox

### Example Session

```
Bot: Hey! What's been going on today?

You: Had the most awkward encounter ever 😭

Bot: What happened?

You: I was leaving hostel and ran into my crush at the 
     college gate. We ended up in the same auto rickshaw!

Bot: That sounds intense! How did it go?

You: Terribly lol. I was sitting right across from her, 
     my face turned bright red, hands shaking. I couldn't 
     even drink water without spilling it 😭

Bot: Did you get to talk to her at all?

You: Barely. She even paid my auto fare because I didn't 
     have cash. I was so embarrassed I paid her back via 
     UPI later with a quick thank you message.

You: That's all

Bot: Got it! Let me write up your journal entry now.

[Generates and saves journal in your style]
```

## After First Run

### The app analyzed your existing journals!

It learned:
- Your tone (casual, formal, etc.)
- Your emoji usage
- Your formatting preferences
- Your storytelling style

Now it will generate entries that sound like YOU wrote them.

## Daily Workflow

1. 🔔 **9 PM** - Get notification
2. 💬 **5 mins** - Chat about your day
3. 📝 **Auto** - Journal entry created
4. ☁️ **Auto** - Syncs via Dropbox
5. ✅ **Done** - Consistent journaling!

## Troubleshooting

### "Ollama Not Running" Error

```bash
# In a new terminal
ollama serve
```

Keep this running, or set up auto-start (see below).

### Can't See System Tray Icon

Some Linux desktop environments hide tray icons by default.

**GNOME**: Install TopIconPlus extension
```bash
sudo apt install gnome-shell-extension-topicons-plus
```

**KDE/XFCE**: Should work by default

### Journal Not Saving

1. Check Settings → Vault Path is correct
2. Verify folder exists and is writable
3. Check Dropbox is syncing

### Poor AI Responses

Try a different model:
```bash
# Download better model
ollama pull llama3.1:70b  # Larger, better quality

# Update in Settings → Ollama Model
```

## Auto-Start on Boot (Optional)

### Method 1: Systemd (Recommended)

```bash
# 1. Edit the service file
nano journal-buddy.service

# 2. Update the path (line 7):
#    Change: /path/to/journal-buddy/main.py
#    To: /home/YOURNAME/journal-buddy/main.py

# 3. Copy to systemd
mkdir -p ~/.config/systemd/user/
cp journal-buddy.service ~/.config/systemd/user/

# 4. Enable and start
systemctl --user enable journal-buddy.service
systemctl --user start journal-buddy.service

# 5. Check status
systemctl --user status journal-buddy.service
```

### Method 2: Startup Applications

1. Open "Startup Applications" in your system settings
2. Click "Add"
3. Name: `Journal Buddy`
4. Command: `/usr/bin/python3 /home/YOURNAME/journal-buddy/main.py`
5. Save

## Advanced Tips

### Change Notification Time

Right-click tray icon → Settings → Notification Time

### Re-analyze Writing Style

```bash
# Edit config
nano ~/.journal-buddy/config.json

# Change this line:
"writing_style_analyzed": false

# Save and restart app
```

### Try Different AI Models

```bash
# See available models
ollama list

# Download new model
ollama pull mistral

# Update in Settings
```

### Multiple Journals Per Day

The app automatically appends to the same day's file with timestamps.

## Privacy & Security

- ✅ 100% local AI (Ollama)
- ✅ No cloud API calls
- ✅ No data leaves your computer
- ✅ No tracking or analytics
- ✅ Open source code

## Getting Help

1. Check `QUICKSTART.md` for quick answers
2. Read `README.md` for detailed docs
3. Review `STRUCTURE.md` for technical details

## What's Next?

- Customize your notification time
- Experiment with different conversation styles
- Check your Obsidian vault - journals are already there!
- Set up auto-start for effortless journaling

---

## Summary

You now have a complete AI journaling assistant that:
- Chats with you daily like a friend
- Generates journal entries in YOUR voice
- Auto-saves to Obsidian in YYYY-MM-DD.md format
- Syncs via Dropbox
- Runs completely FREE and LOCAL

**Happy journaling!** 📝✨

No more blank page anxiety. No more missed journal entries.
Just natural conversations that become beautiful journal entries.
