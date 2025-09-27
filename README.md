
# OrderKuota — Telegram Bot + Rafathar Code Payment Gateway (Collaborative Build)

Satu VIP product, durasi 1–12 bulan, QRIS statis + kode unik 3 digit, polling mutasi (Rafathar/Orkut/OKConnect),
setelah match → kirim invite link 5 menit (member_limit=1), set membership expiry, auto-approve join request,
auto-expel saat expiry (ban+unban), logging JSONL & ke admin.

## Struktur
```
orderkouta_pg_collab/
  config.json
  ui.json
  pricing.json
  requirements.txt
  bot.py
  services/
    rafathar_api.py
    pricing_service.py
    payment_service.py
    membership_service.py
    audit_service.py
  handlers/
    start.py
    order_handler.py
    payment_poll.py
    join_request.py
  jobs/
    expiry.py
    sweep_pending.py
  repo/
    filesio.py
    orders_pending.py
    payments.py
    members.py
    users.py
    audit.py
  data/                  # runtime data (json/jsonl)
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Edit `config.json` dan `pricing.json`.

## Jalankan
```bash
python bot.py
```
Bot command:
- `/start` menampilkan info
- `/order` memunculkan UI pilih durasi 1–12 bulan (tombol + / − / bayar)
- Bot mengirim QR + nominal unik, menunggu pembayaran (polling tiap 10 detik, timeout 15 menit)
- Setelah paid: kirim invite link 5 menit (member_limit=1), set masa aktif, catat audit
- Auto-approve join request
- Job expiry meng-expel saat masa aktif habis

> Catatan: perlu izin bot sebagai admin di group/channel VIP agar bisa membuat invite, approve join request, dan kick/unban.
