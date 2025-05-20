import os

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNELS = list(map(int, os.environ.get("CHANNELS", "-1001234567890").split()))

REDIRECT_CHANNEL = -100xxxxxxxxxx
REDIRECT_INVITE = "https://t.me/+XXXXXX"  # Your public/private invite link
