import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# 🔐 Вставь свой токен бота
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

logging.basicConfig(level=logging.INFO)

# Глобальная переменная для хранения приложения Telegram
app = None

# Функция парсинга новостей
async def fetch_and_send_news():
    try:
        url = "https://news.google.com/rss/search?q=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&hl=ru&gl=RU&ceid=RU:ru"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll("item")[:5]  # Берем топ-5 новостей

        message = "📰 *Свежие новости про Россию:*\n"
        for item in items:
            title = item.title.text
            link = item.link.text
            message += f"\n- [{title}]({link})"

        # Отправляем сообщение всем пользователям, которые запустили бота
        for chat_id in subscribers:
            await app.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        logging.error(f"Ошибка при получении новостей: {e}")

# Список подписчиков
subscribers = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await update.message.reply_text("Привет! Я буду присылать свежие новости про Россию каждые 10 минут.")

# Главная функция запуска
def main():
    global app
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(fetch_and_send_news()), 'interval', minutes=10)
    scheduler.start()

    app.run_polling()

if __name__ == "__main__":
    main()
