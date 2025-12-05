#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации SESSION_STRING для Pyrogram
"""
import sys
import io
import asyncio
from os import getenv
from dotenv import load_dotenv

# Исправление для Python 3.14+ - создаем event loop перед импортом Pyrogram
if sys.version_info >= (3, 14):
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

from pyrogram import Client

# Настройка кодировки UTF-8 для Windows консоли
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

load_dotenv()

def _get_env_int(name: str):
    v = getenv(name)
    try:
        return int(v) if v is not None else None
    except Exception:
        return None

API_ID = _get_env_int("API_ID")
API_HASH = getenv("API_HASH") or ""

if API_HASH.startswith('"') and API_HASH.endswith('"'):
    API_HASH = API_HASH[1:-1]

if not API_ID or not API_HASH:
    print("❌ Ошибка: не найдены API_ID или API_HASH в файле .env")
    print("\nУбедитесь, что файл .env существует и содержит:")
    print("API_ID=ваш_api_id")
    print("API_HASH=ваш_api_hash")
    sys.exit(1)

print("🔐 Генерация SESSION_STRING...")
print(f"📱 Используется API_ID: {API_ID}")
print("\n⚠️  Внимание: вам нужно будет:")
print("   1. Ввести номер телефона")
print("   2. Ввести код подтверждения из Telegram")
print("   3. Если включена двухфакторная аутентификация - ввести пароль")
print("\n" + "="*50 + "\n")

try:
    with Client("session_generator", API_ID, API_HASH) as app:
        session_string = app.export_session_string()
        print("\n" + "="*50)
        print("✅ SESSION_STRING успешно сгенерирован!")
        print("="*50)
        print("\nДобавьте эту строку в ваш .env файл:")
        print(f"SESSION_STRING={session_string}")
        print("\n" + "="*50)
        
except KeyboardInterrupt:
    print("\n\n❌ Процесс прерван пользователем")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Ошибка при генерации SESSION_STRING: {e}")
    sys.exit(1)

