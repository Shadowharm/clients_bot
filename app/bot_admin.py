from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, filters
import asyncio
import re
from typing import List, Optional

load_dotenv()

class BotAdmin:

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        bot_token: str,
        kw_file: str = "keywords.txt",
        admin_id: Optional[int] = None,
        session_name: str = "bot_admin"
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.KW_FILE = kw_file
        self.ADMIN_ID = admin_id

        self.client = Client(session_name, api_id=self.api_id, api_hash=self.api_hash, bot_token=self.bot_token)
        self._kw_lock = asyncio.Lock()

        @self.client.on_message(filters.private & filters.text)
        async def _admin_commands_handler(client, message):
            if self.ADMIN_ID and message.from_user and message.from_user.id != self.ADMIN_ID:
                return

            text = message.text.strip()
            cmd, *rest = text.split(maxsplit=1)
            arg = rest[0].strip() if rest else ""

            if cmd.lower() == "/help":
                await message.reply(
                    "Команды:\n"
                    "/add <keyword> — добавить ключевое слово/фразу\n"
                    "/remove <keyword> — удалить (точное совпадение, регистронезависимо)\n"
                    "/list — показать все ключевые слова\n"
                    "/clear — удалить все ключевые слова\n"
                    "/help — показать это сообщение"
                )
                return

            if cmd.lower() == "/list":
                kws = await self.load_keywords()
                if not kws:
                    await message.reply("Список ключевых слов пуст.")
                else:
                    await message.reply("Ключевые слова:\n" + "\n".join(f"- {k}" for k in kws))
                return

            if cmd.lower() == "/add":
                if not arg:
                    await message.reply("Укажи ключевое слово после /add")
                    return
                kws = await self.load_keywords()
                if any(k.lower() == arg.lower() for k in kws):
                    await message.reply(f"'{arg}' уже в списке.")
                    return
                kws.append(arg)
                await self.save_keywords(kws)
                await message.reply(f"Добавлено: {arg}")
                return

            if cmd.lower() == "/remove":
                if not arg:
                    await message.reply("Укажи ключевое слово после /remove")
                    return
                kws = await self.load_keywords()
                new = [k for k in kws if k.lower() != arg.lower()]
                if len(new) == len(kws):
                    await message.reply(f"'{arg}' не найдено в списке.")
                    return
                await self.save_keywords(new)
                await message.reply(f"Удалено: {arg}")
                return

            if cmd.lower() == "/clear":
                await self.save_keywords([])
                await message.reply("Список ключевых слов очищен.")
                return

            if text.startswith("/"):
                await message.reply("Неизвестная команда. /help")
                return

    # ----- file helpers -----
    async def load_keywords(self) -> List[str]:
        async with self._kw_lock:
            try:
                with open(self.KW_FILE, "r", encoding="utf-8") as f:
                    lines = [ln.strip() for ln in f if ln.strip()]
            except FileNotFoundError:
                lines = []
            return lines

    async def save_keywords(self, keywords: List[str]) -> None:
        async with self._kw_lock:
            with open(self.KW_FILE, "w", encoding="utf-8") as f:
                for k in keywords:
                    f.write(k.strip() + "\n")

    @staticmethod
    def compile_pattern(keywords: List[str]) -> Optional[re.Pattern]:
        kws = [k.strip() for k in keywords if k and k.strip()]
        if not kws:
            return None
        escaped = [re.escape(k) for k in kws]
        return re.compile(r"\b(?:" + "|".join(escaped) + r")\b", flags=re.IGNORECASE)

    async def start(self) -> None:
        await self.client.start()
        print("BotAdmin started")

    async def stop(self) -> None:
        await self.client.stop()
        print("BotAdmin stopped")
