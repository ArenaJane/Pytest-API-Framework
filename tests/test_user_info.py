import sys
import allure
import pytest
from pathlib import Path
from core.api.user_info_api import UserInfoAPI

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_user_info_with_token(auth_client):   # 注意这里用的是 auth_client，自带 token
    with allure.step("获取用户信息"):
        api = UserInfoAPI(auth_client)
        resp = api.call()
    assert resp.status_code == 200
    assert resp.username == "arena"
    assert resp.role == "tester"

def test_user_info_without_token(client):
    with allure.step("无 token 获取用户信息"):
        api = UserInfoAPI(client)
        resp = api.call()
    assert resp.status_code == 401
    assert resp.msg == "missing token"

def test_user_info_expired(auth_token, client):
    with allure.step("token 过期"):
        import time
        time.sleep(4)  # 等 token 过期
        client.session.headers.update({"Authorization": f"Bearer {auth_token}"})
        api = UserInfoAPI(client)
        resp = api.call()
    assert resp.status_code == 401
    assert resp.msg == "token expired"