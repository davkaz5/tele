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
