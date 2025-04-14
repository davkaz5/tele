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
import requests

def get_ozon_products():
    url = 'https://api-seller.ozon.ru/v1/products/info'
    headers = {
        'Client-Id': '2325638',  # 
        'Api-Key': '04c38548-43a4-47d0-8b94-b86c3de7e808',  # Заменить на твой API ключ
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Возвращает список товаров
    else:
        return f"Ошибка: {response.status_code}"

def analyze_competitors(competitor_price, your_price, competitor_reviews, your_reviews):
    recommendations = []

    # Сравниваем цену
    if competitor_price < your_price:
        recommendations.append("Снизьте цену для привлечения покупателей.")

    # Сравниваем отзывы
    if competitor_reviews > your_reviews:
        recommendations.append("Работайте над качеством товара и обслуживанием.")

    return recommendations
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text  # Ссылка на товар
    products = get_ozon_products()  # Получаем все товары

    # Пример анализируемого товара (в реальном коде ты будешь искать конкретный товар)
    competitor_price = 500  # Пример цены конкурента
    your_price = 550  # Пример твоей цены
    competitor_reviews = 150  # Пример отзывов конкурента
    your_reviews = 100  # Пример твоих отзывов

    recommendations = analyze_competitors(competitor_price, your_price, competitor_reviews, your_reviews)

    response = "\n".join(recommendations)
    await update.message.reply_text(response)
from telegram.ext import CommandHandler

async def start_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте ссылку на товар, чтобы я мог начать анализ.")

start_handler = CommandHandler('start_analysis', start_analysis)
app.add_handler(start_handler)
