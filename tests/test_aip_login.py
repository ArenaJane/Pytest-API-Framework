# import os
#
# import allure
# import pytest
# import time
# from utils.config_loader import config
# from utils.file_loader import load_yaml, write_yaml
# from utils.assert_utils import assert_response
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, config['data']['login_file'])
#
# data_list = load_yaml(DATA_PATH)
import os
import sys
import allure
import pytest
from pathlib import Path
from core.api.login_api import LoginAPI, LoginRequest
from utils.file_loader import load_yaml
from models.api_models import YamlTestCase, RequestSpec, ExpectedSpec
from utils.config_loader import config

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def login_cases():
    yaml_file = os.path.join(project_root, config['data']['login_file'])
    raw = load_yaml(yaml_file)
    cases = []
    for item in raw:
        cases.append(YamlTestCase(
            name=item['name'],
            request=RequestSpec(**item['request']),
            expected=ExpectedSpec(**item['expected'])
        ))
    return cases

@pytest.mark.parametrize('case', login_cases())
@allure.feature("登录——数据驱动")
def test_login_with_yaml(case, client):
    with allure.step(f"执行用例: {case.name}"):
        with allure.step(f"用例: {case.name}"):
            req = LoginRequest(**case.request.json)
            resp = LoginAPI(client).call(req)

    with allure.step("校验响应"):
        assert resp.status_code == case.expected.status_code
        if case.expected.contains:
            assert resp.msg == case.expected.contains.get("msg")
            if "token" in case.expected.contains:
                assert resp.token == case.expected.contains["token"]

def test_login_success(client):
    with allure.step("使用正确的用户名和密码登录"):
        api = LoginAPI(client)
        req = LoginRequest(username="arena", password="1sf8d6")
        resp = api.call(req)

    with allure.step("校验登录成功返回"):
        assert resp.status_code == 200
        assert resp.msg == "Login successfully"
        assert resp.token == "token-arena"

def test_login_fail(client):
    with allure.step("使用错误的密码登录"):
        api = LoginAPI(client)
        req = LoginRequest(username="arena", password="wrongpassword")
        resp = api.call(req)

    with allure.step("校验登录失败返回"):
        assert resp.status_code == 401
        assert resp.msg == "Login failed"
        assert resp.token is None
# @pytest.mark.parametrize('data', data_list)
# def test_aip_login(data, client):
#     with allure.step("测试登录"):
#         response = client.send(method=data['method'], url=data['url'], json=data['json'])
#         print(response.json())
#         assert_response(response, expected=data['expected'])
#
# def test_get(client):
#     with allure.step("测试请求"):
#         res = client.send('GET', '/user/info')
#         print(res.json())
#         assert res.status_code == 200
#         assert res.json()['username'] == 'arena'
#
# def test_user_info(client):
#     with allure.step("测试刷新"):
#         res = client.send('GET', '/user/info')
#         print(res.json())
#         time.sleep(4)
#         res = client.send('GET', '/user/info')
#         print(res.json())