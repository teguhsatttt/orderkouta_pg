
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
import json
from ..services.pricing_service import clamp_months
from ..services.payment_service import create_order, poll_until_paid
from ..services.membership_service import grant_membership, schedule_expel
from datetime import datetime

def keyboard(m):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("−", callback_data=f"m:{m-1}"),
        InlineKeyboardButton(f"{m} bulan", callback_data="noop"),
        InlineKeyboardButton("+", callback_data=f"m:{m+1}")
    ], [
        InlineKeyboardButton("Bayar", callback_data=f"pay:{m}")
    ]])

async def order_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("ui.json", "r", encoding="utf-8") as f:
        ui = json.load(f)
    await update.effective_chat.send_message(ui["order_prompt"], reply_markup=keyboard(1))

async def order_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data.startswith("m:"):
        m = clamp_months(int(data.split(":")[1]))
        await q.edit_message_reply_markup(reply_markup=keyboard(m))
        return
    if data.startswith("pay:"):
        m = clamp_months(int(data.split(":")[1]))
        with open("config.json","r",encoding="utf-8") as f: cfg = json.load(f)
        order = create_order(cfg, q.from_user.id, m)
        text = f"Nominal unik: {order['amount']}\nKey: {order.get('keyorkut')}"
        if order.get("qrcode"):
            text += f"\nQR: {order['qrcode']}"
        await q.edit_message_text(text)

        jq = context.job_queue
        async def check(ctx):
            ok, st = poll_until_paid(cfg, order)
            if ok:
                rec = await grant_membership(context.application, cfg, q.from_user.id, m)
                when_dt = datetime.fromisoformat(rec["membership_expire"].replace("Z",""))
                await context.bot.send_message(q.message.chat_id, f"Pembayaran berhasil. Invite: {rec['invite_link']}")
                await schedule_expel(jq, cfg, q.from_user.id, when_dt)
            else:
                await context.bot.send_message(q.message.chat_id, "Waktu pembayaran habis atau belum match.")
        jq.run_once(lambda ctx: context.application.create_task(check(ctx)), when=0)

def build_handlers(app):
    app.add_handler(CommandHandler("order", order_cmd))
    app.add_handler(CallbackQueryHandler(order_cb))
