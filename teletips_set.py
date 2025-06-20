from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from plugins.teletips_t import *
from pyrogram.errors import FloodWait, MessageNotModified

bot = Client(
    "Countdown-TeLeTiPs",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

footer_message = os.environ["FOOTER_MESSAGE"]
stoptimer = False

TELETIPS_MAIN_MENU_BUTTONS = [
    [InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")],
    [
        InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
        InlineKeyboardButton('📣 CHANNEL', url='https://t.me/teletipsofficialchannel'),
        InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/teIetips')
    ],
    [InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")]
]


@bot.on_message(filters.command(['start', 'help']) & filters.private)
async def start(client, message):
    await message.reply(
        text=START_TEXT,
        reply_markup=InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS),
        disable_web_page_preview=True
    )


@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    try:
        if query.data == "HELP_CALLBACK":
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]])
            )
        elif query.data == "GROUP_CALLBACK":
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("TeLe TiPs Chat [EN]", url="https://t.me/teletipsofficialontopicchat")],
                    [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
                ])
            )
        elif query.data == "TUTORIAL_CALLBACK":
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎥 Video", url="https://youtu.be/nYSrgdIYdTw")],
                    [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
                ])
            )
        elif query.data == "START_CALLBACK":
            await query.edit_message_text(
                START_TEXT,
                reply_markup=InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
            )
    except MessageNotModified:
        pass


@bot.on_message(filters.command('set'))
async def set_timer(client, message: Message):
    global stoptimer
    try:
        if message.chat.type == "private":
            return await message.reply("⛔️ Команду можно использовать только в группе.")
        
        user_id = message.from_user.id if message.from_user else None
        if user_id is None:
            return await message.reply("❌ Не удалось определить отправителя.")
        
        member = await client.get_chat_member(message.chat.id, user_id)
        if member.status not in ["administrator", "creator"]:
            return await message.reply("👮🏻‍♂️ Только админы могут использовать эту команду.")
        
        if len(message.command) < 3:
            return await message.reply('❌ Неверный формат.\n\n✅ Пример:\n<code>/set 10 "10 секунд"</code>')
        
        user_input_time = int(message.command[1])
        user_input_event = str(message.command[2])
        msg = await bot.send_message(message.chat.id, user_input_time)
        await msg.pin()
        if stoptimer:
            stoptimer = False

        while user_input_time > 0 and not stoptimer:
            d = user_input_time // 86400
            h = (user_input_time % 86400) // 3600
            m = (user_input_time % 3600) // 60
            s = user_input_time % 60
            text = f"{user_input_event}\n\n⏳ {d:02d}d : {h:02d}h : {m:02d}m : {s:02d}s\n\n<i>{footer_message}</i>"
            await msg.edit(text)
            await asyncio.sleep(9)
            user_input_time -= 9

        await msg.edit("🚨 ВРЕМЯ ВЫШЛО!")
        await msg.unpin()
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as ex:
        await message.reply(f"⚠️ Ошибка: {ex}")


@bot.on_message(filters.command('stopc'))
async def stop_timer(client, message: Message):
    global stoptimer
    try:
        user_id = message.from_user.id if message.from_user else None
        if user_id is None:
            return await message.reply("❌ Не удалось определить отправителя.")

        member = await bot.get_chat_member(message.chat.id, user_id)
        if member.status not in ["administrator", "creator"]:
            return await message.reply("👮🏻‍♂️ Только админы могут остановить таймер.")

        stoptimer = True
        await message.reply("🛑 Таймер остановлен.")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as ex:
        await message.reply(f"⚠️ Ошибка: {ex}")


print("✅ Countdown Timer is alive!")
bot.run()
