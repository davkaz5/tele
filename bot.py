import logging
import asyncio
import telegram
from bs4 import BeautifulSoup
import requests

BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"
CHAT_ID = 6372974933  # Твой chat_id

logging.basicConfig(level=logging.INFO)
bot = telegram.Bot(token=BOT_TOKEN)

# Функция для поиска новостей про Россию
async def fetch_news():
    try:
        url = "https://news.google.com/search?q=россия&hl=ru&gl=RU&ceid=RU%3Aru"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article h3 a")

        news = []
        for a in articles[:5]:
            title = a.text
            link = "https://news.google.com" + a["href"][1:]
            news.append(f"📰 {title}\n🔗 {link}")
        return "\n\n".join(news)

    except Exception as e:
        return f"Ошибка при получении новостей: {e}"

# Фоновая задача: отправка новостей каждые 10 минут
async def send_news_periodically():
    while True:
        logging.info("Получаю новости...")
        news = await fetch_news()
        await bot.send_message(chat_id=CHAT_ID, text=news)
        await asyncio.sleep(600)  # 10 минут

# Основной запуск
async def main():
    await send_news_periodically()

if __name__ == "__main__":
    asyncio.run(main())
