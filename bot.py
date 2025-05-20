from pyrogram import Client, filters
from pyrogram.types import Message, InlineQuery
from config import API_ID, API_HASH, BOT_TOKEN
from plugins.inline import handle_inline_query
from plugins.search import handle_search, handle_button_click

app = Client("ShobanaSearchBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.text)
async def text_handler(client, message: Message):
    await handle_search(client, message)

@app.on_inline_query()
async def inline_handler(client, inline_query: InlineQuery):
    await handle_inline_query(client, inline_query)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    await handle_button_click(client, callback_query)

app.run()
