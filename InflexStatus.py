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

BOT_LIST = [x.strip() for x in os.getenv("BOT_LIST").split(' ')]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
LOG_ID = int(os.getenv("LOG_ID"))
CHECKING_TIME_MIN = int(os.getenv("CHECKING_TIME_MIN", "5"))
CHANNEL_NAME = "Solo Tree"

async def main():
    print("Status Checker Bot Started, Dont Forgot To Visit @InflexSupport.")
    async with app:
        while True:
            TEXT = f"✨ **Welcome To The {CHANNEL_NAME} Bot's Status Channel**\n\n❄ Here Is the List Of The Bot's Which We Own And There Status ( Alive/Dead ), This Message Will Keep Updating On **Every {CHECKING_TIME_MIN} Minutes.**"

            for bots in BOT_LIST:
                Inflex = await app.get_users(f"@{bots}")
                try:
                    await app.send_message(bots, "/Start")
                    await asyncio.sleep(int(CHECKING_TIME_MIN))
                    messages = app.get_chat_history(bots, limit=1)
                    async for x in messages:
                        msg = x.text
                    if msg == "/Start
                        TEXT += f"\n\n**╭⎋ [{Inflex.first_name}](tg://openmessage?user_id={Inflex.id})** \n**╰⊚ 𝖲𝗍𝖺𝗍𝗎𝗌 : 𝖣𝖾𝖺𝖽 💤**"
                        await app.send_message(LOG_ID, f"**[{Inflex.first_name}](tg://openmessage?user_id={Inflex.id}) 𝖮𝖿𝖿 𝖧𝖺𝗂, 𝖠𝖼𝖼𝗁𝖺 𝖧𝗎𝖺 𝖣𝖾𝗄𝗁 𝖫𝗂𝗒𝖺 𝖬𝖺𝗂𝗇𝖾.**")
                        await app.read_chat_history(bots)
                    else:
                        TEXT += f"\n\n**╭⎋ [{Inflex.first_name}](tg://openmessage?user_id={Inflex.id}) : 𝖠𝗅𝗂𝗏𝖾 🫧**\n**╰⊚** {msg}"
                        await app.read_chat_history(bots)
                except FloodWait as e:
                    await asyncio.sleep(e.value)

            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            date = time.strftime("%d %b %Y")
            time = time.strftime("%I:%M %p")
            TEXT += f"\n\n**𝖫𝖺𝗌𝗍 𝖢𝗁𝖾𝖼𝗄𝖾𝖽 𝖮𝗇 :**\n**𝖣𝖺𝗍𝖾 :** {date}\n**𝖳𝗂𝗆𝖾 :** {time}\n\n"

            # Edit the message with the new text and keyboard
            await app.edit_message_text(int(CHANNEL_ID), MESSAGE_ID, TEXT, reply_markup=reply_markup)

            await asyncio.sleep(120)

app.run(main())
