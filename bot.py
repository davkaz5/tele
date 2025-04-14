import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Вставь сюда свои ключи
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

# Функция для общения с ChatGPT
async def chatgpt_reply(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Или gpt-4 если доступен
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка: {e}"

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await chatgpt_reply(user_text)
    await update.message.reply_text(reply)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Задай мне любой вопрос!")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
