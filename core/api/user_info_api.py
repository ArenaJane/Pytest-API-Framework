from dataclasses import dataclass
from typing import Optional

@dataclass
class UserInfoRequest:
    pass

@dataclass
class UserInfoResponse:
    status_code: int
    msg: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None

class UserInfoAPI:
    def __init__(self, client):
        self.client = client
        self.url = "/user/info"

    def call(self) -> UserInfoResponse:
        resp = self.client.send('GET', self.url)
        data = resp.json()
        return UserInfoResponse(
            status_code=resp.status_code,
            msg=data.get('msg'),
            username=data.get('username'),
            role=data.get('role')
        )