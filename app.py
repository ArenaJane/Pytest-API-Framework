from flask import Flask, request, jsonify
import time
import allure

app = Flask(__name__)

USER_DB = {
    'arena': '1sf8d6'
}

TOKENS = {}

@app.route('/login', methods=['POST'])
def login():
    with allure.step("请求登录:"):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print(f"用户数据库: {USER_DB}")
        print(f"输入的用户名: {username}")
        print(f"输入的密码: {password}")
        print(f"数据库中的密码: {USER_DB.get(username)}")
        with allure.step("验证用户名和密码"):
            if USER_DB.get(username) == password:
                print("✅ 密码验证成功")
                token = f"token-{username}"
                TOKENS[token] = {
                    'username': username,
                    'expire': time.time() + 3  # 3秒后过期
                }
                with allure.step("生成并返回token"):
                    return jsonify({
                        'msg': 'Login successfully',
                        'token': token
                    })
            else:
                print("❌ 密码验证失败")
                with allure.step("返回登录失败"):
                    return jsonify({
                        'msg': 'Login failed'
                    }), 401

@app.route('/user/info', methods=['GET'])
def user_info():
    with allure.step("用户信息请求"):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            with allure.step("token缺失"):
                return jsonify({'msg': 'missing token'}), 401

        token = auth_header.replace('Bearer ', '')
        user_data = TOKENS.get(token)

        if not user_data:
            with allure.step("无效token"):
                return jsonify({'msg': 'invalid token'}), 403

        username = user_data.get('username')

        if not username:
            with allure.step("无效用户信息"):
                return jsonify({'msg': 'invalid user data'}), 403

        if time.time() > user_data.get('expire', 0):
            with allure.step("token过期，请刷新token"):
                return jsonify({'msg': 'token expired'}), 401

    with allure.step("返回用户信息"):
        return jsonify({
            'username': username,
            'role': 'tester'
        })

@app.route('/refresh', methods=['POST'])
def refresh():
    with allure.step("刷新请求"):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            with allure.step("token缺失"):
                return jsonify({'msg': 'missing token'}), 401

        token = auth_header.replace('Bearer ', '')
        user_info = TOKENS.get(token)

        if not user_info:
            with allure.step("无效token"):
                return jsonify({'msg': 'invalid token'}), 403

        if time.time() > user_info.get('expire', 0):
            with allure.step("token过期, 请刷新token"):
                return jsonify({'msg': 'token expired'}), 401

        username = user_info['username']
        new_token = f"token-{username}-new"
        with allure.step("生成新token并更新存储"):
            TOKENS[new_token] = {
                'username': username,
                'expire': time.time()+3
            }
            del TOKENS[token]
        with allure.step("返回新token"):
            return jsonify({'token': new_token})

if __name__ == '__main__':
    app.run(debug=True)