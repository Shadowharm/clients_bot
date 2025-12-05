from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent

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
SESSION_STRING: str = _strip(getenv("SESSION_STRING")) or ""
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
LOG_DIR: Path = BASE_DIR / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"
CHATS_UPDATE_INTERVAL: int = int(_strip(getenv("CHATS_UPDATE_INTERVAL")) or 300)
