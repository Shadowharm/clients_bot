# app/get_session.py
import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

API_ID = int(os.getenv("API_ID") or 0)
API_HASH = os.getenv("API_HASH") or ""

if not API_ID or not API_HASH:
    raise SystemExit("Установите API_ID и API_HASH в окружении или .env")

async def main():
    async with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as app:
        print("Скопируйте эту строку и сохраните в .env как SESSION_STRING:")
        print(app.session_string)

if __name__ == "__main__":
    asyncio.run(main())
