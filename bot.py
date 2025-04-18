import logging
import asyncio
from telethon import TelegramClient, events
from telegram import Bot

# Твой бот Telegram
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"
CHAT_ID = 6372974933

# Для Telethon API (можно сгенерировать на https://my.telegram.org)
API_ID = 12345678
API_HASH = 'your_api_hash'

# Список Telegram-каналов
SOURCE_CHANNELS = [
    'memes',
    'video_memes_ru',
    'shit_video',
    'rusmemesdaily',
    'orunet'
]

bot = Bot(token=BOT_TOKEN)
client = TelegramClient('session', API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    if event.video:
        try:
            file = await event.download_media()
            caption = event.text or "🎬 Смешное видео"
            await bot.send_video(chat_id=CHAT_ID, video=open(file, 'rb'), caption=caption)
            logging.info("📤 Отправлено новое видео")
        except Exception as e:
            logging.error(f"❌ Ошибка при отправке: {e}")

async def main():
    await client.start()
    logging.info("🤖 Бот запущен и слушает каналы")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
