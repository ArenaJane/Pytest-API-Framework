import allure
import pytest
import os
import shutil

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent  # __file__ 是 conftest.py，parent.parent 回到 APILoginProject
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.user import User
from utils.request import  Request
from utils.config_loader import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DATA = os.path.join(BASE_DIR, 'data', 'user.yaml')
TEMP_DATA = os.path.join(BASE_DIR, 'data', 'temp.yaml')

@pytest.fixture
def temp_data_file():
    shutil.copyfile(ORIGINAL_DATA, TEMP_DATA)
    yield TEMP_DATA
    if os.path.exists(TEMP_DATA):
        os.remove(TEMP_DATA)

@pytest.fixture
def user_factory(temp_data_file):
    def create_user(username, password):
        return User(username, password, data_file=temp_data_file)
    return create_user

@pytest.fixture(scope='session')
def client():
    with allure.step("初始化客户端并登录"):
        client = Request(base_url=config['base_url'])
        res = client.send("POST", "/login", json={
            "username": "arena",
            "password": "1sf8d6"
        })
        token = res.json()["token"]

        client.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    return client