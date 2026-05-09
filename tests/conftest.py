import pytest
import time
import sys
from pathlib import Path
import threading

# 保证项目根目录在 sys.path 中
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.request import Request
from utils.config_loader import config
from utils.file_loader import load_yaml
from models.api_models import YamlTestCase
from app import app as flask_app

@pytest.fixture(scope="session")
def test_server():
    """在测试会话期间启动 Flask 测试服务器"""
    # 用独立线程启动 Flask
    thread = threading.Thread(target=flask_app.run, kwargs={
        'host': '127.0.0.1',
        'port': 5000,
        'debug': True,
        'use_reloader': False
    })
    thread.daemon = True
    thread.start()
    time.sleep(0.5)
    yield "http://127.0.0.1:5000"

@pytest.fixture(scope="function")
def client(test_server):
    return Request(base_url=config['base_url'])


@pytest.fixture(scope="function")
def auth_token(client):
    """
    独立的登录 fixture：
    1. 使用 LoginAPI 对象执行登录
    2. 返回 token 字符串
    3. scope=session 保证只登录一次
    """
    from core.api.login_api import LoginAPI, LoginRequest

    login_api = LoginAPI(client)
    req = LoginRequest(username="arena", password="1sf8d6")
    resp = login_api.call(req)

    assert resp.token is not None, "登录失败，无法获取 auth_token"
    return resp.token


@pytest.fixture
def auth_client(test_server, auth_token):
    """
    为需要登录态的测试用例准备的客户端：
    - 在原始 client 的基础上，每次请求自动带上 Authorization 头
    - 这样用例里直接用 auth_client 发送请求，不用手动管 token
    """
    client = Request(base_url=config['base_url'])
    client.session.headers.update({
        "Authorization": f"Bearer {auth_token}"
    })
    return client
