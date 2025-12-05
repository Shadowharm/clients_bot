import re
import requests
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, filters
from datetime import datetime
from typing import List, Optional

load_dotenv()

class Watcher:
    """
    Класс, реализующий наблюдение за списком chat_id из chats.txt и отправку уведомлений через Bot API.
    Логика равна вашему второму файлу.
    """
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: Optional[str] = None,
        bot_token: Optional[str] = None,
        chats_file: str = "chats.txt",
        kw_file: str = "keywords.txt",
        session_name: str = "watcher_user"
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.BOT_TOKEN = bot_token or ""
        self.CHATS_FILE = chats_file
        self.KW_FILE = kw_file

        self.client = Client(session_name, api_id=self.api_id, api_hash=self.api_hash, session_string=self.session_string)

        self.WATCH_CHAT_IDS = self._load_chats()
        print(f"Загружено {len(self.WATCH_CHAT_IDS)} chat_id из {self.CHATS_FILE}")

        @self.client.on_message(filters.all)
        async def _on_new_message(client, message):
            if not self.WATCH_CHAT_IDS:
                return
            chat_id = getattr(message.chat, "id", None)

            if chat_id not in self.WATCH_CHAT_IDS:
                return

            text = self.text_from_message(message)
            if not text:
                return

            keywords = self.load_keywords_from_file(self.KW_FILE)
            if not keywords:
                return

            escaped = [re.escape(k) for k in keywords if k]
            local_pattern = re.compile(r"\b(?:" + "|".join(escaped) + r")\b", flags=re.IGNORECASE)

            if not local_pattern.search(text):
                return
            ts = datetime.fromtimestamp(message.date.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
            chat_title = message.chat.title or getattr(message.chat, "first_name", None) or str(chat_id)
            sender = "system/anonymous"
            if message.from_user:
                sender = (message.from_user.first_name or "")
                if message.from_user.last_name:
                    sender += f" {message.from_user.last_name}"
                if message.from_user.username:
                    sender += f" (@{message.from_user.username})"

            link = await self.build_message_link(message) or "(ссылка недоступна)"
            preview = text.replace("\n", " ").strip()
            if len(preview) > 300:
                preview = preview[:297] + "..."

            # Отладочная информация для диагностики проблем со ссылками
            chat_type = getattr(message.chat, "type", "unknown")
            chat_username = getattr(message.chat, "username", None)
            debug_info = f"chat_type: {chat_type}"
            if chat_username:
                debug_info += f" | username: @{chat_username}"
            
            lines = []
            lines.append("------------------------------------------------------------")
            lines.append(f"[{ts}] Ключевое слово найдено в чате: {chat_title}")
            lines.append(f"Отправитель: {sender}")
            lines.append(f"Ссылка: {link}")
            lines.append(f"Текст: {preview}")
            lines.append(f"message_id: {message.id} | chat_id: {chat_id} | {debug_info}")
            lines.append("------------------------------------------------------------\n")
            message_text = "\n".join(lines)

            print(message_text)
            if not self.BOT_TOKEN:
                print("BOT_TOKEN не задан — пропускаю отправку POST")
                return

            notify_chat_id = getattr(self, "NOTIFY_CHAT_ID", None)
            if notify_chat_id is None:
                print("NOTIFY_CHAT_ID не задан — пропускаю отправку POST")
                return

            url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": notify_chat_id,
                "text": message_text,
                "disable_notification": True,
            }
            try:
                resp = requests.post(url, json=payload, timeout=10)
                if resp.status_code == 200:
                    print(f"Уведомление отправлено в {notify_chat_id} (status 200).")
                else:
                    print(f"Ошибка при отправке уведомления: {resp.status_code} {resp.text}")
            except Exception as e:
                print("Ошибка при отправке POST:", e)

    def _load_chats(self) -> List[int]:
        try:
            with open(self.CHATS_FILE, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
        except FileNotFoundError:
            lines = []

        loaded: List[int] = []
        for ln in lines:
            token = ln.split("|", 1)[0].strip()
            try:
                loaded.append(int(token))
            except ValueError:
                print(f"Не удалось преобразовать в int: '{token}' — пропускаю")
        return loaded

    @staticmethod
    def load_keywords_from_file(path: str = "keywords.txt") -> List[str]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip()]
        except FileNotFoundError:
            open(path, "w", encoding="utf-8").close()
            return []

    async def build_message_link(self, message):
        """
        Строит ссылку на сообщение в Telegram.
        Формирует правильную ссылку для публичных каналов/групп и супергрупп.
        Возвращает ссылку в формате https://t.me/...
        """
        chat = message.chat
        message_id = message.id
        cid = getattr(chat, "id", None)
        
        # Проверяем username в объекте чата
        username = getattr(chat, "username", None)
        
        # Если username нет, пытаемся получить его через get_chat
        if not username:
            try:
                full_chat = await self.client.get_chat(chat.id)
                username = getattr(full_chat, "username", None)
            except Exception:
                pass
        
        # Если есть username - это публичный канал/группа
        # Формат: https://t.me/username/message_id
        if username:
            return f"https://t.me/{username}/{message_id}"
        
        # Для супергрупп без username используем формат c/chat_id/message_id
        # Важно: для супергрупп chat_id имеет формат -100xxxxxxxxxx
        # В ссылке нужно убрать префикс -100 и использовать только числовую часть
        if isinstance(cid, int) and cid < 0:
            cid_str = str(cid)
            if cid_str.startswith("-100"):
                # Супергруппы: убираем префикс -100
                # Важно: raw_id должен быть числом без ведущих нулей
                raw_id = cid_str[4:]
                # Убираем ведущие нули, если они есть
                raw_id = str(int(raw_id)) if raw_id else raw_id
                # Формируем ссылку в формате https://t.me/c/chat_id/message_id
                return f"https://t.me/c/{raw_id}/{message_id}"
            elif cid_str.startswith("-"):
                # Обычные группы (legacy): убираем минус
                raw_id = cid_str[1:]
                raw_id = str(int(raw_id)) if raw_id else raw_id
                return f"https://t.me/c/{raw_id}/{message_id}"
        
        # Для личных чатов (положительный chat_id) ссылку создать нельзя
        # Это ограничение Telegram API
        return None

    @staticmethod
    def text_from_message(message):
        parts = []
        if getattr(message, "text", None):
            parts.append(message.text)
        if getattr(message, "caption", None):
            parts.append(message.caption)
        return "\n".join(parts).strip()

    async def start(self, notify_chat_id: Optional[int] = None) -> None:
        self.NOTIFY_CHAT_ID = notify_chat_id
        await self.client.start()
        print("Watcher started")

    async def stop(self) -> None:
        await self.client.stop()
        print("Watcher stopped")
