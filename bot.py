import os
from telebot import TeleBot, types

# Рекомендуется хранить токен в переменной окружения TELEGRAM_BOT_TOKEN
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

bot = TeleBot(TOKEN, parse_mode="HTML")

# URL мини-приложения (ваш GitHub Pages). Пример: https://<username>.github.io/mini-app/
WEBAPP_URL = "https://<username>.github.io/mini-app/"

@bot.message_handler(commands=["start"])
def handle_start(message):
    # Клавиатура с кнопкой Web App
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_info = types.WebAppInfo(url=WEBAPP_URL)
    btn = types.KeyboardButton(text="Открыть мини-приложение", web_app=webapp_info)
    kb.add(btn)

    # Альтернативно можно отправить инлайн-кнопку:
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(text="Открыть мини-приложение", web_app=webapp_info))

    bot.send_message(
        message.chat.id,
        "Нажмите кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=kb
    )
    bot.send_message(
        message.chat.id,
        "Либо используйте инлайн-кнопку:",
        reply_markup=ikb
    )

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)
