# bot.py
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== Налаштування ======
TOKEN = "7640426502:AAHGOWUMRxB79IOuEK7mKeFLC3Mb1DveNi4"          # підстав свій токен
PAYMENT_NUMBER = "https://send.monobank.ua/jar/41gi3pgXqB"  # номер або реквізити для оплати
# ==========================

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Оплатити", callback_data="pay")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # звичайно update.message буде при /start
    if update.message:
        await update.message.reply_text(
            "❤️Натисни кнопку, щоб отримати посилання для оплати:",
            reply_markup=reply_markup
        )
    else:
        # запасний варіант: відправити безпосередньо користувачу
        user_id = update.effective_user.id
        await context.bot.send_message(
            chat_id=user_id,
            text="❤️Натисни кнопку, щоб отримати посилання для оплати:",
            reply_markup=reply_markup
        )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # закриває "loading" у кнопці
    # Надсилаємо текст з номером у той же чат
    await query.message.reply_text(f"{PAYMENT_NUMBER}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click, pattern="^pay$"))
    app.run_polling()

if __name__ == "__main__":
    main()
