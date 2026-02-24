import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# بدون @
SOURCE_CHAT = os.environ.get("SOURCE_CHAT", "solwhaletrending").lstrip("@")

# رقمك من @userinfobot
DEST_CHAT = int(os.environ["DEST_CHAT"])

# فلتر (غيره لاحقاً)
KEYWORD = os.environ.get("KEYWORD", "+75")

async def run_bot_forever():
    while True:
        try:
            client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

            @client.on(events.NewMessage(chats=SOURCE_CHAT))
            async def handler(event):
                text = event.raw_text or ""
                if KEYWORD not in text:
                    return
                await client.send_message(DEST_CHAT, f"🚀 ALERT from @{SOURCE_CHAT}\n\n{text}")
                print("Sent alert to private.")

            await client.start()
            print(f"Bot is running... Watching: {SOURCE_CHAT} | Filter: {KEYWORD}")

            # هذا يخليه يشتغل ولا يقفل
            await client.run_until_disconnected()

        except Exception as e:
            # نطبع سبب التوقف عشان نعرف المشكلة
            print("❌ Bot crashed:", repr(e))
            print("🔁 Restarting in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_bot_forever())
