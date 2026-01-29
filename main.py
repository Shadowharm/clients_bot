# main.py
# pip install pyrogram tgcrypto python-dotenv requests
import asyncio
import sys
import io

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

from app import config
from app.bot_admin import BotAdmin
from app.watcher import Watcher
from app.chats_updater import get_chats_in_folder

async def main():
    if not config.API_ID or not config.API_HASH:
        raise SystemExit("❌ API_ID или API_HASH не заданы в .env")
    if not config.BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN не задан в .env")
    if config.NOTIFY_CHAT_ID is None:
        print("⚠️ NOTIFY_CHAT_ID не задан — бот не сможет отправлять уведомления")

    try:
        print("🔄 Получение списка чатов ...")
        chat_ids = await get_chats_in_folder()
        print(chat_ids)
        with open(config.CHATS_FILE, "w", encoding="utf-8") as f:
            for cid in chat_ids:
                f.write(f"{cid}\n")
        print(f"✅ Записано {len(chat_ids)} чатов в {config.CHATS_FILE}")
    except Exception as e:
        print(f"❌ Ошибка при получении чатов: {e}")

    # создаём экземпляры
    bot_admin = BotAdmin(api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, admin_id=config.ADMIN_ID)
    watcher = Watcher(api_id=config.API_ID, api_hash=config.API_HASH)

    # старт обоих клиентов
    await bot_admin.start()
    await watcher.start(notify_chat_id=config.NOTIFY_CHAT_ID)

    print("Все клиенты запущены. Ожидание событий... (Ctrl+C для остановки)")

    try:
        await idle()  # pyrogram.idle() — ждёт сигналов остановки
    finally:
        await watcher.stop()
        await bot_admin.stop()

if __name__ == "__main__":
    asyncio.run(main())
