# 职麦AI系统DDD核心上下文交互全景图

### 1. 简约全景图（Mermaid 可视化）



```mermaid
graph TD
    %% 1. 定义子域（大模块划分）
    subgraph 核心子域-用户域
        subgraph 用户上下文
            U_AGG[聚合根：User<br/>(用户实体)]
            U_EVT1[领域事件：UserRegisteredEvent<br/>(用户注册成功)]
            U_EVT2[领域事件：UserEmailVerifiedEvent<br/>(邮箱验证成功)]
        end
    end

    subgraph 核心子域-积分域
        subgraph 积分上下文
            P_AGG[聚合根：PointsAccount<br/>(积分账户)]
            P_EVT[领域事件：PointsDeductedEvent<br/>(积分扣减成功)]
            P_CMD[命令：DeductPointsCmd<br/>(扣减积分指令)]
        end
    end

    subgraph 核心子域-面试服务域
        subgraph 模拟面试上下文
            I_AGG[聚合根：InterviewSession<br/>(面试会话)]
            I_EVT[领域事件：InterviewCreatedEvent<br/>(面试会话创建)]
        end
    end

    subgraph 通用子域-通知域
        subgraph 通知上下文
            N_AGG[聚合根：Notification<br/>(通知记录)]
            N_SVC[领域服务：EmailNotificationSvc<br/>(邮件通知服务)]
        end
    end

    %% 2. 交互链路（消息传递+事件触发）
    %% 链路1：用户注册 → 自动创建积分账户
    U_AGG -- "注册成功 → 发布" --> U_EVT1
    U_EVT1 -- "消息队列传递（如RabbitMQ）→ 监听" --> P_AGG
    P_AGG -- "接收事件 → 执行" --> P_CMD1[命令：CreatePointsAccountCmd<br/>(创建积分账户)]

    %% 链路2：用户发起模拟面试 → 扣减积分
    I_AGG -- "用户发起面试 → 调用积分接口" --> P_CMD
    P_CMD -- "执行扣减 → 发布" --> P_EVT
    P_EVT -- "消息传递 → 监听" --> I_AGG
    I_AGG -- "积分扣减成功 → 发布" --> I_EVT

    %% 链路3：积分变动/面试创建 → 发送通知
    P_EVT -- "消息传递 → 触发" --> N_SVC
    I_EVT -- "消息传递 → 触发" --> N_SVC
    N_SVC -- "生成通知记录" --> N_AGG
    N_SVC -- "发送邮件" --> USER[终端用户]

    %% 3. 补充说明（简化标注）
    style U_AGG fill:#e6f7ff,stroke:#1890ff
    style P_AGG fill:#f0f9ff,stroke:#40a9ff
    style I_AGG fill:#fff2e8,stroke:#fa8c16
    style N_AGG fill:#f6ffed,stroke:#52c41a
    style U_EVT1 fill:#fff0f0,stroke:#f5222d,stroke-dasharray:5,5
    style P_EVT fill:#fff0f0,stroke:#f5222d,stroke-dasharray:5,5
    style I_EVT fill:#fff0f0,stroke:#f5222d,stroke-dasharray:5,5
```

### 2. 全景图核心说明

#### （1）核心元素定义



| 层级    | 元素                    | 说明                                                 |
| ----- | --------------------- | -------------------------------------------------- |
| 子域    | 用户域 / 积分域 / 面试服务域     | 系统核心业务域，承载用户管理、积分流转、AI 面试核心能力                      |
| 限界上下文 | 用户上下文 / 积分上下文         | 业务边界清晰的独立模块，内部逻辑自治，对外通过事件 / 命令交互                   |
| 聚合根   | User/PointsAccount 等  | 上下文内的核心实体，聚合其他关联对象（如 User 聚合 UserProfile），统一对外暴露接口 |
| 领域事件  | UserRegisteredEvent 等 | 上下文内状态变更的 “消息载体”，用于跨上下文通信（松耦合）                     |
| 命令    | DeductPointsCmd 等     | 上下文间的 “主动请求”（同步调用），用于明确的业务操作（如扣积分）                 |

#### （2）关键交互流程（3 条核心链路）



1. **用户注册→自动开积分账户**

   用户完成注册（User 聚合根状态变更）→ 发布`UserRegisteredEvent`→ 积分上下文监听事件→ 执行`CreatePointsAccountCmd`→ 为用户创建 PointsAccount 聚合根（初始积分可设为 0 或赠送新手积分）。

2. **发起模拟面试→积分扣减**

   用户创建面试会话（InterviewSession 聚合根初始化）→ 模拟面试上下文向积分上下文发送`DeductPointsCmd`（如扣 20 积分）→ 积分上下文扣减成功→ 发布`PointsDeductedEvent`→ 模拟面试上下文监听事件，确认积分足够后创建面试会话（`InterviewCreatedEvent`）。

3. **状态变更→自动通知用户**

   积分扣减成功（`PointsDeductedEvent`）/ 面试会话创建（`InterviewCreatedEvent`）→ 通知上下文监听事件→ 调用`EmailNotificationSvc`→ 生成 Notification 聚合根记录→ 向用户发送 “积分扣减提醒”“面试开始通知” 邮件。

> （注：文档部分内容可能由 AI 生成）
