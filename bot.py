import logging
import asyncio
import telegram
import feedparser
from datetime import datetime, timedelta

# 🔐 Вставь токен и чат ID
BOT_TOKEN = "СЮДА_ТОКЕН"
CHAT_ID = 6372974933

# RSS-ленты для новостей
FEEDS = [
    "https://lenta.ru/rss/news",
    "https://www.rbc.ru/rss/",
    "https://www.vedomosti.ru/rss/news.xml",
    "https://www.cnews.ru/inc/rss/news.xml",
    "https://www.kommersant.ru/RSS/news.xml",
]

KEYWORDS = ["Россия", "Ozon", "Wildberries", "маркетплейс", "AliExpress", "торговля", "интернет-магазин"]

logging.basicConfig(level=logging.INFO)
bot = telegram.Bot(token=BOT_TOKEN)

# Хранение уже отправленных новостей
sent_links = set()

async def fetch_and_send_news():
    while True:
        logging.info("🔍 Проверка новостей...")
        for url in FEEDS:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if entry.link in sent_links:
                    continue

                if any(keyword.lower() in entry.title.lower() for keyword in KEYWORDS):
                    message = f"📰 *{entry.title}*\n{entry.link}"
                    try:
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN)
                        sent_links.add(entry.link)
                        await asyncio.sleep(2)
                    except Exception as e:
                        logging.error(f"Ошибка при отправке: {e}")

        await asyncio.sleep(600)  # 10 минут

async def main():
    await fetch_and_send_news()

if __name__ == "__main__":
    asyncio.run(main())
