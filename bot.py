from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = '8466348872:AAG0jMvbPcf7xAFG78ueZa-Je3uxyfOSjQ4'
RESPONSES = {
    "salom": "Va alaykum assalom!",
    "yordam": "Qanday yordam kerak? /help ni bosing.",
    "bot haqida": "Men OpenAI yordamida yaratilgan zamonaviy Telegram botman.",
    "openai": "OpenAI haqida ma'lumot: https://openai.com",
    "rahmat": "Sizga yordam berishdan mamnunman!",
    "qalay": "Yaxshi, rahmat! Sizchi?",
    "xo'sh": "Savolingizni kutaman.",
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.lower()

    for key in RESPONSES:
        if key in text:
            await update.message.reply_text(RESPONSES[key])
            return

    await update.message.reply_text("Kechirasiz, tushunmadim. Iltimos, boshqacha so‘z bilan so‘rayvering.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [KeyboardButton("📋 Yordam"), KeyboardButton("ℹ️ Bot haqida")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Salom, {user.first_name}!\nMen sizga yordam bera oladigan mukammal botman 😊",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Yordam:\n"
        "/start - Botni boshlash\n"
        "/help - Yordam oynasi\n"
        "Yoki menyudan kerakli tugmani tanlang."
    )

async def send_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("OpenAI", url="https://openai.com"),
            InlineKeyboardButton("GitHub", url="https://github.com"),
        ],
        [
            InlineKeyboardButton("🔁 Javob yoz", callback_data="javob")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Quyidagi tugmalardan birini tanlang:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "javob":
        await query.edit_message_text("✅ Siz tugmani bosdingiz!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()

    if "salom" in text:
        await update.message.reply_text("Va alaykum assalom!")
    elif text == "📋 yordam":
        await help_command(update, context)
    elif text == "ℹ️ bot haqida":
        await update.message.reply_text("Men OpenAI Odilbek yaratilgan zamonaviy Telegram botman.")
    elif text == "🔁 javob yoz":
        await update.message.reply_text("Siz tugmani bosdingiz, endi boshqa savol bering!")
    elif "openai" in text:
        await update.message.reply_text("OpenAI haqida ma'lumot: https://openai.com")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buttons", send_inline_buttons))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()
    print("Bot to'xtatildi.")

