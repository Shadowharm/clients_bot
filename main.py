# main.py
# pip install pyrogram tgcrypto python-dotenv requests
import asyncio
import sys
import io
from os import getenv
from dotenv import load_dotenv

# Настройка кодировки UTF-8 и отключение буферизации для Windows консоли
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Исправление для Python 3.14+ - создаем event loop перед импортом Pyrogram
if sys.version_info >= (3, 14):
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

from pyrogram import idle

load_dotenv()

from app.bot_admin import BotAdmin
from app.watcher import Watcher
from app.chats_updater import get_chats_in_folder

def _get_env_int(name: str):
    v = getenv(name)
    try:
        return int(v) if v is not None else None
    except Exception:
        return None

API_ID = _get_env_int("API_ID") or 0
API_HASH = getenv("API_HASH") or ""
if API_HASH.startswith('"') and API_HASH.endswith('"'):
    API_HASH = API_HASH[1:-1]

BOT_TOKEN = getenv("BOT_TOKEN") or ""
SESSION_STRING = getenv("SESSION_STRING")
ALLOWED_USER_ID = _get_env_int("ALLOWED_USER_ID")
NOTIFY_CHAT_ID = _get_env_int("NOTIFY_CHAT_ID") or ALLOWED_USER_ID or _get_env_int("USER_ID")

CHATS_FILENAME = getenv("CHATS_FILENAME") or "chats.txt"

async def main():

    try:
        print("🔄 Получение списка чатов ...")
        chat_ids = await get_chats_in_folder()
        with open(CHATS_FILENAME, "w", encoding="utf-8") as f:
            for cid in chat_ids:
                f.write(f"{cid}\n")
        print(f"✅ Записано {len(chat_ids)} чатов в {CHATS_FILENAME}")
    except Exception as e:
        print(f"❌ Ошибка при получении чатов: {e}")

    # создаём экземпляры
    bot_admin = BotAdmin(api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, admin_id=ALLOWED_USER_ID)
    watcher = Watcher(api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, bot_token=BOT_TOKEN)

    # старт обоих клиентов
    await bot_admin.start()
    await watcher.start(notify_chat_id=NOTIFY_CHAT_ID)

    print("Все клиенты запущены. Ожидание событий... (Ctrl+C для остановки)")

    try:
        await idle()  # pyrogram.idle() — ждёт сигналов остановки
    finally:
        await watcher.stop()
        await bot_admin.stop()

if __name__ == "__main__":
    asyncio.run(main())
