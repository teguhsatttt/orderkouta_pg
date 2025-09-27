
from .rafathar_api import RafatharAPI
from ..repo import orders_pending, payments, audit
from ..services.pricing_service import build_amount, order_ref, clamp_months
from datetime import datetime
import time

def create_order(cfg, user_id: int, months: int):
    months = clamp_months(months)
    amount = build_amount(cfg["pricing"]["price_per_month"], months)
    api = RafatharAPI(cfg["rafathar"]["base_url"], cfg["rafathar"]["apikey"])
    resp = api.create_payment(amount=amount, codeqr="codeqr")

    keyorkut = resp.get("keyorkut") or resp.get("order_id") or resp.get("data", {}).get("keyorkut")
    qrcode = resp.get("qrcode") or resp.get("data", {}).get("qrcode")

    ref = order_ref(user_id, months)
    order = {
        "order_ref": ref, "user_id": user_id, "months": months,
        "amount": amount, "created_at": datetime.utcnow().isoformat()+"Z",
        "keyorkut": keyorkut, "qrcode": qrcode, "provider_resp": resp
    }
    orders_pending.save(ref, order)
    audit.log("order_created", order_ref=ref, user_id=user_id, amount=amount, months=months)
    return order

def poll_until_paid(cfg, order):
    api = RafatharAPI(cfg["rafathar"]["base_url"], cfg["rafathar"]["apikey"])
    merchant = cfg["rafathar"]["merchant"]
    keyorkut = order.get("keyorkut")
    deadline = time.time() + int(cfg["order"]["payment_window_sec"])
    interval = int(cfg["order"]["poll_interval_sec"])

    while time.time() < deadline:
        st = api.cek_status(merchant=merchant, keyorkut=keyorkut) if keyorkut else {}
        status_txt = str(st).lower()
        if "paid" in status_txt or "success" in status_txt or ""status": "success"" in status_txt:
            payments.save(order["order_ref"], {"order": order, "status": st})
            orders_pending.remove(order["order_ref"])
            audit.log("payment_matched", order_ref=order["order_ref"], user_id=order["user_id"], status=st)
            return True, st
        time.sleep(interval)
    audit.log("payment_timeout", order_ref=order["order_ref"])
    return False, None
