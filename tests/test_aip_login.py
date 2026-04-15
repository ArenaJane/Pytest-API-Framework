import os

import allure
import pytest
import time
from utils.config_loader import config
from utils.file_loader import load_yaml, write_yaml
from utils.assert_utils import assert_response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, config['data']['login_file'])

data_list = load_yaml(DATA_PATH)

@pytest.mark.parametrize('data', data_list)
def test_aip_login(data, client):
    with allure.step("测试登录"):
        response = client.send(method=data['method'], url=data['url'], json=data['json'])
        print(response.json())
        assert_response(response, expected=data['expected'])

def test_get(client):
    with allure.step("测试请求"):
        res = client.send('GET', '/user/info')
        print(res.json())
        assert res.status_code == 200
        assert res.json()['username'] == 'arena'

def test_user_info(client):
    with allure.step("测试刷新"):
        res = client.send('GET', '/user/info')
        print(res.json())
        time.sleep(4)
        res = client.send('GET', '/user/info')
        print(res.json())