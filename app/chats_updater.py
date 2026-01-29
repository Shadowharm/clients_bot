from pyrogram import Client
from pyrogram.raw import functions

from app import config

async def get_chats_in_folder(folder_name: str = config.FOLDER_NAME):
    if not folder_name:
        print("⚠️ FOLDER_NAME не задан — пропускаю получение чатов")
        return []
    async with Client(
        config.WATCHER_SESSION_NAME,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.WATCHER_SESSION_STRING or None,
        in_memory=True,
    ) as app:
        folders = await app.invoke(functions.messages.GetDialogFilters())
        folder = next((f for f in folders if getattr(f, "title", "") == folder_name), None)
        print(folder)
        if not folder or not getattr(folder, "include_peers", []):
            print("⚠️ No chats in this folder")
            return []

        chat_ids = []
        for peer in folder.include_peers:
            print(f"Fetching chat {peer}")
            try:
                # Prefer resolving peer and mapping to a numeric chat_id without get_chat.
                try:
                    resolved_peer = await app.resolve_peer(peer)
                except Exception:
                    resolved_peer = peer

                channel_id = getattr(resolved_peer, "channel_id", None)
                user_id = getattr(resolved_peer, "user_id", None)
                chat_id = getattr(resolved_peer, "chat_id", None)

                if channel_id is not None:
                    chat_ids.append(int(f"-100{channel_id}"))
                elif user_id is not None:
                    chat_ids.append(int(user_id))
                elif chat_id is not None:
                    # Legacy group chat: negative chat_id
                    chat_ids.append(int(-chat_id))
                else:
                    print(f"⚠️ Unknown peer type: {resolved_peer}")
            except Exception as e:
                print(f"❌ Error fetching chat {peer}: {e}")
        return chat_ids
