from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import CHANNELS

RESULTS_PER_PAGE = 10
search_cache = {}  # {user_id: [messages]}
page_tracker = {}  # {user_id: current_page}


def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


async def handle_search(client: Client, message: Message):
    query = message.text.strip()
    if not query:
        await message.reply("❗ Please provide a search query.")
        return

    user_id = message.from_user.id
    matched_msgs = []

    for channel in CHANNELS:
        async for msg in client.search_messages(channel, query, filter="document"):
            if msg.document:
                matched_msgs.append(msg)
            if len(matched_msgs) >= 100:
                break

    if not matched_msgs:
        await message.reply("❌ No files found.")
        return

    search_cache[user_id] = matched_msgs
    page_tracker[user_id] = 1
    await send_page(client, message, user_id, 1)


async def send_page(client: Client, message_or_cb, user_id: int, page: int):
    msgs = search_cache.get(user_id, [])
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    page_msgs = msgs[start:end]

    if not page_msgs:
        await message_or_cb.reply("⚠ No results on this page.")
        return

    text_lines = []
    for msg in page_msgs:
        name = msg.document.file_name
        size = human_size(msg.document.file_size)
        link = f"https://t.me/c/{str(msg.chat.id)[4:]}/{msg.message_id}"
        text_lines.append(f"[{size}] [{name}]({link})")

    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"page_{page - 1}"))
    if end < len(msgs):
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"page_{page + 1}"))

    reply_markup = InlineKeyboardMarkup([buttons]) if buttons else None
    text = f"**Search Results – Page {page}**\n\n" + "\n".join(text_lines)

    if isinstance(message_or_cb, Message):
        await message_or_cb.reply(text, disable_web_page_preview=True, reply_markup=reply_markup)
    else:
        await message_or_cb.edit_message_text(text, disable_web_page_preview=True, reply_markup=reply_markup)
    page_tracker[user_id] = page


async def handle_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await send_page(client, callback_query, user_id, page)
        await callback_query.answer()
