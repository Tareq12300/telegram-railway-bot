import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

TARGET_CHAT = os.environ["TARGET_CHAT"]
SEND_TO = os.environ["SEND_TO"]

VOLUME_LIMIT = int(os.environ.get("VOLUME_LIMIT", "130000"))

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def parse_money(x):
    x = x.replace(",", "").replace("$", "").strip().upper()

    mult = 1

    if x.endswith("K"):
        mult = 1000
        x = x[:-1]

    elif x.endswith("M"):
        mult = 1000000
        x = x[:-1]

    try:
        return float(x) * mult
    except:
        return None


def parse_volume(text):

    m = re.search(r"Vol:\s*\$?([0-9\.,]+[KMB]?)", text)

    if not m:
        return None

    return parse_money(m.group(1))


def get_symbol(text):

    m = re.search(r"\$([A-Z0-9]{2,15})", text)

    if m:
        return m.group(1)

    return "UNKNOWN"


@client.on(events.NewMessage(chats=TARGET_CHAT))
async def handler(event):

    text = event.raw_text

    volume = parse_volume(text)

    if not volume or volume < VOLUME_LIMIT:
        return

    symbol = get_symbol(text)

    msg = f"""
🚨 Whale Alert

Token: {symbol}
Volume 1h: ${volume:,.0f}

{text}
"""

    try:
        entity = await client.get_entity(int(SEND_TO))
        await client.send_message(entity, msg)
        print("ALERT:", symbol, volume)

    except Exception as e:
        print("SEND ERROR:", e)


async def main():

    me = await client.get_me()

    print("Logged in as:", me.first_name)
    print("Listening to:", TARGET_CHAT)
    print("Volume filter:", VOLUME_LIMIT)


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
