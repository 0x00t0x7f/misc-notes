以下是一个 **FastAPI + RocketMQ + DDD** 项目**集成 Prometheus + Grafana 的完整监控方案**，涵盖：

- ✅ RocketMQ 内置指标暴露（通过 `PrometheusExporter`）
- ✅ Prometheus 采集配置
- ✅ Grafana 仪表盘导入与自定义
- ✅ 完整的 `docker-compose.yml` 集成配置
- ✅ 自动化指标采集与可视化

---

## 📌 一、RocketMQ 指标暴露（关键！）

RocketMQ 本身支持 Prometheus 指标导出（需使用 `rocketmq-prometheus-exporter`）。

### ✅ 步骤 1：在 RocketMQ Broker 中启用 Prometheus Exporter

修改 RocketMQ 的 `conf/broker.conf`：

```properties
# 启用 Prometheus Exporter
brokerClusterName = DefaultCluster
brokerName = broker-a
brokerId = 0
brokerRole = ASYNC_MASTER
flushDiskType = ASYNC_FLUSH

# Prometheus Exporter 配置
# 端口（默认 9898）
prometheusExporterPort=9898

# 可选：开启 PromQL 查询（用于 Grafana）
prometheusExporterEnable=true
```

> 💡 **注意**：`rocketmq-prometheus-exporter` 是 RocketMQ 5.0+ 的功能，如果你使用的是 4.x 版本，需升级或使用第三方工具（如 `rocketmq-exporter`）。

---

## 📌 二、Prometheus 采集配置（`prometheus.yml`）

创建文件：`monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'rocketmq-broker'
    static_configs:
      - targets: ['rocketmq-broker-0:9898']
    metrics_path: '/prometheus'

  - job_name: 'rocketmq-namesrv'
    static_configs:
      - targets: ['rocketmq-namesrv-0:9876']  # Namesrv 无原生 Exporter，需额外方案
    # 说明：Namesrv 不支持 Prometheus，需通过外部脚本或埋点
    # 建议：使用 `rocketmq-exporter` 或编写自定义导出脚本

  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['fastapi:8000']
    metrics_path: '/metrics'
    # 说明：FastAPI 应用需集成 `prometheus-fastapi` 或 `aioprometheus`
```

---

## 📌 三、FastAPI 集成 Prometheus（自动暴露 `/metrics`）

在你的 `app/main.py` 中集成 Prometheus：

### ✅ 步骤 1：安装依赖

```bash
poetry add prometheus-fastapi
```

### ✅ 步骤 2：在 `main.py` 中注册 Prometheus 中间件

```python
# app/main.py

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI + RocketMQ + DDD", version="1.0")

# 注册 Prometheus 指标
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_paths=["/metrics", "/health"],
)
instrumentator.instrument(app).expose(app, include_in_schema=False)

# 你的 API 路由...
@app.get("/health")
def health():
    return {"status": "ok"}
```

> ✅ 启动后访问：`http://localhost:8000/metrics`，即可看到 Prometheus 指标。

---

## 📌 四、Grafana 仪表盘配置（推荐使用官方模板）

### ✅ 步骤 1：导入 Grafana 仪表盘

1. 登录 Grafana（默认 `http://localhost:3000`，账号：`admin`，密码：`admin`）
2. 点击左侧菜单 **Dashboards > Import**
3. 输入以下 ID 导入模板：
   - **RocketMQ 官方仪表盘**：[5737](https://grafana.com/grafana/dashboards/5737)（适用于 RocketMQ 5.0+）
   - **Prometheus - FastAPI**：[18744](https://grafana.com/grafana/dashboards/18744)（推荐用于 FastAPI 应用监控）

### ✅ 步骤 2：配置数据源

1. 进入 **Configuration > Data Sources**
2. 添加 Prometheus 数据源：
   - URL: `http://prometheus:9090`
   - 保存并测试连接

---

## 📌 五、完整 `docker-compose.yml`（含所有组件）

```yaml
# docker-compose.yml

version: '3.8'

services:
  rocketmq-namesrv-0:
    image: apache/rocketmq:5.1.0
    container_name: rocketmq-namesrv-0
    ports:
      - "9876:9876"
    environment:
      - NAMESRV_ADDR=0.0.0.0:9876
    command: sh -c "sh mqnamesrv & sleep 5; sh mqbroker -n 127.0.0.1:9876 -p 9881 -e 127.0.0.1:9898"

  rocketmq-broker-0:
    image: apache/rocketmq:5.1.0
    container_name: rocketmq-broker-0
    ports:
      - "9881:9881"
      - "9898:9898"  # Prometheus Exporter 端口
    environment:
      - NAMESRV_ADDR=rocketmq-namesrv-0:9876
      - BROKER_ROLE=ASYNC_MASTER
    command: sh -c "sh mqbroker -n rocketmq-namesrv-0:9876 -p 9881 -e 127.0.0.1:9898 & sleep 5; echo 'Broker started'"

  prometheus:
    image: prom/prometheus:v2.50.0
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - rocketmq-broker-0
      - fastapi

  grafana:
    image: grafana/grafana-enterprise:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - ./monitoring/grafana/dashboards:/etc/grafana/dashboards
      - grafana-storage:/var/lib/grafana
    depends_on:
      - prometheus

  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi
    ports:
      - "8000:8000"
    depends_on:
      - rocketmq-broker-0
      - prometheus

volumes:
  grafana-storage:
```

---

## 📌 六、验证与使用

1. 启动所有服务：
   ```bash
   docker-compose up -d --build
   ```

2. 访问：
   - Prometheus：`http://localhost:9090`
   - Grafana：`http://localhost:3000`（登录 `admin/admin`）
   - FastAPI：`http://localhost:8000/docs`

3. 观察 Grafana 仪表盘：
   - RocketMQ Broker 的消息吞吐、延迟、队列积压等
   - FastAPI 的请求量、响应时间、错误率等

---

## ✅ 总结：这套监控方案为什么是“黄金标准”？

| 功能 | 是否支持 |
|------|------------|
| RocketMQ 指标自动暴露 | ✅（通过 `prometheusExporterPort`） |
| Prometheus 自动采集 | ✅（YAML 配置 + Docker Compose） |
| Grafana 可视化（含官方模板） | ✅（ID 5737 + 18744） |
| FastAPI 指标自动暴露 | ✅（`prometheus-fastapi`） |
| 支持生产级监控告警（可扩展） | ✅（可接入 Alertmanager） |
