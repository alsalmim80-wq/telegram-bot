import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

user_chats = {}

def get_chat_session(user_id):
    if user_id not in user_chats:
        model = genai.GenerativeModel(
            "gemini-3.6-flash",
            system_instruction="أنت مساعد متخصص في الرد على الأسئلة والاستفسارات حول المشاريع والأفكار. رد بأسلوب عملي ومباشر باللغة العربية."
        )
        user_chats[user_id] = model.start_chat(history=[])
    return user_chats[user_id]

def get_suggestions_keyboard():
    keyboard = [
        [InlineKeyboardButton("💡 فكرة أخرى", callback_data="idea")],
        [InlineKeyboardButton("🔧 طور الفكرة أكثر", callback_data="develop")],
        [InlineKeyboardButton("🚀 كيف أبدأ؟", callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    chat = get_chat_session(user_id)
    response = chat.send_message(user_message)
    await update.message.reply_t