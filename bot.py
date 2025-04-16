import logging
import asyncio
import telegram
import feedparser
import re

BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"
CHAT_ID = 6372974933  # Убедись, что это числовой ID

FEEDS = [
    "https://lenta.ru/rss/news",
    "https://www.kommersant.ru/RSS/news.xml",
]

KEYWORDS = ["Россия", "Ozon", "Wildberries", "маркетплейс", "AliExpress", "торговля", "интернет-магазин"]

logging.basicConfig(level=logging.INFO)
bot = telegram.Bot(token=BOT_TOKEN)

sent_links = set()

# Экранируем все спецсимволы для Markdown V2
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

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
                    link = escape_markdown(entry.link)
                    message = f"📰 *{title}*\n{link}"
                    try:
                        # Проверяем, может ли бот отправить сообщение
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
                        sent_links.add(entry.link)
                        await asyncio.sleep(2)
                    except telegram.error.Unauthorized:
                        logging.error("Ошибка авторизации: Проверь токен или доступ к боту.")
                    except Exception as e:
                        logging.error(f"Ошибка при отправке: {e}")

        await asyncio.sleep(1200)  # Каждые 10 минут

async def main():
    await fetch_and_send_news()

if __name__ == "__main__":
    asyncio.run(main())
