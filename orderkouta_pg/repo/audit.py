
from .filesio import append_jsonl
from datetime import datetime
AUDIT_PATH = "data/audit.jsonl"
def log(event, **fields):
    rec = {"ts": datetime.utcnow().isoformat()+"Z", "event": event}
    rec.update(fields)
    append_jsonl(AUDIT_PATH, rec)
