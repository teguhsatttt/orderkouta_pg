
from telegram import Update
from telegram.ext import ContextTypes, ChatJoinRequestHandler
from ..repo import members, audit

async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    rec = members.load(req.from_user.id)
    if rec:
        try:
            await req.approve()
            audit.log("join_approved", user_id=req.from_user.id)
        except Exception as e:
            audit.log("join_approve_error", user_id=req.from_user.id, err=str(e))

def build_handlers(app):
    app.add_handler(ChatJoinRequestHandler(on_join_request))
