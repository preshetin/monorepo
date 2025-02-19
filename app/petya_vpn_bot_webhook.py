import os
import datetime
import aiohttp
from aiogram import Bot, types
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv("PETYA_VPN_TELEGRAM_BOT_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL_BOT_INCOMNIG_MESSAGES")

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def handle_petya_vpn_webhook(update: dict):
    telegram_update = types.Update(**update)

    # If a message exists then record details and send slack alert
    if telegram_update.message:
        chat_id = telegram_update.message.chat.id
        username = telegram_update.message.from_user.username
        text = telegram_update.message.text
        created_at = datetime.datetime.utcnow().isoformat()

        # Prepare payload for Slack
        slack_payload = {
            "text": f"Chat ID: {chat_id}\nUsername: <https://t.me/{username}|{username}>\nMessage: {text}\nCreated At: {created_at}"
        }

        # Send message data to Slack channel via webhook
        async with aiohttp.ClientSession() as session:
            await session.post(SLACK_WEBHOOK_URL, json=slack_payload)

        # Optionally, send a welcome message back to the user
        await bot.send_message(
            chat_id=chat_id,
            text="Welcome! Core functionality will be soon."
        )
