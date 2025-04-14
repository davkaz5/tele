from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне ссылку на товар с Ozon")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "ozon.ru" in text:
        await update.message.reply_text("Анализирую ссылку... (будет результат)")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))

app.run_polling()
