import logging
import asyncio
import telegram
import feedparser
import re
from datetime import datetime, timedelta

# 🔐 Токен и ID чата
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"
CHAT_ID = 6372974933

# RSS-ленты
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

sent_links = set()

# Экранирование Markdown-символов
def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+=|{}.!-])', r'\\\1', text)

async def fetch_and_send_news():
    while True:
        logging.info("🔍 Проверка новостей...")
        for url in FEEDS:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if entry.link in sent_links:
                    continue

                if any(keyword.lower() in entry.title.lower() for keyword in KEYWORDS):
                    title = escape_markdown(entry.title)
                    message = f"📰 *{title}*\n{entry.link}"
                    try:
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
                        sent_links.add(entry.link)
                        await asyncio.sleep(2)
                    except Exception as e:
                        logging.error(f"Ошибка при отправке: {e}")

        await asyncio.sleep(600)  # каждые 10 минут

async def main():
    await fetch_and_send_news()

if __name__ == "__main__":
    asyncio.run(main())
