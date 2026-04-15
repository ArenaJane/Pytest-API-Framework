def assert_response(response, expected):
    if 'status_code' in expected:
        expected_code = expected['status_code']
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"状态码不匹配！期望: {expected_code}, 实际: {actual_code}\n" \
            f"响应内容: {response.text}"

    if 'body' in expected:
        res_json = response.json()
        for key, value in expected['body'].items():
            assert res_json.get(key) == value

    if 'contains' in expected:
        response_data = response.json()
        for key, value in expected['contains'].items():
            if value == "":
                # 只检查字段是否存在
                assert key in response_data, f"响应中缺少字段: {key}"
            else:
                actual_value = response_data.get(key, "")
                assert value in actual_value, \
                    f"字段 '{key}' 不包含期望值\n" \
                    f"期望包含: '{value}'\n" \
                    f"实际值: '{actual_value}'"