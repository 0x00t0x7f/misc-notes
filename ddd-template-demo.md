## 🌐 DDD 分层架构项目结构模板（推荐）

```
project-ddd-template/
│
├── main.py                         # FastAPI 应用入口
│
├── app/
│   ├── domain/                    # 领域层：核心业务逻辑
│   │   ├── entities/             # 实体（Entity）
│   │   ├── value_objects/       # 值对象（Value Object）
│   │   ├── enums/                 # 枚举类型（如状态、角色）
│   │   ├── services/              # 领域服务（Domain Service）
│   │   ├── repositories/          # 领域仓库接口（Repository Interface）
│   │   └── events/                 # 领域事件（Domain Event）
│   │
│   ├── application/               # 应用层：协调领域逻辑，处理用例
│   │   ├── use_cases/            # 用例（Use Case）
│   │   ├── dtos/                   # 数据传输对象（DTO）
│   │   ├── mappers/                # 映射器（DTO ↔ Entity）
│   │   ├── exceptions/             # 应用层自定义异常
│   │   └── services/               # 应用服务（Application Service）
│   │
│   ├── infrastructure/            # 基础设施层：技术实现，解耦领域
│   │   ├── storage/                # 文件存储（本地/云）
│   │   ├── database/               # 数据库（SQLAlchemy/Prisma等）
│   │   ├── messaging/              # 消息队列（WebSocket/RabbitMQ/Kafka）
│   │   ├── cache/                  # 缓存实现（Redis）
│   │   ├── email/                  # 邮件发送服务
│   │   ├── security/               # 安全工具（JWT、密码加密）
│   │   └── config.py               # 配置加载（如数据库连接、Redis地址）
│   │
│   ├── api/                         # API 层（可选，也可合并到 app）
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routers/
│   │   │   │   ├── upload.py
│   │   │   │   └── status.py
│   │   │   └── schemas/
│   │   │       ├── upload.py
│   │   │       └── status.py
│   │   └── websocket/
│   │       └── handlers.py
│   │
│   └── config.py                    # 全局配置（可选）
│
├── tests/
│   ├── unit/
│   │   ├── test_domain/
│   │   │   ├── test_resume_entity.py
│   │   │   └── test_parser_service.py
│   │   └── test_application/
│   │       └── test_use_case.py
│   ├── integration/
│   │   └── test_api_endpoints.py
│   └── conftest.py
│
├── .env
├── pyproject.toml
├── README.md
└── docker-compose.yml
```

---

## 📚 各层详细作用与设计原则

---

### 1. **`domain` 层 —— 领域层（核心）**

> ✅ **作用：**  
> 封装**核心业务规则、实体、值对象、领域服务和领域事件**。  
> 是系统“最懂业务”的部分，**不依赖任何外部框架或技术**。

> 🔑 **设计原则：**
> - 与框架无关（无 `FastAPI`, `SQLAlchemy` 等依赖）
> - 严禁引入外部服务（如数据库、邮件、HTTP 客户端）
> - 实体应有唯一标识（ID）和行为方法
> - 值对象不可变，强调“意义”而非身份

> 📌 **典型内容：**
> - `entities/resume.py`：简历实体（包含姓名、技能、工作经历等）
> - `value_objects/file_hash.py`：文件哈希（不可变，用于去重）
> - `enums/status.py`：处理状态（`UPLOADED`, `PARSING`, `COMPLETED`）
> - `services/resume_parser_service.py`：解析服务（调用 OCR/NLP，但不直接操作数据库）
> - `events/resume_parsed_event.py`：领域事件（如“简历已解析”）

---

### 2. **`application` 层 —— 应用层（协调者）**

> ✅ **作用：**  
> 管理**业务用例的执行流程**，协调领域层与基础设施层。  
> 是“指挥官”——决定何时调用哪个服务，如何处理异常。

> 🔑 **设计原则：**
> - 不包含业务规则（业务逻辑必须在 `domain` 层）
> - 用例应以“用户视角”命名（如 `UploadResumeUseCase`）
> - 使用 DTO 进行数据传输，避免将实体暴露给外部
> - 可引入应用服务（如 `EmailNotificationService`）但应通过接口注入

> 📌 **典型内容：**
> - `use_cases/upload_resume.py`：上传简历用例（调用领域服务、发布事件）
> - `dtos/resume_dto.py`：数据传输对象（用于 API 返回）
> - `mappers/resume_mapper.py`：实体与 DTO 的映射器
> - `exceptions/resume_exception.py`：应用层自定义异常（如 `ResumeNotFound`）

---

### 3. **`infrastructure` 层 —— 基础设施层（技术实现）**

> ✅ **作用：**  
> 提供**技术实现**，如数据库、文件存储、消息队列、缓存等。  
> 它**依赖于 `domain` 和 `application` 的抽象接口**，实现具体功能。

> 🔑 **设计原则：**
> - 封装所有外部依赖（数据库、HTTP 客户端等）
> - 通过接口与上层解耦（如 `RepositoryInterface` → `SqlAlchemyResumeRepository`）
> - 不包含业务逻辑，只做“如何做”
> - 支持注入（依赖注入，如 `DependencyInjector`）

> 📌 **典型内容：**
> - `database/models.py`：SQLAlchemy 模型（映射数据库表）
> - `database/repositories/resume_repository.py`：简历仓库实现（继承抽象接口）
> - `storage/local_storage.py`：本地文件存储实现
> - `messaging/message_broker.py`：WebSocket 或 RabbitMQ 消息发布器
> - `security/jwt_service.py`：JWT 生成与验证服务

---

### 4. **`api` 层 —— API 层（入口）**

> ✅ **作用：**  
> 提供**对外接口**（HTTP、WebSocket、gRPC 等），接收请求、验证参数、调用应用层用例，并返回结果。

> 🔑 **设计原则：**
> - **不处理业务逻辑**，只做“路由”和“参数校验”
> - 使用 `FastAPI` 的依赖注入机制，注入 `UseCase` 实例
> - 接口应清晰、文档化（自动 OpenAPI 文档）

> 📌 **典型内容：**
> - `routers/upload.py`：上传接口路由（POST `/upload`）
> - `schemas/upload.py`：请求/响应数据模型（Pydantic）
> - `websocket/handlers.py`：WebSocket 消息处理逻辑

---

## 🎯 总结：各层职责清晰划分

| 层级 | 职责 | 是否可依赖外部框架？ |
|------|------|--------------------------|
| `domain` | 核心业务逻辑、实体、规则 | ❌ 否（纯净领域） |
| `application` | 用例编排、流程控制 | ✅ 是（但不包含业务逻辑） |
| `infrastructure` | 技术实现（DB、存储、消息） | ✅ 是（依赖外部系统） |
| `api` | 接收外部请求，返回响应 | ✅ 是（HTTP/WebSocket） |

---

## ✅ 使用建议

- 项目初期：先搭建 `domain` 和 `application`，再逐步实现 `infrastructure`
- 测试策略：单元测试重点在 `domain` 和 `application`；集成测试关注 `api` 与 `infrastructure` 的协作
- 扩展性：未来可以轻松替换数据库（MySQL → PostgreSQL）、消息队列（Redis → Kafka）



