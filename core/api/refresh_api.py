from dataclasses import dataclass
from typing import Optional

@dataclass
class RefreshRequest:
    pass

@dataclass
class RefreshResponse:
    status_code: int
    msg: Optional[str] = None
    token: Optional[str] = None

class RefreshAPI:
    def __init__(self, client):
        self.client = client
        self.url = '/refresh'

    def call(self) -> RefreshResponse:
        resp = self.client.send('POST', self.url)
        data = resp.json()
        return RefreshResponse(
            status_code=resp.status_code,
            msg=data.get('msg'),
            token=data.get('token')
        )