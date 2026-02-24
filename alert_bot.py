import os
import asyncio
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]
SOURCE_CHAT = os.environ.get("SOURCE_CHAT", "solwhaletrending").lstrip("@")
DEST_CHAT = int(os.environ["DEST_CHAT"])
KEYWORD = os.environ.get("KEYWORD", "+75")

# Flask keep-alive
app = Flask(__name__)

@app.route("/")
def home():
    return "alive", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

# Telegram bot
async def run_bot():
    while True:
        try:
            client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

            @client.on(events.NewMessage(chats=SOURCE_CHAT))
            async def handler(event):
                text = event.raw_text or ""
                if KEYWORD not in text:
                    return
                await client.send_message(DEST_CHAT, f"🚀 ALERT\n\n{text}")
                print("✅ Alert sent.")

            await client.start()
            print(f"✅ Bot running | Channel: {SOURCE_CHAT} | Filter: {KEYWORD}")
            await client.run_until_disconnected()

        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔁 Reconnecting in 15s...")
            await asyncio.sleep(15)

if __name__ == "__main__":
    t = threading.Thread(target=run_web, daemon=True)
    t.start()
    asyncio.run(run_bot())
```

ثم تأكد أن `requirements.txt` يحتوي:
```
telethon
flask
