from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# 🔍 Получение цены с CoinGecko
def get_price(symbol: str):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[symbol.lower()]["usd"]
    except:
        return "недоступна"

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Цена BTC", callback_data='price bitcoin'),
        InlineKeyboardButton("Цена ETH", callback_data='price ethereum'),
        InlineKeyboardButton("Цена SOL", callback_data='price solana'),
        InlineKeyboardButton("Цена DOGE", callback_data='price dogecoin')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "Привет! Я Коперник Прайм 🤖\n"
        "Доступные команды:\n"
        "/price BTCUSDT — узнать цену\n"
        "/rsi BTCUSDT — RSI (в разработке)\n\n"
        "Выбери монету или используй команду:\n"
        "/price BTCUSDT"
    )

    await update.message.reply_text(message, reply_markup=reply_markup)

# 📩 Команда /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pair = context.args[0].upper()
        if pair == "BTCUSDT":
            symbol = "bitcoin"
        elif pair == "ETHUSDT":
            symbol = "ethereum"
        elif pair == "SOLUSDT":
            symbol = "solana"
        elif pair == "DOGEUSDT":
            symbol = "dogecoin"
        else:
            await update.message.reply_text("⚠️ Неизвестная пара. Попробуй BTCUSDT, ETHUSDT, SOLUSDT, DOGEUSDT.")
            return

        price = get_price(symbol)
        await update.message.reply_text(f"💸 Цена {pair}: ${price}")
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при получении цены.")

# 🔘 Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    symbol_map = {
        "price bitcoin": "bitcoin",
        "price ethereum": "ethereum",
        "price solana": "solana",
        "price dogecoin": "dogecoin"
    }

    if data in symbol_map:
        symbol = symbol_map[data]
        price = get_price(symbol)
        await query.edit_message_text(text=f"💸 Цена {symbol.upper()}/USDT: ${price}")
    else:
        await query.edit_message_text(text="Команда не распознана.")

# 🧠 Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🚀 Коперник Прайм запущен. Жду команды в Telegram...")
    app.run_polling()
