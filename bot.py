import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Вставь сюда свой токен бота
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

# Логирование
logging.basicConfig(level=logging.INFO)

# AI-анализ ссылки Ozon (быстрый)
async def analyze_ozon_link(url: str) -> str:
    keywords = []
    if "hugo" in url.lower():
        keywords.append("Hugo Boss")
    if "ma-vie" in url.lower():
        keywords.append("Ma Vie")
    if "парфюм" in url.lower() or "voda" in url.lower():
        keywords.append("парфюмерная вода")

    title = "Товар из Ozon"
    if keywords:
        title = " / ".join(keywords)

    recommendations = (
        f"🔍 *Анализ товара:*\n"
        f"📌 *Название:* {title}\n"
        f"💬 *Отзывы:* Оценки не загружены (бот работает в AI-режиме)\n\n"
        f"✅ *Рекомендации:*\n"
        f"1. Убедись, что заголовок содержит ключевые слова: {'; '.join(keywords) if keywords else 'основные бренды и аромат'}.\n"
        f"2. Добавь описание аромата, стойкости и страны производства.\n"
        f"3. Загрузите 3-5 качественных фото товара.\n"
        f"4. Используй блок “часто задаваемые вопросы”.\n"
        f"5. Проверь, чтобы в карточке были заполнены все характеристики.\n"
    )
    return recommendations

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "ozon.ru" in user_text:
        reply = await analyze_ozon_link(user_text)
    else:
        reply = "Пожалуйста, пришли ссылку на товар с Ozon для анализа."

    await update.message.reply_text(reply, parse_mode='Markdown')

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли ссылку на товар Ozon, и я дам рекомендации по улучшению карточки.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
