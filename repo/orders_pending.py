
from .filesio import write_json, read_json
import os

BASE = "data/orders_pending"

def save(order_ref, obj):
    path = os.path.join(BASE, f"{order_ref}.json")
    write_json(path, obj)

def load(order_ref):
    path = os.path.join(BASE, f"{order_ref}.json")
    return read_json(path)

def remove(order_ref):
    path = os.path.join(BASE, f"{order_ref}.json")
    try: os.remove(path)
    except FileNotFoundError: pass
