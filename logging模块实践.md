使用 Python 的 `logging` 模块构建一个**高性能、可审计、易排查问题**的系统日志，是生产环境中的关键实践。

## 写在前
先了解日志等级以及每个日志等级的特点
| 日志等级 | 特点 | 作用 |
|----------|------|------|
| `DEBUG` | 详细调试信息，仅开发环境使用 | 排查问题、跟踪逻辑流程 |
| `INFO` | 正常运行信息，关键业务流程记录 | 监控系统状态、确认操作成功 |
| `WARNING` | 潜在问题或异常，但不影响运行 | 提醒注意，如资源不足、配置异常 |
| `ERROR` | 错误发生，功能部分失效 | 记录故障，便于快速定位修复 |
| `CRITICAL` | 严重错误，系统可能崩溃或不可用 | 紧急告警，需立即处理 |

> ✅ **生产环境建议**：仅启用 `INFO` 及以上，禁用 `DEBUG` 以提升性能。

---

## ✅ 一、设计原则

| 原则 | 说明 |
|------|------|
| **性能优先** | 生产环境避免阻塞、避免大量字符串拼接 |
| **信息完整** | 包含时间、模块、级别、请求上下文、错误堆栈等 |
| **分级控制** | 开发环境详细，生产环境精炼但关键信息不丢 |
| **可审计** | 关键操作（如登录、支付、权限变更）必须记录 |
| **结构化输出** | 使用 JSON 格式，便于日志聚合与分析（如 ELK、Prometheus + Loki） |

---

## ✅ 二、日志系统整体架构设计

```
[ 应用代码 ]
     ↓
[ logging 模块 + 自定义 Handler ]
     ↓
[ 日志输出：文件 + 控制台 + 可选远程（如 Syslog, Kafka）]
```

**执行流程**
```
[Logger] 
   │
   ▼
[Message + Context]   ← 日志内容 + 上下文（如 user_id, request_id）
   │
   ▼
[Filter(s)] ←─────────────┐
   │                           │
   ▼                           ▼
[Formatter(s)] ←─────────────┘
   │
   ▼
[Handler(s)] 
   │
   ▼
[Output] → 文件 / 控制台 / HTTP / DB / Kafka 等
```


---

## ✅ 三、配置方案（推荐 `dictConfig`）

### ✅ 1. 基础配置：`logging_config.py`

```python
import logging
import logging.config
import os
from datetime import datetime

# 获取当前环境（开发/生产）
ENV = os.getenv("ENV", "development").lower()

# 日志文件路径
LOG_DIR = os.getenv("LOG_DIR", "./logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 生成日志文件名（按天切割）
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y%m%d')}.log")

# 配置字典模板（核心）
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "format": "%(asctime)s %(name)s %(levelname)s %(funcName)s %(lineno)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d | %(funcName)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO" if ENV == "production" else "DEBUG",
            "formatter": "detailed",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO" if ENV == "production" else "DEBUG",
            "formatter": "json" if ENV == "production" else "standard",
            "filename": LOG_FILE,
            "maxBytes": 50 * 1024 * 1024,  # 50MB
            "backupCount": 5,
            "encoding": "utf-8"
        },
        "audit": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": os.path.join(LOG_DIR, "audit.log"),
            "maxBytes": 100 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "DEBUG" if ENV == "development" else "INFO",
            "propagate": False
        },
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO" if ENV == "production" else "DEBUG",  # 和 handlers的level作用不同：分层控制，实现灵活细粒度的日志过滤
            "propagate": False  # 当前 logger 的日志是否继续传递给其祖先 logger（即父 logger），默认为True
        },
        "audit": {
            "handlers": ["audit"],
            "level": "INFO",
            "propagate": False
        }
    }
}

# 应用配置
def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")  # logging.getLogger("app.user") 子logger， logging.getLogger("app.user.auth") 更深层的子 logger  它们之间是继承关系，除非被显式覆盖
    # logger = logging.getLogger("undefined_logger")  配置中没定义的 logger，不会自动绑定 handler 和 formatter，即不会有日志传递和输出
    logger.info(f"Logging initialized for {ENV} environment")
    return logger
```

> 💡建议：子 logger 尽量不自己加 handler，而是通过配置继承父 logger 的 handler

### formaters、handlers、loggers 区别

|组件	|作用	|说明|
|---|---|---|
|filters| 过滤器| 决定是否输出、脱敏、加标签、防止日志爆炸（限流）|
|formatters	|定义日志的输出格式（如时间、级别、消息、上下文等）	|决定日志“长什么样”，支持结构化输出（如JSON）|
|handlers	|定义日志的输出目的地和方式（如文件、控制台、网络等）|	决定日志“去哪儿”，可绑定多个 formatters 和 level|
|loggers	|日志的逻辑入口，用于生成日志记录，控制日志是否被处理|	每个模块/类可以有自己的 logger，是日志体系的“源头”|

> ✅ 关系链：
logger → 产生日志 → 根据 level 决定是否传递给 handlers
handler → 使用 formatter 格式化日志 → 写入目标（文件/控制台等）
> 一句话总结：日志从 logger 出发，经过 filter 逐条判断是否该处理，再由 formatter 格式化内容，最后交给 handler 输出到目标位置


### 日志是如何被处理的？（日志决策树）
```
是否在 app_logger 添加 handler？
        │
        ├── 是 → 日志先输出到 app 的 handler（如控制台）
        │         ↓
        │         是否 propagate = True?
        │         ├── 是 → 日志传给 root_logger
        │         │         ↓
        │         │         root_logger 的 handler 是否被触发？
        │         │         ├── 是 → 发往 ELK（重复！）
        │         │         └── 否 → 不发（不重复！）
        │         └── 否 → 不传 → 不影响 root
        │
        └── 否 → 日志不输出到 app 的 handler
                  ↓
                  是否 propagate = True?
                  ├── 是 → 日志传给 root → 若 root 被调用 → handler 触发 → 发往 ELK
                  └── 否 → 不传 → 不影响 root

```

### 如何在项目中配置loggers？
原则：一个项目，一个 root logger；模块按需创建子 logger；所有日志最终统一由 root 处理输出。

**日志结构：层级命名+模块化**
```
# 例如：
logging.getLogger("app")              # 整个应用
logging.getLogger("app.api")          # API 模块
logging.getLogger("app.db")           # 数据库模块
logging.getLogger("app.utils")        # 工具函数
logging.getLogger("app.service")      # 业务逻辑
```
> ✅ 命名建议：<项目名>.<模块名>，比如 app.api, app.core, app.worker

**根logger配置（只配一次）**
```
# config_logging.py 或 main.py 中统一配置
import logging

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 确保 root 没有重复 handler（防重复打印）
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
```
> ✅ 重要：只在应用启动时调用一次 setup_logging()，避免重复添加 handler。

**模块内日志使用（规范写法）**
```
# app/api.py
import logging

logger = logging.getLogger("app.api")  # 用模块名命名

def get_user(user_id):
    logger.debug("开始查询用户，user_id=%d", user_id)
    try:
        # 模拟数据库查询
        user = {"id": user_id, "name": "张三"}
        logger.info("成功查询用户: %s", user)
        return user
    except Exception as e:
        logger.error("查询用户失败，user_id=%d, 错误: %s", user_id, str(e))
        raise
```

**配置方式推荐（项目级）**
|方式	|推荐程度	|说明|
|---|---|---|
|✅ Python 代码配置	|⭐⭐⭐⭐⭐	|最灵活，适合中小型项目|
|✅ YAML/JSON 配置文件	|⭐⭐⭐⭐☆|	适合大型项目，可热重载|
|❌ 硬编码在代码里	|⭐☆☆☆☆	|不可维护，不推荐|

> ✅ 推荐：用 logging.config.dictConfig() 加 YAML/JSON 配置文件。

---

## ✅ 四、关键优化点（性能+功能双优）

| 优化项 | 说明 |
|--------|------|
| **避免 `str.format()` 拼接** | 使用 `logger.info("msg", extra={})` 传参，避免字符串拼接开销 |
| **使用 `JSONFormatter` 结构化输出** | 便于 ELK、Prometheus+Loki 分析 |
| **日志文件按天/大小切割** | 使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler` |
| **审计日志独立输出** | 关键操作（登录、修改权限、删除数据）记录到 `audit.log`，便于审计 |
| **禁止 `logging.getLogger().debug(...)` 无条件输出** | 在生产环境，`DEBUG` 日志不输出，避免性能损耗 |

---

## ✅ 五、代码中如何使用（示例）

```python
# app.py
import logging

# 获取日志实例
logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")

def login_user(username, ip):
    try:
        # 模拟登录逻辑
        if not username:
            raise ValueError("Username is required")
        
        # 记录审计日志
        audit_logger.info(
            "User login attempt",
            extra={
                "event": "login_attempt",
                "username": username,
                "ip": ip,
                "success": True,
                "timestamp": logging.getLogger("app").info("timestamp")  # 实际用 time.time()
            }
        )
        logger.info(f"User {username} logged in from {ip}")

    except Exception as e:
        audit_logger.error(
            "Login failed",
            extra={
                "event": "login_failed",
                "username": username,
                "ip": ip,
                "error": str(e)
            }
        )
        logger.error(f"Login failed for {username}: {e}")
        raise
```

---

## ✅ 六、生产环境建议

| 项目 | 建议 |
|------|------|
| 日志级别 | `INFO` 为主，`DEBUG` 仅在开发/排查时开启 |
| 日志格式 | 使用 `JSON` 格式，便于机器解析 |
| 日志保留 | 保留 7~30 天，自动清理旧日志 |
| 审计日志 | **必须独立输出**，禁止与普通日志合并 |
| 日志聚合 | 推荐接入 **ELK Stack**、**Prometheus + Loki** 或 **Datadog**、**Splunk** |

---

## ✅ 七、Tips

- 使用 `extra` 传递上下文信息（如 `user_id`, `request_id`, `trace_id`），便于追踪。
- 在分布式系统中，使用 **`trace_id`** 统一关联日志。
- 使用 `contextvars`（Python 3.7+）在异步/协程中传递上下文。
- 用 `@log_call` 装饰器自动记录函数调用日志（可选）。

---

## ✅ 总结（一个“高性能+可审计+易排查”的日志系统）

| 特性 | 实现方式 |
|------|----------|
| 性能最优 | 使用 `dictConfig` + `JSONFormatter` + `RotatingFileHandler` |
| 信息完整 | 包含时间、模块、级别、函数、行号、`extra` 上下文 |
| 可审计 | 关键操作独立记录到 `audit.log`，包含 `event`, `user_id`, `ip`, `timestamp` |
| 易排查 | 使用 `trace_id` + `request_id` + `extra` 联动日志 |
| 环境适配 | `ENV=development` 时输出 `DEBUG` 日志，`production` 时仅 `INFO` 及以上 |

---

## 附录1：测试日志输出
```python
import logging

# 1. 创建一个 e2e_logger（子 logger）
e2e_logger = logging.getLogger("e2e")
e2e_logger.setLevel(logging.DEBUG)

# 2. 配置 e2e_logger 自己的 handler（控制台输出）
e2e_console_handler = logging.StreamHandler()
e2e_console_handler.setLevel(logging.DEBUG)
e2e_console_formatter = logging.Formatter(
    "%(name)s - %(levelname)s - %(message)s"
)
e2e_console_handler.setFormatter(e2e_console_formatter)
e2e_logger.addHandler(e2e_console_handler)

# 3. 设置 propagate = True，让日志传给 root_logger
e2e_logger.propagate = True

# 4. 配置 root_logger（它会接收 e2e_logger 传来的日志）
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 5. 给 root_logger 添加一个控制台 handler（它也会输出）
root_console_handler = logging.StreamHandler()
root_console_handler.setLevel(logging.DEBUG)
root_console_formatter = logging.Formatter(
    "ROOT - %(name)s - %(levelname)s - %(message)s"
)
root_console_handler.setFormatter(root_console_formatter)
root_logger.addHandler(root_console_handler)

# 6. 测试：打印一条日志
print("=== 开始测试日志输出 ===")
e2e_logger.info("这是一个 e2e 日志，应该被 e2e 和 root 都打印出来。")
```

## 附录2：常见错误&避坑指南
|错误	|说明	|如何避免|
|---|---|---|
|propagate = False 但又想传给 root|	日志“断了”，不会传给 root	|除非你明确不想传，否则设 propagate = True|
|多次调用 setup_logging()|	重复添加 handler → 日志重复打印|	用 if not root_logger.handlers: 判断|
|子 logger 有 handler，但 propagate = False|	只自己打印，不传 root|	按需设置，但要清楚意图|
|所有 loggers 都用 root_logger	|没有模块区分，日志乱成一团|	每个模块用独立的 logger 名|

## 附录3：项目级日志配置黄金法则
|法则|说明|
|---|---|
|1️⃣ 一个 root logger	|项目只配置一次，统一管理|
|2️⃣ 模块用子 logger	|logging.getLogger("app.module")|
|3️⃣ propagate = True（默认）|	让日志能传给 root|
|4️⃣ 只在启动时配置一次|	防止重复 handler|
|5️⃣ 日志格式统一	|便于搜索、分析、CI/CD 日志处理|

## 附录4：filter的配置示例
```python
import logging
from contextvars import ContextVar

# 全局上下文变量
_request_context = ContextVar("request_context", default={})

class SensitiveFilter(logging.Filter):
    def filter(self, record):
        # 1. 从上下文中获取请求信息
        ctx = _request_context.get({})
        record.user_id = ctx.get("user_id", "N/A")
        record.client_ip = ctx.get("client_ip", "N/A")
        record.request_id = ctx.get("request_id", "N/A")
        record.endpoint = ctx.get("endpoint", "unknown")

        # 2. 脱敏：只对 message 和 exc_info 脱敏
        if hasattr(record, "message") and isinstance(record.message, str):
            record.message = self.mask_sensitive(record.message)

        if hasattr(record, "exc_info") and record.exc_info:
            exc_str = str(record.exc_info[1])
            record.exc_info = (record.exc_info[0], self.mask_sensitive(exc_str), record.exc_info[2])

        return True

    def mask_sensitive(self, text: str) -> str:
        # 示例：替换密码、手机号等
        patterns = {
            "password": r'(password|pwd|pass|secret|token|key)[\s:]*["\']?([a-zA-Z0-9_\-+=%]*)["\']?',
            "phone": r'\b(\+?86)?1[3-9]\d{9}\b',
        }
        for pattern in patterns.values():
            text = re.sub(pattern, r'\1: ***', text, flags=re.IGNORECASE)
        return text

```

然后在 logging.yaml中注册
```yaml
filters:
  sensitive_filter:
    (): filters.sensitive_filter.SensitiveFilter

handlers:
  file:
    class: logging.FileHandler
    formatter: structured
    filters: [sensitive_filter]
    filename: logs/app.log
```

**附加建议：用loguru替代logging**
如果你追求更简洁、更现代的写法，可以考虑使用 loguru：
```python
from loguru import logger

logger.add("logs/app.log", rotation="100 MB")
logger.add(sys.stderr, level="INFO")

logger.info("Hello, World!")  # 一行搞定
```
> ✅ 它自动处理 propagate、重复 handler、格式等问题，开发效率提升 30%+。

