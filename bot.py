import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Вставь сюда свой токен
BOT_TOKEN = "7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU"

# Установим базовый логгер
logging.basicConfig(level=logging.INFO)

# Минимальная сумма заказа и стоимость доставки
MIN_ORDER_AMOUNT = 3000
DELIVERY_COST = 500

# Функция обработки ссылок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Здесь будет парсинг цены с Wildberries по ссылке
    price = get_price_from_link(user_text)
    
    if price < MIN_ORDER_AMOUNT:
        await update.message.reply_text(f"Для оформления заказа сумма должна быть не менее {MIN_ORDER_AMOUNT} рублей. Ваш товар стоит {price} рублей. Пожалуйста, добавьте товары до минимальной суммы.")
    else:
        total_price = price + DELIVERY_COST
        await update.message.reply_text(f"Цена товара: {price} рублей\nСтоимость доставки: {DELIVERY_COST} рублей\nИтоговая сумма: {total_price} рублей\n\nДля подтверждения заказа напишите 'Да', чтобы завершить.")

# Пример функции парсинга цены товара
def get_price_from_link(link):
    # Здесь должен быть код для парсинга страницы Wildberries
    # Для примера вернем фиксированную цену
    return 3500  # Это тестовая цена, замените на реальную логику

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправьте ссылку на товар с Wildberries, и я посчитаю итоговую сумму с доставкой!")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
