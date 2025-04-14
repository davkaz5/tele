import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

logging.basicConfig(level=logging.INFO)

async def analyze_ozon_link(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Название не найдено"

        reviews_block = soup.find("span", string=lambda text: text and "отзыва" in text)
        reviews = reviews_block.get_text(strip=True) if reviews_block else "Отзывы не найдены"

        recommendations = (
            f"🔍 *Анализ товара:*\n"
            f"📌 *Название:* {title}\n"
            f"💬 *Отзывы:* {reviews}\n\n"
            f"✅ *Рекомендации:*\n"
            f"1. Убедись, что добавлены ключевые слова в описание.\n"
            f"2. Загрузите качественные фотографии с разных ракурсов.\n"
            f"3. Ответьте на вопросы покупателей.\n"
            f"4. Уточните данные об аромате, составе и стойкости.\n"
            f"5. Регулярно обновляйте описание для улучшения SEO."
        )
        return recommendations
    except Exception as e:
        return f"Ошибка анализа: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне ссылку на товар с Ozon, и я выдам рекомендации.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "ozon.ru" in text:
        result = await analyze_ozon_link(text)
        await update.message.reply_text(result, parse_mode="Markdown")
    else:
        await update.message.reply_text("Пожалуйста, отправь ссылку на товар с Ozon.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
