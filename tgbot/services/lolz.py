import time
import random
import secrets
import aiohttp
from tgbot.data import config

from tgbot.services.http_client import get_shared_session


class Lolz:
    def __init__(self, access_token: str):
        self.api_url = 'https://api.zelenka.guru/'
        self.session_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        self.timeout = aiohttp.ClientTimeout(total=360)
        self.session_name = f"lolz:{access_token[:12]}"

    def _session(self):
        return get_shared_session(self.session_name, headers=self.session_headers, timeout=self.timeout)

    async def get_user(self):
        response = await self._session().get('https://api.lzt.market/me', timeout=self.timeout)
        if response.status == 200:
            response_json = await response.json()
            if 'user' not in response_json.keys():
                raise ValueError('Invalid Token [Lolzteam Market]')
            return response_json['user']

        error = await response.text()
        error = error.split('<h1>')[1].split('</h1>')[0]
        raise BaseException(error)

    def get_link(self, amount: int, comment: str):
        return f'https://lzt.market/balance/transfer?username={config.lolz_nick}&hold=0&amount={amount}&comment={comment}'

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'

    async def check_payment(self, amount: int, comment: str):
        user_id = config.lolz_id
        response = await self._session().get(f'{self.api_url}market/user/{user_id}/payments', timeout=self.timeout)

        if response.status == 200:
            resp_json = await response.json()
            payments = resp_json['payments']
            for payment in payments.values():
                if 'Перевод денег от' in payment['label']['title'] and int(amount) == payment['incoming_sum'] and comment == payment['data']['comment']:
                    return True
            return False

        resp_text = await response.text()
        error = resp_text.split('<h1>')[1].split('</h1>')[0]
        return f"❗ Попробуйте чуть позже, {error}"
                error = error.split('<h1>')[1].split('</h1>')[0]

                return f"❗ Попробуйте чуть позже, {error}"
