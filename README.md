# Pytest-API-Framework

🚀 **一款基于 Python 的接口自动化测试框架，融合了接口对象化、数据驱动与生产级工程实践，专为高质量测试与简历亮点而生。**

## ✨ 核心特性

- **接口对象化封装**：告别裸字典，每个 API 都是一个 `XXXAPI` 类，请求/响应均由 `dataclass` 强类型定义，代码即文档，IDE 自动补全。
- **数据驱动测试**：使用 YAML 管理测试用例数据，`pytest.mark.parametrize` 自动加载执行，一条命令跑完所有场景。
- **优雅的依赖管理**：通过 `pytest fixture` 实现登录 token 的自动注入与复用，无需硬编码或全局变量。
- **全面的断言能力**：支持状态码校验、关键字包含、JSON Schema 结构验证（可选），并可轻松扩展。
- **清晰的工程分层**：`core/api` 存放业务接口对象，`models` 存放数据模型，`tests` 存放用例，`utils` 提供通用工具，职责分明。
- **Allure 报告集成**：内置 `allure-pytest` 支持，生成美观的测试报告。
- **零耦合数据管理**：测试数据与代码完全分离，维护数据时无需触碰逻辑代码。

## 📦 快速开始

### 环境要求
- Python 3.8+
- 已安装依赖（见 `requirements.txt`）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置
编辑 `config/settings.yaml`（或你实际使用的配置文件），设置被测系统的 `base_url` 等参数。

### 运行测试
```bash
# 运行全部测试
pytest

# 生成 Allure 报告
pytest --alluredir=report
allure serve report
```

## 📁 目录结构

```
Pytest-API-Framework/
├── config/                 # 全局配置文件
├── core/                   # 核心模块
│   ├── api/                # 接口对象层（每个 API 一个类）
│   │   ├── login_api.py    # 登录接口对象
│   │   └── user_info_api.py# 用户信息接口对象
├── data/                   # 测试数据（YAML）
│   ├── login.yaml          # 登录相关用例数据
│   └── user.yaml           # 用户基础数据（供其他工具使用）
├── models/                 # 通用数据模型（请求/响应/用例结构）
│   └── api_models.py
├── tests/                  # 测试用例
│   ├── conftest.py         # fixture 定义（client, auth_client 等）
│   ├── test_login.py       # 登录模块测试
│   ├── test_user_info.py   # 用户信息模块测试
│   └── test_refresh.py     # 刷新模块测试
├── utils/                  # 工具集（请求封装、YAML加载、断言、日志等）
│   ├── request.py
│   ├── file_loader.py
│   ├── assert_utils.py
│   └── logger.py
├── logs/                   # 运行日志
├── report/                 # Allure 报告输出
├── temps/                  # 临时文件
├── app.py                 # 自建的flask应用，用于测试
└── README.md
```

## 🧪 使用示例

### 1. 定义接口对象（`core/api/login_api.py`）

```python
from dataclasses import dataclass
from typing import Optional

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
        self.url = "/login"

    def call(self, request: LoginRequest) -> LoginResponse:
        resp = self.client.send("POST", self.url, json={
            "username": request.username,
            "password": request.password
        })
        data = resp.json()
        return LoginResponse(
            status_code=resp.status_code,
            msg=data.get("msg"),
            token=data.get("token")
        )
```

### 2. 编写数据驱动用例（`tests/test_login.py`）

```python
import pytest
from core.api.login_api import LoginAPI, LoginRequest
from models.api_models import YamlTestCase, load_yaml_cases

@pytest.mark.parametrize("case", load_yaml_cases("data/login.yaml"))
def test_login(case, client):
    req = LoginRequest(**case.request.json)
    resp = LoginAPI(client).call(req)
    assert resp.status_code == case.expected.status_code
    assert resp.msg == case.expected.contains.get("msg")
```

### 3. 利用 Fixture 自动处理登录态

```python
# conftest.py 已定义 auth_client fixture，自动注入 token
def test_get_user_info(auth_client):
    res = auth_client.send("GET", "/user/info")
    assert res.status_code == 200
    assert res.json()["username"] == "arena"
```

## 🔧 技术栈

- **Python 3.8+** · **pytest** · **requests** · **PyYAML** · **Allure**
- **dataclasses** · **pytest fixtures** · **设计模式：对象封装 / 数据驱动**

## 🗺️ 后续规划

- [ ] 接入 `attrs` 增强数据校验
- [ ] 集成 JSON Schema 断言
- [ ] 扩展为分布式测试执行平台（对接 `Distributed-Test-Platform`）
- [ ] 加入 LLM 驱动的测试用例自动生成（AI 测试）

---

> 本项目源于一个简单的接口自动化练习，经过 **接口对象化重构**、**数据驱动升级** 和 **登录态管理优化**，已具备企业级自动化测试框架的雏形.
