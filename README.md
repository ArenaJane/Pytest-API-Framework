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

下面帮你把 `Pytest-API-Framework` 这个项目，从“看似能跑”到“工程级框架”的整个蜕变过程，整理成一份可以直接用于简历复盘、面试讲述、或者项目总结笔记的完整文档。

---

## Pytest-API-Framework 项目总结

### 一、项目实现了什么

一个**接口对象化、数据驱动、登录态自动管理**的接口自动化测试框架。它从最初一个结构松散、逻辑混乱的“脚本集合”，被重构为一个职责清晰、可扩展性强的工程化测试框架，能高效覆盖登录、用户信息等接口的正反向测试场景。

### 二、运用的技术栈

- **Python 3.8+** · **pytest** · **requests** · **PyYAML** · **Allure**
- **dataclasses**（强类型数据模型）
- **pytest fixture**（依赖注入、作用域控制）
- **设计模式**：接口对象封装、数据驱动测试、单一职责原则
- **测试数据分离**：YAML 管理用例数据与预期结果

### 三、核心修改与重构路径

| 阶段 | 核心动作 | 解决的问题 |
|------|----------|------------|
| **1. 去伪存真** | 删除 `core/user.py` 伪 `User` 类，创建 `core/api/login_api.py`，封装真正的 HTTP 登录接口 | 旧 `User.login()` 读写本地 YAML 而非调用接口，测试与实现脱节 |
| **2. 接口对象化** | 用 `dataclass` 定义 `LoginRequest`、`LoginResponse`，`LoginAPI.call()` 返回强类型对象 | 告别字典取值，IDE 可自动补全，字段变更时编译器报错 |
| **3. 登录态管理重构** | 拆分 `client` 为纯 HTTP 客户端，新增 `auth_token`（session级别登录）和 `auth_client`（function级别注入token） | 旧代码在 `client` 中硬编码登录，无法测试未登录场景，状态污染 |
| **4. 数据驱动升级** | 定义 `YamlTestCase` 等通用模型，改写 `login.yaml` 结构，用 `pytest.mark.parametrize` 加载所有用例 | 实现一条命令跑完所有登录场景，新增用例只需加 YAML 数据 |
| **5. 扩展接口** | 封装 `UserInfoAPI` 并编写正/反向测试（含未登录测试） | 验证框架的可扩展性，覆盖越权场景 |
| **6. 问题攻坚** | `test_user_info_without_token` 预期 401 却返回 200，排查发现 `client` 作用域设为 `session` 导致 token 残留，改为 `function` 级别解决 | 深入理解 pytest fixture 作用域与状态污染风险 |

### 四、项目提升的关键能力

| 维度 | 提升前 | 提升后 |
|------|--------|--------|
| **代码可读性** | 用例中遍布 `data['method']`、`resp.json()['token']` 等魔法字符串 | 用例变成 `LoginAPI(client).call(req).token`，语义清晰 |
| **可维护性** | 接口字段改动需要全局搜索替换 | 只需修改对应 `dataclass` 定义，所有引用处自动报错提醒 |
| **测试独立性** | 登录 token 硬编码或藏在全局变量 | 通过 `auth_client` fixture 显式注入，每个测试干净隔离 |
| **数据管理** | YAML 数据与测试逻辑混杂 | 代码与数据完全分离，通过 `parametrize` 灵活组合 |
| **工程思维** | 一个“能跑”的脚本 | 分层清晰（模型层、接口层、工具层、测试层），具备企业级框架雏形 |

### 五、需注意的关键细节

1. **Pytest Fixture 作用域陷阱**  
   `scope='session'` 的 `client` 会在所有测试间共享同一个 session，若在其中注入 token，则所有测试都会带上认证信息，导致“未登录测试”永远通过。**解决方案**：`client` 保持无状态（`scope='function'`），需要 token 时使用独立的 `auth_client`。

2. **状态恢复**  
   在 `auth_client` 中修改 `client.session.headers` 后，务必用 `yield` 后恢复原始 headers，避免污染其他测试。

3. **数据模型与 YAML 结构对齐**  
   使用嵌套 `dataclass` 反序列化 YAML 时，YAML 文件的结构必须与类属性完全一致，否则会报错。建议先写模型，再按模型定义 YAML。

4. **删除旧代码要彻底**  
   旧 `user.py` 和 `temp_data_file`、`user_factory` 等 fixture 必须全量移除，避免新人或未来自己误 import。

### 六、遇到的问题与攻克过程

**问题**：`test_user_info_without_token` 预期返回 401，实际返回 200。  
**排查过程**：
- 检查 `client` fixture 代码，发现原本 `scope='session'` 且在 fixture 内部硬编码了 `headers.update(Authorization)`。
- 即便我们后来把登录逻辑拆到 `auth_token` 中，但 `client` 的 scope 仍是 session，一旦某个测试用到了 `auth_client`，token 就会被写入共享的 session headers。
- 因此即使后续测试直接使用 `client`，请求头里仍残留之前的 token。

**攻克方法**：
- 将 `client` 的 `scope` 改为 `function`，每个测试获得一个全新的客户端实例。
- 同时确保 `auth_client` 每次执行时临时注入 token，并在用后恢复，彻底杜绝状态污染。

**教训**：Pytest 的 fixture 作用域是双刃剑。`session` 级别适用于昂贵的初始化（如数据库连接），但绝不能用于可能被污染的请求客户端。
