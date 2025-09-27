
import httpx
from urllib.parse import urljoin

class RafatharAPI:
    def __init__(self, base_url: str, apikey: str):
        self.base_url = base_url.rstrip('/') + '/'
        self.apikey = apikey

    def _get(self, path: str, params: dict):
        url = urljoin(self.base_url, path.lstrip('/'))
        qp = {"apikey": self.apikey}
        qp.update(params or {})
        with httpx.Client(timeout=30) as client:
            r = client.get(url, params=qp)
            r.raise_for_status()
            return r.json()

    def create_payment(self, amount: int, codeqr: str = "codeqr") -> dict:
        return self._get("/api/orkut/createpayment", {"amount": amount, "codeqr": codeqr})

    def cek_status(self, merchant: str, keyorkut: str) -> dict:
        return self._get("/api/orkut/cekstatus", {"merchant": merchant, "keyorkut": keyorkut})

    def cek_saldo(self, id_: str, pin: str, password: str) -> dict:
        return self._get("/api/orkut/ceksaldo", {"id": id_, "pin": pin, "password": password})
