import allure
import time
import pytest
from core.api.refresh_api import RefreshAPI, RefreshResponse

class TestRefresh:
    @allure.title("刷新 token - 正常场景")
    def test_refresh_success(self, auth_client):
        """使用有效 token 刷新，应该返回新 token"""
        api = RefreshAPI(auth_client)
        resp = api.call()

        with allure.step("校验刷新成功"):
            assert resp.status_code == 200
            assert resp.msg is None          # 成功时 app.py 没有设置 msg
            assert resp.token is not None
            # 可选：校验新 token 格式
            assert "new" in resp.token

    @allure.title("刷新 token - 缺少 token")
    def test_refresh_missing_token(self, client):
        """不带 Authorization 头发请求，应返回 401"""
        api = RefreshAPI(client)
        resp = api.call()

        with allure.step("校验缺少 token"):
            assert resp.status_code == 401
            assert resp.msg == "missing token"
            assert resp.token is None

    @allure.title("刷新 token - 无效 token")
    def test_refresh_invalid_token(self, client):
        """带一个从未签发过的 token"""
        client.session.headers.update({"Authorization": "Bearer fake-token-123"})
        api = RefreshAPI(client)
        resp = api.call()

        with allure.step("校验无效 token"):
            assert resp.status_code == 403
            assert resp.msg == "invalid token"
            assert resp.token is None

    @allure.title("刷新 token - token 过期")
    def test_refresh_expired_token(self, client, auth_token):
        """用已过期的 token 刷新（token 3 秒过期），需要独立的、未被删除的 token"""
        # 1. 先登录，得到一个临时 token
        from core.api.login_api import LoginAPI, LoginRequest
        login_api = LoginAPI(client)
        login_resp = login_api.call(LoginRequest(username="arena", password="1sf8d6"))
        assert login_resp.status_code == 200
        temp_token = login_resp.token

        # 2. 等待 token 过期
        time.sleep(4)

        # 3. 用过期 token 请求刷新
        client.session.headers.update({"Authorization": f"Bearer {temp_token}"})
        refresh_api = RefreshAPI(client)
        resp = refresh_api.call()

        with allure.step("校验 token 过期"):
            assert resp.status_code == 401
            assert resp.msg == "token expired"
            assert resp.token is None