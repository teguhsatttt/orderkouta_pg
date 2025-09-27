
from .filesio import write_json, read_json
import os
BASE = "data/members"
def save(user_id, obj):
    path = os.path.join(BASE, f"{user_id}.json")
    write_json(path, obj)
def load(user_id):
    path = os.path.join(BASE, f"{user_id}.json")
    return read_json(path)
