# Telegram Chat Monitor Bot

## Overview
This is a Telegram bot application that monitors specified chats for keywords and sends notifications when matches are found. The bot runs continuously in the background, watching for messages containing your configured keywords.

**Current Status**: ✅ Bot is running and operational in Replit environment
**Last Updated**: December 5, 2024

## Project Purpose
- Monitor Telegram chats from a specified folder
- Search for keywords in incoming messages
- Send real-time notifications when keywords are detected
- Manage keywords through bot commands

## Architecture

### Components
1. **BotAdmin** (`app/bot_admin.py`) - Admin interface for managing keywords
   - Handles bot commands (/add, /remove, /list, /clear, /help)
   - Manages keyword storage in `keywords.txt`
   - Accessible only to authorized admin user

2. **Watcher** (`app/watcher.py`) - Message monitoring service
   - Monitors all messages in configured chats
   - Matches messages against keyword patterns
   - Sends notifications via Telegram Bot API

3. **ChatsUpdater** (`app/chats_updater.py`) - Chat list manager
   - Fetches chats from specified Telegram folder
   - Updates `chats.txt` with chat IDs on startup

### Technology Stack
- **Language**: Python 3.11
- **Framework**: Pyrogram (Telegram MTProto API)
- **Dependencies**: 
  - pyrogram==2.0.106
  - tgcrypto
  - aiosqlite
  - python-dotenv
  - requests

## Environment Configuration

### Required Secrets (Already Configured)
All credentials are stored in Replit Secrets and automatically loaded:

- `API_ID` - Telegram API ID from https://my.telegram.org
- `API_HASH` - Telegram API Hash from https://my.telegram.org
- `BOT_TOKEN` - Bot token from @BotFather
- `SESSION_STRING` - User account session string
- `ALLOWED_USER_ID` - Admin user's Telegram ID

### Optional Environment Variables
You can add these to Replit Secrets if needed:

- `FOLDER_NAME` - Name of Telegram folder to monitor (default: "test work")
- `NOTIFY_CHAT_ID` - Chat ID for notifications (default: same as ALLOWED_USER_ID)
- `CHATS_FILENAME` - Filename for chat list (default: "chats.txt")
- `PYROGRAM_SESSION_NAME` - Pyrogram session name (default: "my_account")

## How to Use

### Setting Up Your Telegram Folder
1. In Telegram, create a folder (filter) with chats you want to monitor
2. Add chats to this folder
3. Set `FOLDER_NAME` environment variable to match your folder name
4. Restart the bot to reload the chat list

### Bot Commands
Send these commands to your bot via Telegram:

- `/add <keyword>` - Add a keyword to monitor
- `/remove <keyword>` - Remove a keyword
- `/list` - Show all active keywords
- `/clear` - Remove all keywords
- `/help` - Show help message

### Example Workflow
1. Start a chat with your bot using the BOT_TOKEN
2. Send `/add important` to monitor the word "important"
3. Send `/add urgent` to add another keyword
4. Send `/list` to see all keywords
5. When messages containing these keywords appear in monitored chats, you'll receive notifications

## File Structure
```
.
├── app/
│   ├── __init__.py
│   ├── bot_admin.py      # Admin bot commands
│   ├── chats_updater.py  # Chat list management
│   ├── config.py         # Configuration loader
│   └── watcher.py        # Message monitoring
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── chats.txt            # Generated: List of monitored chat IDs
├── keywords.txt         # Generated: List of keywords to watch
├── generate_session.py  # Utility: Generate SESSION_STRING
└── example.env          # Example environment variables
```

## Running the Bot

### In Replit
The bot is configured to run automatically via the "Telegram Bot" workflow. It will:
1. Fetch chats from your specified folder on startup
2. Start both BotAdmin and Watcher clients
3. Wait for events (messages and commands)

To view logs: Check the console output in the Replit interface

To restart: Click "Run" or use the workflow controls

### Monitoring and Logs
- Console logs show when keywords are detected
- Notifications are sent to your configured Telegram chat
- Session files are created (*.session) - these are gitignored

## Troubleshooting

### "No chats in this folder" Warning
**Cause**: The specified folder name doesn't match any folder in your Telegram account, or the folder is empty.

**Solution**: 
1. Check your Telegram folder name matches `FOLDER_NAME` environment variable
2. Ensure the folder contains chats
3. Restart the bot after making changes

### Bot Not Responding to Commands
**Cause**: You're not the authorized admin, or BOT_TOKEN is incorrect.

**Solution**:
1. Verify `ALLOWED_USER_ID` matches your Telegram user ID
2. Verify `BOT_TOKEN` is correct
3. Check bot logs for authentication errors

### No Notifications Received
**Cause**: Keywords don't match, or notification settings are incorrect.

**Solution**:
1. Use `/list` to verify keywords are configured
2. Check `NOTIFY_CHAT_ID` is set correctly
3. Verify monitored chats have messages with matching keywords
4. Review console logs for matching events

## Session String Generation
If you need to generate a new SESSION_STRING:

```bash
python generate_session.py
```

This will authenticate with your Telegram account and output the session string to add to Replit Secrets.

## Security Notes
- All credentials are stored as Replit Secrets (encrypted)
- Session files (*.session) are automatically gitignored
- Only the configured admin can access bot commands
- Keywords and chat lists are stored locally and not committed to git

## User Preferences
- Default folder name: "test work" (customizable)
- Notifications sent with disable_notification flag (silent)
- Case-insensitive keyword matching
- UTF-8 encoding for all text files

## Recent Changes
- **Dec 5, 2024**: Initial Replit setup completed
  - Installed Python 3.11 and dependencies
  - Configured Replit Secrets for all credentials
  - Set up workflow for automatic bot execution
  - Enhanced .gitignore for Python projects
  - Created comprehensive documentation
