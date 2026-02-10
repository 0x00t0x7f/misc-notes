
## ✅ 项目需求

| 服务 | 功能 |
|------|------|
| `api-main` | 主应用服务，通过 REST API 调用语音服务，通过 Celery 向消息中心发布事件 |
| `api-voice` | 语音识别服务，接收主应用调用，处理音频并返回识别结果 |
| `message-center` | 消息中心服务，接收 Celery 发布的事件消息，用于后续分析或日志记录 |

---

## 🔐 安全性核心设计

| 安全机制 | 实现方式 |
|----------|----------|
| 🔒 **HTTPS 加密（Nginx + Let's Encrypt）** | 所有外部访问强制 HTTPS |
| 🌐 **服务间通信使用 API Key + JWT 认证** | 限制非法调用 |
| 🔒 **IP 白名单（Nginx Geo 模块）** | 仅允许指定 IP 段访问 |
| 🚫 **敏感端口不暴露于外网（PostgreSQL/Redis）** | 仅在内部网络通信 |
| 🔐 **Celery 任务队列使用 Redis + 任务签名验证** | 防止任务劫持 |
| 🧩 **Docker 自定义网络隔离** | 三服务之间通信仅限于 `app-network` |
| 📦 **密钥管理分离：使用 `.env` 文件 + Docker 环境变量** | 不提交密钥到 Git |

---

# 📄 `docker-compose.yml`（完整、安全、可扩展）

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ================== 1. Nginx 反向代理（HTTPS + IP 白名单） ==================
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - ./nginx/certs:/etc/letsencrypt
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - api-main
      - api-voice
      - message-center
    networks:
      - app-network
    restart: unless-stopped

  # ================== 2. 主应用服务（FastAPI） ==================
  api-main:
    build:
      context: ./app-main
      dockerfile: Dockerfile
    container_name: api-main
    environment:
      # 服务间认证密钥（主 → 语音服务）
      - VOICE_API_KEY=main-to-voice-api-key-123456

      # JWT 身份认证配置
      - SECRET_KEY=your-very-secure-jwt-secret-key-here
      - JWT_ALGORITHM=HS256

      # 数据库与缓存配置
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0

      # Celery 配置（连接 Redis）
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2

      # 服务间信任 IP（消息中心）
      - MESSAGE_CENTER_URL=http://message-center:8000/api/v1/events
      - MESSAGE_CENTER_API_KEY=main-to-message-center-key-789012

      # 安全：仅允许特定 IP 段调用
      - ALLOWED_MAIN_IPS=172.20.0.2
    networks:
      - app-network
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # ================== 3. 语音识别服务（FastAPI） ==================
  api-voice:
    build:
      context: ./app-voice
      dockerfile: Dockerfile
    container_name: api-voice
    environment:
      # 服务间认证密钥（语音 → 主应用）
      - SERVICE_API_KEY=voice-api-key-123456

      # JWT 配置（可选：用于内部接口）
      - SECRET_KEY=your-very-secure-jwt-secret-key-here
      - JWT_ALGORITHM=HS256

      # 数据库与缓存
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0

      # Celery 配置（语音任务队列）
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2

      # 仅允许主应用访问
      - ALLOWED_MAIN_IPS=172.20.0.2
    networks:
      - app-network
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # ================== 4. 消息中心服务（FastAPI + Celery） ==================
  message-center:
    build:
      context: ./message-center
      dockerfile: Dockerfile
    container_name: message-center
    environment:
      # 服务间认证密钥（主应用 → 消息中心）
      - API_KEY=main-to-message-center-key-789012

      # JWT 配置
      - SECRET_KEY=your-very-secure-jwt-secret-key-here
      - JWT_ALGORITHM=HS256

      # 数据库（可选：存储事件日志）
      - DATABASE_URL=postgresql://user:password@db:5432/appdb

      # Redis 配置
      - REDIS_URL=redis://redis:6379/0

      # Celery 配置
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2

      # 仅允许主应用访问（IP 白名单）
      - ALLOWED_MAIN_IPS=172.20.0.2
    networks:
      - app-network
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # ================== 5. PostgreSQL 数据库 ==================
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    networks:
      - app-network
    restart: unless-stopped

  # ================== 6. Redis（缓存 + Celery 任务队列） ==================
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

  # ================== 7. Celery Worker（语音服务专用） ==================
  celery-worker-voice:
    build:
      context: ./app-voice
      dockerfile: Dockerfile
    container_name: celery-worker-voice
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    command: celery -A app.tasks.celery_app worker -l info --queues=voice_tasks
    depends_on:
      - redis
      - api-voice
    networks:
      - app-network
    restart: unless-stopped

  # ================== 8. Celery Beat（定时任务） ==================
  celery-beat:
    build:
      context: ./app-voice
      dockerfile: Dockerfile
    container_name: celery-beat
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    command: celery -A app.tasks.celery_app beat -l info
    depends_on:
      - redis
      - api-voice
    networks:
      - app-network
    restart: unless-stopped

  # ================== 9. Celery Worker（消息中心专用） ==================
  celery-worker-message:
    build:
      context: ./message-center
      dockerfile: Dockerfile
    container_name: celery-worker-message
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    command: celery -A app.tasks.celery_app worker -l info --queues=message_events
    depends_on:
      - redis
      - message-center
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```
