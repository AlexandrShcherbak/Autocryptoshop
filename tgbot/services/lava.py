import aiohttp
import json, hmac, hashlib, time, random, secrets

from tgbot.services.http_client import get_shared_session


class Lava:
    def __init__(self, shop_id: str, secret_token: str) -> None:
        self.shop_id = shop_id
        self.secret = secret_token
        self.base_url = "https://api.lava.ru/"
        self.timeout = aiohttp.ClientTimeout(total=360)
        self.session_name = f"lava:{self.shop_id}"

    def _session(self):
        return get_shared_session(self.session_name, timeout=self.timeout)

    def _signature_headers(self, data):
        jsonStr = json.dumps(data).encode()
        sign = hmac.new(bytes(self.secret, 'UTF-8'), jsonStr, hashlib.sha256).hexdigest()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Signature': sign
        }
        return headers

    async def create_invoice(self, amount: float, success_url: str, comment: str) -> dict:
        url = f"{self.base_url}/business/invoice/create"
        params = {
            "sum": amount,
            "shopId": self.shop_id,
            "successUrl": success_url,
            "orderId": f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}',
            "comment": comment
        }
        headers = self._signature_headers(params)
        response = await self._session().post(url=url, headers=headers, json=params)
        return await response.json()

    async def status_invoice(self, invoice_id: str) -> bool:
        url = f"{self.base_url}/business/invoice/status"
        params = {
            "shopId": self.shop_id,
            "invoiceId": invoice_id
        }
        headers = self._signature_headers(params)
        response = await self._session().post(url=url, headers=headers, json=params)
        res = await response.json()
        return res['data']['status'] == "success"

    async def get_balance(self):
        params = {'shopId': self.shop_id}
        headers = self._signature_headers(params)
        request = await self._session().post('https://api.lava.ru/business/shop/get-balance', json=params, headers=headers)
        return await request.json()
