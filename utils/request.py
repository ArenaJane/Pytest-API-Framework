import requests
import allure

class Request:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def send(self, method, url, retry=True, **kwargs):

        full_url = self.base_url + url

        with allure.step(f"请求接口 {method} {full_url}"):
            res = self.session.request(method, full_url, **kwargs)
            allure.attach(str(res.text), '响应数据')

            if res.status_code == 401 and retry:
                with allure.step("token过期, 尝试刷新token"):
                    if self.refresh_token():
                        with allure.step("刷新token成功，重新发送请求"):
                            return self.send(method, url, retry=False, **kwargs)

        return res

    def refresh_token(self):
        full_url = self.base_url + '/refresh'
        with allure.step(f"刷新 Token: POST {full_url}"):
            res = self.session.post(full_url)
            if res.status_code == 200:
                new_token = res.json().get('token')
                self.session.headers.update({
                    'Authorization': f'Bearer {new_token}'
                })
                allure.attach(new_token, '新Token')
                return True

        return False