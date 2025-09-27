
from telegram import Update
from telegram.ext import ContextTypes
import json
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("ui.json", "r", encoding="utf-8") as f:
        ui = json.load(f)
    await update.effective_chat.send_message(ui["welcome"])
