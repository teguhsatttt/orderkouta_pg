
from .filesio import write_json
import os
BASE = "data/payments"
def save(order_ref, obj):
    path = os.path.join(BASE, f"{order_ref}.json")
    write_json(path, obj)
