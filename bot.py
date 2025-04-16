import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Вставьте сюда свой токен бота и API ключ TgStat
BOT_TOKEN = '7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU'
TGSTAT_API_KEY = 'ce099f638fefb344c9389e9becda5f72'

# Каналы для мониторинга
channels = [
    '@ecomnews',
    '@marketplaces_ru',
    '@ozonnews',
    '@wildberriesnews',
    '@aliexpressnews'
]

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция для получения новостей из TGStat
async def fetch_news():
    news_data = []
    for channel in channels:
        url = f'https://api.tgstat.ru/v1/channels/{channel}/posts?token={TGSTAT_API_KEY}&limit=5'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])
            for post in posts:
                news_data.append({
                    'channel': channel,
                    'title': post.get('title'),
                    'link': post.get('url')
                })
    return news_data

# Функция для отправки новостей в Telegram
async def send_news_to_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_data = await fetch_news()
    for news in news_data:
        message = f"📰 *Новости из канала {news['channel']}*\n\n"
        message += f"🔗 [Ссылка на новость]({news['link']})\n"
        await update.message.reply_text(message, parse_mode='Markdown')

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я собираю новости из Telegram-каналов о маркетплейсах и электронной коммерции.")

# Функция для получения новостей и отправки их пользователю
async def fetch_news_and_send():
    chat_id = '6372974933'  # Используйте ваш chat_id
    news_data = await fetch_news()
    for news in news_data:
        message = f"📰 *Новости из канала {news['channel']}*\n\n"
        message += f"🔗 [Ссылка на новость]({news['link']})\n"
        # Отправка новости в Telegram
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Запуск бота с асинхронным циклом
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Планировщик для запуска бота каждые 10 минут
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_news_and_send, 'interval', minutes=10)
    scheduler.start()

    # Запуск бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
