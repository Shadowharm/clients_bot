from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parents[1]

def _strip(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s2: str = s.strip()
    if s2.startswith('"') and s2.endswith('"'):
        return s2[1:-1]
    return s2

API_ID: int = int(_strip(getenv("API_ID")) or 0)
API_HASH: str = _strip(getenv("API_HASH")) or ""
BOT_TOKEN: str = _strip(getenv("BOT_TOKEN")) or ""

# Watcher (user account) session. Prefer WATCHER_SESSION_STRING but keep SESSION_STRING for backward compatibility.
WATCHER_SESSION_STRING: str = _strip(getenv("WATCHER_SESSION_STRING")) or _strip(getenv("SESSION_STRING")) or ""
WATCHER_SESSION_NAME: str = _strip(getenv("WATCHER_SESSION_NAME")) or "watcher_user"

# Bot session name (used by BotAdmin)
BOT_SESSION_NAME: str = _strip(getenv("BOT_SESSION_NAME")) or "bot_admin"

FOLDER_NAME: str = _strip(getenv("FOLDER_NAME")) or "test work"

_ALLOWED_USER_ID: Optional[str] = _strip(getenv("ALLOWED_USER_ID"))
ADMIN_ID: Optional[int] = int(_ALLOWED_USER_ID) if _ALLOWED_USER_ID else None

_notify_raw: Optional[str] = _strip(getenv("NOTIFY_CHAT_ID")) or _strip(getenv("ALLOWED_USER_ID")) or _strip(getenv("USER_ID"))
try:
    NOTIFY_CHAT_ID: Optional[int] = int(_notify_raw) if _notify_raw else None
except Exception:
    NOTIFY_CHAT_ID = None

KW_FILE: Path = BASE_DIR / (_strip(getenv("KW_FILE")) or "keywords.txt")
CHATS_FILE: Path = BASE_DIR / (_strip(getenv("CHATS_FILE")) or "chats.txt")

# Keyword matching behavior: "substr" or "word"
KEYWORD_MATCH_MODE: str = (_strip(getenv("KEYWORD_MATCH_MODE")) or "substr").lower()

# Max length for outgoing bot messages (Telegram limit is 4096)
MAX_NOTIFY_LENGTH: int = int(_strip(getenv("MAX_NOTIFY_LENGTH")) or 4000)
LOG_DIR: Path = BASE_DIR / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"
CHATS_UPDATE_INTERVAL: int = int(_strip(getenv("CHATS_UPDATE_INTERVAL")) or 300)
