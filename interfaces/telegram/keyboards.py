from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def delegation_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Claude", callback_data='claude')],
        [InlineKeyboardButton("💻 DeepSeek", callback_data='deepseek')]
    ])
