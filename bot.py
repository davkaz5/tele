import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Твой API ключ и Client-Id для Ozon
CLIENT_ID = '2325638'  # Заменить на твой Client-Id
API_KEY = '04c38548-43a4-47d0-8b94-b86c3de7e808'  # Заменить на твой API ключ

# Токен твоего Telegram бота (получить у BotFather)
BOT_TOKEN = '7390788587:AAGk0k_C8O69RQFQ8zIxkqhVPhICXNPsfjU'  # Вставь свой токен сюда

# Функция для получения данных о товарах из Ozon
def get_ozon_products():
    url = 'https://api-seller.ozon.ru/v1/products/info'
    headers = {
        'Client-Id': CLIENT_ID,
        'Api-Key': API_KEY,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Возвращает список товаров
    else:
        return f"Ошибка: {response.status_code}"

# Функция для анализа конкурентов
def analyze_competitors(competitor_price, your_price, competitor_reviews, your_reviews):
    recommendations = []

    # Сравниваем цену
    if competitor_price < your_price:
        recommendations.append("Davoi asa tox gine ichacni :).")

    # Сравниваем отзывы
    if competitor_reviews > your_reviews:
        recommendations.append("Работайте над качеством товара и обслуживанием.")

    return recommendations

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет Arsen! Отправь мне ссылку на товар, и я проанализирую конкурентов!")

# Обработчик анализа товара
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text  # Ссылка на товар
    products = get_ozon_products()  # Получаем все товары

    # Пример анализируемого товара (в реальном коде ты будешь искать конкретный товар по ссылке)
    competitor_price = 500  # Пример цены конкурента
    your_price = 550  # Пример твоей цены
    competitor_reviews = 150  # Пример отзывов конкурента
    your_reviews = 100  # Пример твоих отзывов

    recommendations = analyze_competitors(competitor_price, your_price, competitor_reviews, your_reviews)

    response = "\n".join(recommendations)
    await update.message.reply_text(response)

# Основная функция для запуска бота
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчики команд
app.add_handler(CommandHandler("start", start))

# Обработчик текста (когда пользователь отправляет ссылку на товар)
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), analyze))

# Запуск бота
app.run_polling()
