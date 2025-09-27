
from datetime import datetime, timedelta
from telegram import ChatInviteLink
from ..repo import members, audit

def calc_expiry(months: int):
    return datetime.utcnow() + timedelta(days=30*months)

async def grant_membership(app, cfg, user_id: int, months: int):
    vip_chat_id = cfg["telegram"]["vip_chat_id"]
    expire_ts = calc_expiry(months)

    expire_date = datetime.utcnow() + timedelta(minutes=5)
    link: ChatInviteLink = await app.bot.create_chat_invite_link(
        chat_id=vip_chat_id, expire_date=expire_date, member_limit=1
    )

    rec = {
        "user_id": user_id,
        "vip_chat_id": vip_chat_id,
        "invite_link": link.invite_link,
        "invite_expire": expire_date.isoformat()+"Z",
        "membership_expire": expire_ts.isoformat()+"Z",
        "months": months
    }
    members.save(user_id, rec)
    audit.log("membership_granted", user_id=user_id, invite=link.invite_link, expires_at=rec["membership_expire"])
    return rec

async def schedule_expel(job_queue, cfg, user_id: int, when_dt):
    chat_id = cfg["telegram"]["vip_chat_id"]
    async def expel(ctx):
        try:
            await ctx.bot.ban_chat_member(chat_id, user_id)
            await ctx.bot.unban_chat_member(chat_id, user_id)
        except Exception:
            pass
    job_queue.run_once(lambda ctx: app.create_task(expel(ctx)), when=when_dt)
