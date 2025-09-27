
import json, asyncio
from telegram.ext import Application, CommandHandler
from handlers.start import start
from handlers.order_handler import build_handlers as order_handlers
from handlers.join_request import build_handlers as join_handlers

def load_cfg():
    with open("config.json","r",encoding="utf-8") as f: return json.load(f)

async def main():
    cfg = load_cfg()
    app = Application.builder().token(cfg["telegram"]["bot_token"]).build()

    app.add_handler(CommandHandler("start", start))
    order_handlers(app)
    join_handlers(app)

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=["message","callback_query","chat_join_request"])
    print("Bot payment started.")
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
