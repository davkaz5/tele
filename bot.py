import logging
from urllib.parse import unquote
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Вставь свой токен бота
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

logging.basicConfig(level=logging.INFO)

# Функция для умного анализа URL
def smart_analysis(url: str) -> str:
    decoded_url = unquote(url.lower())
    
    # Определение информации о товаре по URL
    title_parts = []
    if "hugo" in decoded_url:
        title_parts.append("Hugo Boss")
    if "ma-vie" in decoded_url:
        title_parts.append("Ma Vie")
    if "parfum" in decoded_url or "парфюм" in decoded_url:
        title_parts.append("парфюм")
    if "75-ml" in decoded_url or "75мл" in decoded_url:
        title_parts.append("75 мл")
    if "tester" in decoded_url:
        title_parts.append("Тестер")

    title = " / ".join(title_parts) if title_parts else "Неопределено"

    # Персонализированные рекомендации
    recommendations = []
    if "tester" in decoded_url:
        recommendations.append("Укажи в заголовке и описании, что это тестер.")
    if "hugo" in decoded_url:
        recommendations.append("Добавь ключевые слова: Hugo, Boss, аромат для женщин/мужчин.")
    if "75" in decoded_url:
        recommendations.append("Укажи объём — 75 мл — в заголовке и характеристиках.")
    if "parfum" in decoded_url or "парфюм" in decoded_url:
        recommendations.append("Уточни тип аромата (парфюмерная вода, туалетная и т.д.)")

    # Рекомендации по отзывам
    recommendations.append("Проверь, чтобы отзывы были актуальными и связаны с качеством товара.")
    recommendations.append("Если есть вопросы, ответь на них в карточке товара.")

    # SEO и описание
    recommendations += [
        "Загрузи 3–5 качественных фото товара (в том числе упаковки).",
        "Добавь описание: аромат, ноты, стойкость, страна производства.",
        "Ответь на популярные вопросы покупателей.",
        "Проверь, чтобы заполнены все характеристики для фильтрации.",
        "Оптимизируй карточку товара с учетом SEO (ключевые слова).",
    ]
    
    # Рекомендации по улучшению карточки товара
    recommendations.append("Не забудь оптимизировать карточку товара с учетом текущих SEO-трендов и требований покупателей.")

    response = f"🔍 *Анализ товара:*\n"
    response += f"📌 *Название:* {title}\n"
    response += f"💬 *Отзывы:* AI-режим — данные не загружаются\n\n"
    response += f"✅ *Рекомендации:*\n" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(recommendations)])

    return response

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "ozon.ru" in user_text:
        reply = smart_analysis(user_text)
    else:
        reply = "Пришли ссылку Арсен на товар Ozon для анализа."

    await update.message.reply_text(reply, parse_mode='Markdown')

# Команда /start
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
