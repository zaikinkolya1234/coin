import json
import os
import threading

from flask import Flask, request, jsonify
import telebot

TOKEN = "8432849665:AAEsa0PTkBzpYZae0y6fsxiq38bRtpLFGvo"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
TOKENS_FILE = "tokens.json"
TOKENS_LOCK = threading.Lock()


def load_tokens():
    if os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_tokens(data):
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


TOKENS = load_tokens()


def get_user_tokens(user_id: int) -> int:
    uid = str(user_id)
    with TOKENS_LOCK:
        tokens = TOKENS.get(uid)
        if tokens is None:
            tokens = 10000
            TOKENS[uid] = tokens
            save_tokens(TOKENS)
        return tokens


def set_user_tokens(user_id: int, tokens: int) -> None:
    uid = str(user_id)
    with TOKENS_LOCK:
        TOKENS[uid] = tokens
        save_tokens(TOKENS)


@app.get("/tokens/<int:user_id>")
def get_tokens(user_id: int):
    tokens = get_user_tokens(user_id)
    return jsonify({"tokens": tokens})


@app.post("/tokens/<int:user_id>")
def set_tokens(user_id: int):
    payload = request.get_json(silent=True) or {}
    tokens = payload.get("tokens")
    if not isinstance(tokens, int):
        return jsonify({"error": "Invalid tokens"}), 400
    set_user_tokens(user_id, tokens)
    return jsonify({"status": "ok"})


@bot.message_handler(commands=["start"])
def start(message):
    tokens = get_user_tokens(message.from_user.id)
    bot.reply_to(message, f"Ваш баланс: {tokens} токенов")


def run_bot():
    bot.polling(none_stop=True)


if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

