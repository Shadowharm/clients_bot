# app/chat_updater.py
from pyrogram import Client
from pyrogram.raw import functions
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID") or 0)
API_HASH = getenv("API_HASH") or ""
FOLDER_NAME = getenv("FOLDER_NAME")
SESSION_STRING = getenv("SESSION_STRING")

async def get_chats_in_folder(folder_name: str = FOLDER_NAME):
    async with Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True) as app:
        folders = await app.invoke(functions.messages.GetDialogFilters())
        folder = next((f for f in folders if getattr(f, "title", "") == folder_name), None)
        if not folder or not getattr(folder, "include_peers", []):
            print("⚠️ No chats in this folder")
            return []

        chat_ids = []
        for peer in folder.include_peers:
            try:
                if getattr(peer, "channel_id", None) is not None:
                    chat_id = int("-100" + str(getattr(peer, "channel_id")))
                elif getattr(peer, "user_id", None) is not None:
                    chat_id = int(getattr(peer, "user_id"))
                elif getattr(peer, "chat_id", None) is not None:
                    # For InputPeerChat (legacy group chats), use resolve_peer to convert it
                    # This handles cases where the chat might have been migrated to a supergroup
                    try:
                        resolved_peer = await app.resolve_peer(peer)
                        # Now try to get the chat - resolved_peer might be a different type
                        chat = await app.get_chat(resolved_peer)
                        chat_ids.append(chat.id)
                    except Exception as e2:
                        # If resolve_peer doesn't work, try GetFullChat directly
                        # This will at least verify the chat exists
                        try:
                            await app.invoke(functions.messages.GetFullChat(chat_id=peer.chat_id))
                            # For legacy chats, store the negated chat_id
                            # This is the format used in message.chat.id
                            chat_id = -peer.chat_id
                            chat_ids.append(chat_id)
                        except Exception as e3:
                            print(f"❌ Error fetching InputPeerChat {peer.chat_id}: {e3}")
                    continue
                else:
                    print(f"⚠️ Unknown peer type: {peer}")
                    continue
                chat = await app.get_chat(chat_id)
                chat_ids.append(chat.id)
            except Exception as e:
                print(f"❌ Error fetching chat {peer}: {e}")
        return chat_ids
