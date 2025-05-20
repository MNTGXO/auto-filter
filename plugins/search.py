from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS

SEARCH_LIMIT = 30

async def handle_search(client, message):
    query = message.text
    results = []

    for channel in CHANNELS:
        async for msg in client.search_messages(channel, query, filter="document"):
            if msg.document:
                results.append(msg)
                if len(results) >= SEARCH_LIMIT:
                    break

    if not results:
        await message.reply("❌ No files found.")
        return

    buttons = [
        [InlineKeyboardButton(f"{msg.document.file_name}", callback_data=f"get_{msg.chat.id}_{msg.message_id}")]
        for msg in results
    ]

    await message.reply("🔍 Select a file to download:", reply_markup=InlineKeyboardMarkup(buttons))


async def handle_button_click(client, callback_query):
    data = callback_query.data
    if not data.startswith("get_"):
        return

    _, chat_id, msg_id = data.split("_")
    chat_id = int(chat_id)
    msg_id = int(msg_id)

    try:
        file_msg = await client.get_messages(chat_id, int(msg_id))
        await file_msg.copy(callback_query.message.chat.id)
        await callback_query.answer()
    except Exception:
        await callback_query.answer("⚠️ Failed to retrieve file.", show_alert=True)
