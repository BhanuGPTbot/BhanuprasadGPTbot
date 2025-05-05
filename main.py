
from flask import Flask, request
import openai
import telegram
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
bot = telegram.Bot(token=TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            reply = response["choices"][0]["message"]["content"]
            bot.send_message(chat_id=chat_id, text=reply)
    return "ok"
