from dataclasses import dataclass
from typing import Optional
from utils.config_loader import config

@dataclass
class LoginRequest:
    username: str
    password: str

@dataclass
class LoginResponse:
    status_code: int
    msg: Optional[str] = None
    token: Optional[str] = None

class LoginAPI:
    def __init__(self, client):
        self.client = client
        self.url = '/login'

    def call(self, request: LoginRequest) -> LoginResponse:
        response = self.client.send(
            method='POST',
            url=self.url,
            json={'username': request.username, 'password': request.password}
        )
        data = response.json()
        return LoginResponse(
            status_code=response.status_code,
            msg=data.get('msg'),
            token=data.get('token')
        )