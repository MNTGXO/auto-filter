from pyrogram.types import InlineQueryResultDocument
from config import CHANNELS

def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

async def handle_inline_query(client, inline_query):
    query = inline_query.query.strip()
    if not query:
        await inline_query.answer([], cache_time=1)
        return

    results = []
    seen_ids = set()

    for channel in CHANNELS:
        async for msg in client.search_messages(channel, query, filter="document"):
            if not msg.document or msg.message_id in seen_ids:
                continue
            seen_ids.add(msg.message_id)

            results.append(
                InlineQueryResultDocument(
                    title=msg.document.file_name,
                    description=f"Size: {human_size(msg.document.file_size)}",
                    document_url=f"https://t.me/c/{str(channel)[4:]}/{msg.message_id}",
                    mime_type=msg.document.mime_type or "application/octet-stream",
                    caption=msg.document.file_name,
                    thumb_url="https://telegra.ph/file/8f65c3bfcfb0a74d6824b.jpg",  # Optional
                )
            )
            if len(results) >= 50:
                break

    await inline_query.answer(results, cache_time=3)
