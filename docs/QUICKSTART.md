# Quick Start Guide

## Installation (5 minutes)

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```

### 2. Install Journal Buddy
```bash
cd journal-buddy
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Check Python version
- Install Ollama if needed
- Download the AI model
- Install Python dependencies

## First Run

```bash
python3 main.py
```

You'll see a Settings dialog. Configure:

1. **Vault Path**: Browse to your Obsidian vault
   - Example: `/home/yourname/Dropbox/ObsidianVault`

2. **Notification Time**: Set your preferred time
   - Example: 21:00 (9 PM)

3. **Model**: Keep default (llama3.1)

Click **Save**.

## Using Journal Buddy

### The app is now running in your system tray! 

Look for the 📝 icon in your system tray.

### Start Journaling:

**Method 1**: Wait for daily notification
- At your set time, click the notification

**Method 2**: Open anytime
- Double-click the 📝 tray icon
- Or right-click → "Open Journal"

### Chat Flow:

1. **Bot greets you**: "Hey! How was your day?"

2. **You respond**: Tell your story naturally
   - "Today I met my crush at the college gate..."
   - "It was super awkward, my face turned red..."
   - "I couldn't even speak properly 😭"

3. **Bot asks follow-ups**: 
   - "What made you feel that way?"
   - "What happened next?"

4. **You continue**: Share more details

5. **When done**: Say "that's all" or "done"

6. **Bot generates**: Creates your journal entry

7. **Auto-saves**: To `YYYY-MM-DD.md` in your vault

## Example Conversation

```
Bot: Hey! How was your day?

You: Had a really awkward moment today 😭

Bot: Oh no! What happened?

You: I ran into my crush at the college gate. We ended up 
     in the same auto. I was sitting right in front of her 
     and my face turned completely red.

Bot: That sounds intense! How did you handle it?

You: Not well lol. My hands were shaking, I couldn't even 
     drink water properly without spilling it. And she paid 
     my auto fare because I didn't have change 😭

Bot: Did you get to talk to her at all?

You: Just briefly. I paid her back later via UPI and sent 
     a quick thank you message. She replied with "It's ok ☺️"

You: That's all for today

Bot: Got it! Let me write up your journal entry now.
```

The bot will then generate an entry that sounds like YOU wrote it!

## Tips

✅ **DO**: 
- Talk naturally, like to a friend
- Include specific details and emotions
- Use emojis if you normally do
- Share honest feelings

❌ **DON'T**: 
- Try to make it "proper" or formal
- Skip emotions
- Rush through - take your time
- Worry about grammar

## Troubleshooting

### Ollama not running?
```bash
ollama serve
```

### Can't see tray icon?
- Check if your desktop environment supports system tray
- Try: `python3 main.py` and look for the window

### Wrong vault path?
- Right-click tray icon → Settings
- Update the path

## Daily Workflow

1. 🔔 Get notification at 9 PM (or your time)
2. 💬 Chat for 5-10 minutes about your day
3. ✅ Journal auto-saves to Obsidian
4. ☁️ Dropbox syncs to all devices
5. 🎉 Consistent journaling without effort!

## Next Steps

- Customize notification time
- Try different conversation styles
- Check out advanced features in README.md

Happy journaling! 📝✨
