import os
import asyncio
import datetime
import pytz
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

load_dotenv()

app = Client(
    name="Inflex",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("STRING_SESSION")
)

BOT_LIST = [x.strip() for x in os.getenv("BOT_LIST").split()]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
LOG_ID = int(os.getenv("LOG_ID"))
CHECKING_TIME_MIN = int(os.getenv("CHECKING_TIME_MIN", "60"))
CHANNEL_NAME = "Solo Tree"

# Optional reply markup with a support button
reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🛠 Support", url="https://t.me/InflexSupport")]]
)

async def main():
    print("Status Checker Bot Started, Don't forget to visit @InflexSupport.")
    async with app:
        while True:
            TEXT = (
                f"✨ **Welcome To The {CHANNEL_NAME} Bot's Status Channel**\n\n"
                f"❄ Here is the list of bots we own and their status (Alive/Dead).\n"
                f"This message updates every **{CHECKING_TIME_MIN} minutes.**"
            )

            for bot_username in BOT_LIST:
                try:
                    bot = await app.get_users(f"@{bot_username}")
                    await app.send_message(bot.id, "/start")
                    await asyncio.sleep(5)

                    messages = app.get_chat_history(bot.id, limit=1)
                    msg_text = ""
                    async for msg in messages:
                        msg_text = msg.text or ""

                    if msg_text.strip() == "/start":
                        TEXT += (
                            f"\n\n**╭⎋ [@{bot_username}](https://t.me/{bot_username})**\n"
                            f"**╰⊚ 𝖲𝗍𝖺𝗍𝗎𝗌 : 𝖣𝖾𝖺𝖽 💤**"
                        )
                        await app.send_message(
                            LOG_ID,
                            f"**[@{bot_username}](https://t.me/{bot_username}) 𝖮𝖿𝖿 𝖧𝖺𝗂, 𝖠𝖼𝖼𝗁𝖺 𝖧𝗎𝖺 𝖣𝖾𝗄𝗁 𝖫𝗂𝗒𝖺 𝖬𝖺𝗂𝗇𝖾.**"
                        )
                        await app.read_chat_history(bot.id)
                    else:
                        TEXT += (
                            f"\n\n**╭⎋ [@{bot_username}](https://t.me/{bot_username}) : 𝖠𝗅𝗂𝗏𝖾 🫧**\n"
                            f"**╰⊚** {msg_text}"
                        )
                        await app.read_chat_history(bot.id)

                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    TEXT += f"\n\n**╭⎋ [@{bot_username}](https://t.me/{bot_username})**\n**╰⊚ Error: {e}**"

            now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
            date = now.strftime("%d %b %Y")
            time = now.strftime("%I:%M %p")
            TEXT += f"\n\n**𝖫𝖺𝗌𝗍 𝖢𝗁𝖾𝖼𝗄𝖾𝖽 𝖮𝗇 :**\n**𝖣𝖺𝗍𝖾 :** {date}\n**𝖳𝗂𝗆𝖾 :** {time}\n"

            await app.edit_message_text(CHANNEL_ID, MESSAGE_ID, TEXT, reply_markup=reply_markup)

            # Sleep for CHECKING_TIME_MIN * 60 seconds
            await asyncio.sleep(CHECKING_TIME_MIN * 60)

app.run(main())
