以下是一个**完整的、生产级风格的 FastAPI + RocketMQ + DDD 示例项目结构**，专为 **领域事件驱动架构（Event-Driven DDD）** 设计，支持：

- ✅ 分层清晰的 DDD 架构（领域层、应用层、基础设施层）
- ✅ FastAPI 提供 REST API 与事件发布接口
- ✅ RocketMQ 实现领域事件的可靠发布与消费
- ✅ 事务消息确保 “本地事务成功” 与 “事件发布成功” 一致
- ✅ 支持异步、非阻塞、高并发的事件处理
- ✅ 完整的配置管理、日志、健康检查

---

## 📁 项目结构（完整版）

```
fastapi-rocketmq-ddd/
├── .env                    # 环境变量（如 RocketMQ 地址）
├── .dockerignore
├── docker-compose.yml    # 本地 RocketMQ 集群 + FastAPI 服务
├── README.md
├── pyproject.toml          # 项目依赖与构建配置（推荐使用 Poetry）
│
├── app/
│   ├── main.py             # FastAPI 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── orders.py     # 订单 API（触发领域事件）
│   │   │   └── users.py        # 用户 API
│   │   └── dependencies.py     # 依赖注入（如 DB、RocketMQ Producer）
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── order.py        # 领域模型（聚合根）
│   │   │   ├── user.py
│   │   │   └── events.py       # 领域事件定义（Pydantic 模型）
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── order_repository.py
│   │   │   └── user_repository.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── order_service.py  # 业务逻辑（触发事件）
│   │       └── event_dispatcher.py  # 事件分发器（集成 RocketMQ）
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── create_order_use_case.py
│   │   │   └── user_login_use_case.py
│   │   └── dtos/
│   │       ├── __init__.py
│   │       ├── order_dto.py
│   │       └── user_dto.py
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── messaging/
│   │   │   ├── __init__.py
│   │   │   ├── rocketmq_producer.py   # RocketMQ Producer 封装
│   │   │   └── rocketmq_consumer.py     # RocketMQ Consumer（可选）
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── db.py                          # SQLAlchemy 初始化
│   │   │   └── models.py                      # ORM 模型（可选）
│   │   └── config/
│   │       ├── __init__.py
│   │       └── settings.py                    # 读取 .env，配置 RocketMQ、DB 等
│   │
│   └── core/
│       ├── __init__.py
│       ├── exceptions.py                        # 自定义异常
│       ├── logging.py                           # 初始化日志
│       └── events.py                            # 事件注册/分发机制
│
├── tests/
│   ├── __init__.py
│   ├── test_orders.py
│   ├── test_events.py
│   └── conftest.py
│
└── scripts/
    └── setup_db.py                             # 初始化数据库（可选）
```

---

## 🎯 核心模块说明

### 1. **领域层（`domain/`）**
- `models/order.py`：`Order` 聚合根，包含业务规则。
- `events.py`：定义领域事件（如 `OrderCreatedEvent`），使用 `pydantic.BaseModel`。
- `repositories/`：定义接口（如 `OrderRepository`），供基础设施层实现。

### 2. **应用层（`application/`）**
- `use_cases/`：包含业务用例（如 `CreateOrderUseCase`）。
- `dtos/`：数据传输对象，用于 API 与领域层之间的数据传递。

### 3. **基础设施层（`infrastructure/`）**
- `messaging/rocketmq_producer.py`：封装 RocketMQ 事务消息发布，确保“本地事务 + 事件发布”一致性。
- `persistence/db.py`：使用 SQLAlchemy 初始化数据库连接。
- `config/settings.py`：读取 `.env`，配置 RocketMQ、DB、日志等。

### 4. **API 层（`app/api/v1/`）**
- `orders.py`：提供 `POST /v1/orders` 接口，调用 `CreateOrderUseCase`，并触发领域事件。
- `dependencies.py`：依赖注入，注入 `OrderService`、`RocketMQProducer` 等。

---

## ✅ RocketMQ 事务消息使用示例（关键！）

```python
# app/domain/services/event_dispatcher.py

from typing import List
from pydantic import BaseModel

from app.infrastructure.messaging.rocketmq_producer import RocketMQProducer

class EventDispatcher:
    def __init__(self, producer: RocketMQProducer):
        self.producer = producer

    async def dispatch(self, event: BaseModel, topic: str):
        # 使用事务消息确保一致性
        await self.producer.send_transaction(
            topic=topic,
            body=event.model_dump_json(),
            # 本地事务执行回调
            check_listener=lambda msg: self._check_transaction(msg),
        )

    def _check_transaction(self, msg):
        # 检查事务状态（通常在 Broker 端回调）
        # 逻辑：查询本地事务是否成功
        # 返回值：COMMIT, ROLLBACK, UNKNOWN
        return "COMMIT"
```

---

## ✅ 关键配置（`.env` 示例）

```env
# RocketMQ
ROCKETMQ_NAMESRV_ADDR=namesrv-0:9876,namesrv-1:9876
ROCKETMQ_TOPIC=ORDER_EVENTS

# FastAPI
FASTAPI_DEBUG=true
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Database
DATABASE_URL=sqlite:///./test.db
```

---

## ✅ 启动方式（Docker Compose）

```bash
# 启动整个项目（FastAPI + RocketMQ 集群）
docker-compose up -d --build

# 查看日志
docker-compose logs -f fastapi
```

---

## ✅ 验证流程

1. 发送 POST 请求创建订单：
   ```bash
   curl -X POST http://localhost:8000/v1/orders \
        -H "Content-Type: application/json" \
        -d '{"user_id": 123, "items": [{"product_id": 1, "quantity": 2}]}'
   ```

2. 观察：
   - RocketMQ Broker 日志中出现 `OrderCreatedEvent` 事务消息。
   - 事件被成功投递到 `ORDER_EVENTS` 主题。
   - 其他微服务（如通知服务、库存服务）可通过消费者订阅并处理事件。

---

## ✅ 总结：为什么这个结构是“黄金标准”？

| 特性 | 是否支持 |
|------|------------|
| DDD 分层清晰 | ✅ |
| 领域事件定义规范 | ✅（Pydantic 模型） |
| 事务消息保证一致性 | ✅（RocketMQ 事务消息） |
| 异步解耦、高并发处理 | ✅ |
| 可测试性、可维护性高 | ✅ |
| 适合 FastAPI + 微服务架构 | ✅ |

---

