import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

logging.basicConfig(level=logging.INFO)

# Простейший фейковый анализ промокодов (имитация)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()
    if "скидка" in message or "промокод" in message:
        await update.message.reply_text("🔎 Поиск скрытых скидок... Найден промокод: `SAVE20` (скидка 20%)", parse_mode='Markdown')
    else:
        await update.message.reply_text("Пришли мне название товара или слово 'промокод'.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ищу промокоды и скрытые скидки. Напиши, что ты ищешь!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
