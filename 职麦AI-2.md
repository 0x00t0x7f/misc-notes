# 职麦 AI 系统 - DDD 架构设计文档

## 目录



1. [系统概述](#1-系统概述)

2. [领域分析与限界上下文](#2-领域分析与限界上下文)

3. [领域模型设计](#3-领域模型设计)

4. [分层架构设计](#4-分层架构设计)

5. [上下文映射与集成](#5-上下文映射与集成)

6. [系统架构视图](#6-系统架构视图)

7. [核心代码示例](#7-核心代码示例)

8. [部署架构](#8-部署架构)

9. [总结与展望](#9-总结与展望)

## 1. 系统概述

"职麦 AI" 是一个集成 AI 技术的求职面试辅助平台，旨在通过智能化工具帮助用户提升求职成功率。系统采用 React、FastAPI、SQLAlchemy、PostgreSQL、Redis、Nginx 及 AI 大模型等技术栈构建，提供模拟面试、简历诊断、职位搜索等全方位求职辅助功能。

系统核心特点：



* 基于 DDD (领域驱动设计) 思想构建，实现业务与技术的清晰分离

* 采用微服务架构理念，各功能模块松耦合设计

* 积分制商业模式，支持多种积分获取与消费场景

* 深度集成 AI 大模型，提供智能化求职辅助

## 2. 领域分析与限界上下文

根据系统功能模块，划分以下限界上下文：



1. **用户上下文 (User Context)**

* 用户注册、登录、认证授权

* 用户信息管理

* 权限控制

1. **积分上下文 (Point Context)**

* 积分账户管理

* 积分交易记录

* 积分充值 (支付宝集成)

1. **仪表盘上下文 (Dashboard Context)**

* 数据统计与展示

* 日历提醒与邮件通知

1. **模拟面试上下文 (Interview Simulation Context)**

* 视频面试模拟

* 面试配置管理

* 面试记录

1. **会议助手上下文 (Meeting Assistant Context)**

* 视频会议模拟

* 实时问答处理

* AI 回答生成

1. **职位搜索上下文 (Job Search Context)**

* 职位信息检索

* 爬虫数据接口适配

1. **简历处理上下文 (Resume Processing Context)**

* 简历上传与解析

* 简历诊断报告生成

* 面试押题生成

1. **推广上下文 (Promotion Context)**

* 推广链接生成

* 推广奖励管理

1. **反馈与支持上下文 (Feedback & Support Context)**

* 意见反馈收集

* 工单管理与处理

## 3. 领域模型设计

### 用户上下文



* **聚合根**：User

* **实体**：UserProfile, Role, Permission

* **值对象**：Email, PhoneNumber, Address

* **领域事件**：UserRegistered, UserProfileUpdated, PasswordChanged

### 积分上下文



* **聚合根**：PointAccount

* **实体**：PointTransaction, RechargeOrder

* **值对象**：Amount, TransactionType, PaymentInfo

* **领域事件**：PointsAdded, PointsDeducted, RechargeCompleted

### 仪表盘上下文



* **聚合根**：Dashboard

* **实体**：StatisticRecord, CalendarReminder

* **值对象**：TimeRange, StatisticDimension

* **领域事件**：ReminderCreated, ReminderTriggered

### 模拟面试上下文



* **聚合根**：InterviewSession

* **实体**：InterviewConfig, InterviewRecord

* **值对象**：JobInfo, CompanyInfo, InterviewSetting

* **领域事件**：InterviewStarted, InterviewCompleted

### 会议助手上下文



* **聚合根**：Meeting

* **实体**：MeetingRecord, ConversationTurn

* **值对象**：Transcript, Question, Answer

* **领域事件**：MeetingStarted, QuestionProcessed

### 职位搜索上下文



* **聚合根**：Job

* **实体**：JobCategory, Company

* **值对象**：JobDescription, Location, SalaryRange

* **领域事件**：JobSearched, JobFavorited

### 简历处理上下文



* **聚合根**：Resume

* **实体**：DiagnosticReport, GeneratedQuestion

* **值对象**：ResumeContent, WorkExperience, SkillSet

* **领域事件**：ResumeUploaded, ReportGenerated, QuestionsGenerated

### 推广上下文



* **聚合根**：Promotion

* **实体**：PromotionLink, RewardRecord

* **值对象**：PromotionCode, RewardRule

* **领域事件**：PromotionLinkCreated, RewardGranted

### 反馈与支持上下文



* **聚合根**：Feedback, SupportTicket

* **实体**：TicketReply

* **值对象**：FeedbackContent, TicketStatus, Priority

* **领域事件**：FeedbackSubmitted, TicketCreated, TicketResolved

## 4. 分层架构设计

每个限界上下文采用 DDD 经典分层架构：



1. **表现层 (Presentation Layer)**

* FastAPI 路由定义

* 请求 / 响应模型

* 认证授权处理

* 接口限流控制

1. **应用层 (Application Layer)**

* 应用服务 (协调领域对象完成业务用例)

* 命令和查询处理

* 事务管理

* 领域事件发布

1. **领域层 (Domain Layer)**

* 聚合根、实体、值对象

* 领域服务

* 领域事件

* 业务规则

1. **基础设施层 (Infrastructure Layer)**

* 数据持久化 (SQLAlchemy)

* 缓存实现 (Redis)

* 消息队列集成 (事件传递)

* 外部服务集成 (邮件、支付、AI 等)

## 5. 上下文映射与集成

限界上下文间采用以下集成方式：



1. **发布 - 订阅模式**：通过事件总线传递领域事件

2. **REST API**：用于需要即时响应的同步通信

3. **共享数据库视图**：谨慎使用，仅在必要时共享只读数据

主要上下文交互：



* 用户上下文 → 所有其他上下文：提供用户认证信息

* 积分上下文 ←→ 多个上下文：处理积分增减

* 推广上下文 → 用户上下文：新用户注册通知

* 推广上下文 → 积分上下文：推广奖励发放

## 6. 系统架构视图

### 限界上下文全景图



```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐

│   用户上下文    │◄────►│   积分上下文    │◄────►│  推广上下文     │

└────────┬────────┘      └────────┬────────┘      └─────────────────┘

&#x20;        │                        │

&#x20;        ▼                        ▼

┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐

│  仪表盘上下文   │      │ 模拟面试上下文  │◄────►│ 会议助手上下文  │

└─────────────────┘      └─────────────────┘      └─────────────────┘

&#x20;                                                     ▲

&#x20;        ┌─────────────────┐      ┌─────────────────┐ │

&#x20;        │  职位搜索上下文  │      │  简历处理上下文  │◄┘

&#x20;        └─────────────────┘      └────────┬────────┘

&#x20;                                          │

&#x20;                        ┌─────────────────┴─────────────────┐

&#x20;                        │           反馈与支持上下文          │

&#x20;                        └─────────────────────────────────────┘
```

### 分层架构图



```
┌─────────────────────────────────────────────────────────────┐

│                      表现层 (API)                           │

│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │

│  │ 路由    │  │ 请求验证 │  │ 认证    │  │ 响应格式化      │  │

│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘  │

├─────────────────────────────────────────────────────────────┤

│                      应用层                                 │

│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │

│  │ 用例服务 │  │ 命令处理 │  │ 查询处理 │  │ 事件发布        │  │

│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘  │

├─────────────────────────────────────────────────────────────┤

│                      领域层                                 │

│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │

│  │ 聚合根  │  │ 实体    │  │ 值对象  │  │ 领域事件        │  │

│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘  │

├─────────────────────────────────────────────────────────────┤

│                      基础设施层                             │

│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │

│  │ 数据库  │  │ 缓存    │  │ 消息队列 │  │ 外部服务集成    │  │

│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘  │

└─────────────────────────────────────────────────────────────┘
```

## 7. 核心代码示例

### 7.1 项目结构



```
jobmai\_ai/

├── api/                     # 表现层

│   ├── v1/

│   │   ├── endpoints/       # API端点

│   │   ├── schemas/         # 请求/响应模型

│   │   └── deps.py          # 依赖项(认证等)

├── application/             # 应用层

│   ├── commands/            # 命令

│   ├── queries/             # 查询

│   └── services/            # 应用服务

├── domain/                  # 领域层

│   ├── user/                # 用户上下文

│   ├── point/               # 积分上下文

│   ├── resume/              # 简历处理上下文

│   └── ...

├── infrastructure/          # 基础设施层

│   ├── db/                  # 数据库相关

│   ├── cache/               # 缓存

│   ├── event\_bus/           # 事件总线

│   └── services/            # 外部服务集成

└── main.py                  # 应用入口
```

### 7.2 用户上下文核心代码

**领域层 - 实体与值对象**



```
\# domain/user/entities.py

from dataclasses import dataclass

from datetime import datetime

from typing import Optional

from uuid import UUID, uuid4

from domain.core import Entity, ValueObject, AggregateRoot

@dataclass(frozen=True)

class Email(ValueObject):

&#x20;   address: str

&#x20;  &#x20;

&#x20;   def \_\_post\_init\_\_(self):

&#x20;       if "@" not in self.address:

&#x20;           raise ValueError("Invalid email address")

@dataclass

class UserProfile(Entity):

&#x20;   first\_name: str

&#x20;   last\_name: str

&#x20;   phone: Optional\[str] = None

&#x20;   profession: Optional\[str] = None

&#x20;  &#x20;

&#x20;   def update\_profile(self, \*\*kwargs):

&#x20;       for key, value in kwargs.items():

&#x20;           if hasattr(self, key):

&#x20;               setattr(self, key, value)

@dataclass

class User(AggregateRoot):

&#x20;   email: Email

&#x20;   hashed\_password: str

&#x20;   is\_active: bool = True

&#x20;   is\_verified: bool = False

&#x20;   profile: Optional\[UserProfile] = None

&#x20;   created\_at: datetime = datetime.now()

&#x20;   updated\_at: datetime = datetime.now()

&#x20;  &#x20;

&#x20;   def \_\_post\_init\_\_(self):

&#x20;       if not self.profile:

&#x20;           self.profile = UserProfile(first\_name="", last\_name="")

&#x20;  &#x20;

&#x20;   def verify(self):

&#x20;       self.is\_verified = True

&#x20;       self.updated\_at = datetime.now()

&#x20;       from domain.user.events import UserVerified

&#x20;       self.register\_event(UserVerified(user\_id=self.id))

&#x20;  &#x20;

&#x20;   def update\_password(self, new\_hashed\_password):

&#x20;       self.hashed\_password = new\_hashed\_password

&#x20;       self.updated\_at = datetime.now()

&#x20;       from domain.user.events import PasswordChanged

&#x20;       self.register\_event(PasswordChanged(user\_id=self.id))
```

**领域层 - 领域事件**



```
\# domain/user/events.py

from dataclasses import dataclass

from uuid import UUID

from domain.core import DomainEvent

@dataclass

class UserRegistered(DomainEvent):

&#x20;   user\_id: UUID

&#x20;   email: str

&#x20;   timestamp: float

&#x20;  &#x20;

@dataclass

class UserVerified(DomainEvent):

&#x20;   user\_id: UUID

&#x20;   timestamp: float

&#x20;  &#x20;

@dataclass

class PasswordChanged(DomainEvent):

&#x20;   user\_id: UUID

&#x20;   timestamp: float
```

**应用层 - 服务与命令**



```
\# application/commands/user\_commands.py

from dataclasses import dataclass

from uuid import UUID

from application.commands import Command

@dataclass

class RegisterUserCommand(Command):

&#x20;   email: str

&#x20;   password: str

&#x20;   first\_name: str

&#x20;   last\_name: str

@dataclass

class VerifyUserCommand(Command):

&#x20;   user\_id: UUID

&#x20;   verification\_code: str
```



```
\# application/services/user\_service.py

from datetime import datetime

from typing import Optional

from uuid import UUID

from passlib.context import CryptContext

from application.commands.user\_commands import RegisterUserCommand, VerifyUserCommand

from domain.user.entities import User, Email, UserProfile

from domain.user.events import UserRegistered

from domain.user.repositories import UserRepository

from infrastructure.services.email\_service import EmailService

pwd\_context = CryptContext(schemes=\["bcrypt"], deprecated="auto")

class UserService:

&#x20;   def \_\_init\_\_(

&#x20;       self,&#x20;

&#x20;       user\_repository: UserRepository,

&#x20;       email\_service: EmailService,

&#x20;       event\_bus

&#x20;   ):

&#x20;       self.user\_repository = user\_repository

&#x20;       self.email\_service = email\_service

&#x20;       self.event\_bus = event\_bus

&#x20;  &#x20;

&#x20;   async def register\_user(self, command: RegisterUserCommand) -> User:

&#x20;       # 检查邮箱是否已注册

&#x20;       existing\_user = await self.user\_repository.get\_by\_email(command.email)

&#x20;       if existing\_user:

&#x20;           raise ValueError("Email already registered")

&#x20;      &#x20;

&#x20;       # 创建用户

&#x20;       email = Email(address=command.email)

&#x20;       hashed\_password = pwd\_context.hash(command.password)

&#x20;       profile = UserProfile(

&#x20;           first\_name=command.first\_name,

&#x20;           last\_name=command.last\_name

&#x20;       )

&#x20;      &#x20;

&#x20;       user = User(

&#x20;           email=email,

&#x20;           hashed\_password=hashed\_password,

&#x20;           profile=profile

&#x20;       )

&#x20;      &#x20;

&#x20;       # 生成验证码并发送邮件

&#x20;       verification\_code = await self.\_generate\_verification\_code(user.id)

&#x20;       await self.email\_service.send\_verification\_email(

&#x20;           email=command.email,

&#x20;           code=verification\_code

&#x20;       )

&#x20;      &#x20;

&#x20;       # 保存用户并发布事件

&#x20;       await self.user\_repository.save(user)

&#x20;       await self.event\_bus.publish(UserRegistered(

&#x20;           user\_id=user.id,

&#x20;           email=command.email,

&#x20;           timestamp=datetime.now().timestamp()

&#x20;       ))

&#x20;      &#x20;

&#x20;       return user

&#x20;  &#x20;

&#x20;   async def verify\_user(self, command: VerifyUserCommand) -> bool:

&#x20;       # 验证用户和验证码

&#x20;       user = await self.user\_repository.get\_by\_id(command.user\_id)

&#x20;       if not user:

&#x20;           raise ValueError("User not found")

&#x20;          &#x20;

&#x20;       # 验证验证码逻辑...

&#x20;       is\_valid = await self.\_validate\_verification\_code(

&#x20;           user\_id=command.user\_id,

&#x20;           code=command.verification\_code

&#x20;       )

&#x20;      &#x20;

&#x20;       if is\_valid:

&#x20;           user.verify()

&#x20;           await self.user\_repository.save(user)

&#x20;           # 事件会由User实体内部注册并通过仓储发布

&#x20;      &#x20;

&#x20;       return is\_valid

&#x20;  &#x20;

&#x20;   async def \_generate\_verification\_code(self, user\_id: UUID) -> str:

&#x20;       # 生成并存储验证码逻辑

&#x20;       pass

&#x20;  &#x20;

&#x20;   async def \_validate\_verification\_code(self, user\_id: UUID, code: str) -> bool:

&#x20;       # 验证验证码逻辑

&#x20;       pass
```

**表现层 - API 端点**



```
\# api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel

from api.deps import get\_current\_user, get\_event\_bus

from application.commands.user\_commands import RegisterUserCommand, VerifyUserCommand

from application.services.user\_service import UserService

from infrastructure.container import Container

from domain.user.entities import User

router = APIRouter()

class RegisterUserRequest(BaseModel):

&#x20;   email: str

&#x20;   password: str

&#x20;   first\_name: str

&#x20;   last\_name: str

class VerifyUserRequest(BaseModel):

&#x20;   verification\_code: str

@router.post("/register", response\_model=dict)

async def register\_user(

&#x20;   request: RegisterUserRequest,

&#x20;   container: Container = Depends(Container),

):

&#x20;   user\_service: UserService = container.user\_service()

&#x20;   try:

&#x20;       command = RegisterUserCommand(

&#x20;           email=request.email,

&#x20;           password=request.password,

&#x20;           first\_name=request.first\_name,

&#x20;           last\_name=request.last\_name

&#x20;       )

&#x20;       user = await user\_service.register\_user(command)

&#x20;       return {"user\_id": user.id, "message": "User registered, please verify your email"}

&#x20;   except ValueError as e:

&#x20;       raise HTTPException(status\_code=400, detail=str(e))

@router.post("/verify", response\_model=dict)

async def verify\_user(

&#x20;   request: VerifyUserRequest,

&#x20;   current\_user: User = Depends(get\_current\_user),

&#x20;   container: Container = Depends(Container),

):

&#x20;   user\_service: UserService = container.user\_service()

&#x20;   try:

&#x20;       command = VerifyUserCommand(

&#x20;           user\_id=current\_user.id,

&#x20;           verification\_code=request.verification\_code

&#x20;       )

&#x20;       result = await user\_service.verify\_user(command)

&#x20;       if result:

&#x20;           return {"message": "User verified successfully"}

&#x20;       return {"message": "Invalid verification code"}

&#x20;   except ValueError as e:

&#x20;       raise HTTPException(status\_code=400, detail=str(e))
```

### 7.3 积分上下文核心代码



```
\# domain/point/entities.py

from dataclasses import dataclass

from datetime import datetime

from enum import Enum

from uuid import UUID, uuid4

from domain.core import Entity, ValueObject, AggregateRoot

class TransactionType(str, Enum):

&#x20;   RECHARGE = "recharge"

&#x20;   CONSUMPTION = "consumption"

&#x20;   REWARD = "reward"

&#x20;   REFUND = "refund"

@dataclass(frozen=True)

class Amount(ValueObject):

&#x20;   value: int

&#x20;  &#x20;

&#x20;   def \_\_post\_init\_\_(self):

&#x20;       if self.value < 0:

&#x20;           raise ValueError("Amount cannot be negative")

@dataclass

class PointTransaction(Entity):

&#x20;   user\_id: UUID

&#x20;   amount: Amount

&#x20;   transaction\_type: TransactionType

&#x20;   description: str

&#x20;   reference\_id: Optional\[UUID] = None  # 关联的业务ID

&#x20;   created\_at: datetime = datetime.now()

@dataclass

class PointAccount(AggregateRoot):

&#x20;   user\_id: UUID

&#x20;   balance: int = 0

&#x20;   created\_at: datetime = datetime.now()

&#x20;   updated\_at: datetime = datetime.now()

&#x20;  &#x20;

&#x20;   def add\_points(self, amount: int, description: str, reference\_id: Optional\[UUID] = None) -> PointTransaction:

&#x20;       if amount <= 0:

&#x20;           raise ValueError("Amount must be positive for adding points")

&#x20;          &#x20;

&#x20;       amount\_obj = Amount(amount)

&#x20;       transaction = PointTransaction(

&#x20;           user\_id=self.user\_id,

&#x20;           amount=amount\_obj,

&#x20;           transaction\_type=TransactionType.REWARD,

&#x20;           description=description,

&#x20;           reference\_id=reference\_id

&#x20;       )

&#x20;      &#x20;

&#x20;       self.balance += amount

&#x20;       self.updated\_at = datetime.now()

&#x20;      &#x20;

&#x20;       from domain.point.events import PointsAdded

&#x20;       self.register\_event(PointsAdded(

&#x20;           user\_id=self.user\_id,

&#x20;           amount=amount,

&#x20;           transaction\_id=transaction.id

&#x20;       ))

&#x20;      &#x20;

&#x20;       return transaction

&#x20;  &#x20;

&#x20;   def deduct\_points(self, amount: int, description: str, reference\_id: Optional\[UUID] = None) -> PointTransaction:

&#x20;       if amount <= 0:

&#x20;           raise ValueError("Amount must be positive for deducting points")

&#x20;          &#x20;

&#x20;       if self.balance < amount:

&#x20;           raise ValueError("Insufficient points")

&#x20;          &#x20;

&#x20;       amount\_obj = Amount(amount)

&#x20;       transaction = PointTransaction(

&#x20;           user\_id=self.user\_id,

&#x20;           amount=amount\_obj,

&#x20;           transaction\_type=TransactionType.CONSUMPTION,

&#x20;           description=description,

&#x20;           reference\_id=reference\_id

&#x20;       )

&#x20;      &#x20;

&#x20;       self.balance -= amount

&#x20;       self.updated\_at = datetime.now()

&#x20;      &#x20;

&#x20;       from domain.point.events import PointsDeducted

&#x20;       self.register\_event(PointsDeducted(

&#x20;           user\_id=self.user\_id,

&#x20;           amount=amount,

&#x20;           transaction\_id=transaction.id,

&#x20;           remaining\_balance=self.balance

&#x20;       ))

&#x20;      &#x20;

&#x20;       return transaction
```

### 7.4 简历处理上下文代码示例



```
\# application/services/resume\_service.py

from uuid import UUID

from application.commands.resume\_commands import ProcessResumeCommand, GenerateInterviewQuestionsCommand

from domain.point.services import PointService

from domain.resume.entities import Resume, DiagnosticReport, GeneratedQuestion

from domain.resume.repositories import ResumeRepository

from infrastructure.services.ai\_service import AIService

from infrastructure.services.file\_service import FileService

class ResumeService:

&#x20;   def \_\_init\_\_(

&#x20;       self,

&#x20;       resume\_repository: ResumeRepository,

&#x20;       point\_service: PointService,

&#x20;       file\_service: FileService,

&#x20;       ai\_service: AIService,

&#x20;       event\_bus

&#x20;   ):

&#x20;       self.resume\_repository = resume\_repository

&#x20;       self.point\_service = point\_service

&#x20;       self.file\_service = file\_service

&#x20;       self.ai\_service = ai\_service

&#x20;       self.event\_bus = event\_bus

&#x20;  &#x20;

&#x20;   async def process\_resume(self, command: ProcessResumeCommand) -> DiagnosticReport:

&#x20;       # 检查并扣除积分

&#x20;       await self.point\_service.deduct\_points(

&#x20;           user\_id=command.user\_id,

&#x20;           amount=10,  # 假设诊断简历消耗10积分

&#x20;           description="Resume diagnostic service"

&#x20;       )

&#x20;      &#x20;

&#x20;       # 保存上传的简历文件

&#x20;       file\_path = await self.file\_service.save\_file(

&#x20;           file\_content=command.file\_content,

&#x20;           file\_name=command.file\_name,

&#x20;           user\_id=command.user\_id

&#x20;       )

&#x20;      &#x20;

&#x20;       # 解析简历内容

&#x20;       resume\_content = await self.file\_service.extract\_text\_from\_file(file\_path)

&#x20;      &#x20;

&#x20;       # 创建简历记录

&#x20;       resume = Resume(

&#x20;           user\_id=command.user\_id,

&#x20;           file\_path=file\_path,

&#x20;           content=resume\_content

&#x20;       )

&#x20;       await self.resume\_repository.save\_resume(resume)

&#x20;      &#x20;

&#x20;       # 调用AI生成诊断报告

&#x20;       ai\_prompt = self.\_build\_diagnostic\_prompt(resume\_content)

&#x20;       ai\_response = await self.ai\_service.generate\_response(ai\_prompt)

&#x20;      &#x20;

&#x20;       # 创建诊断报告

&#x20;       report = DiagnosticReport(

&#x20;           resume\_id=resume.id,

&#x20;           content=ai\_response,

&#x20;           generated\_at=datetime.now()

&#x20;       )

&#x20;       await self.resume\_repository.save\_report(report)

&#x20;      &#x20;

&#x20;       # 发布事件

&#x20;       from domain.resume.events import ResumeDiagnosed

&#x20;       await self.event\_bus.publish(ResumeDiagnosed(

&#x20;           user\_id=command.user\_id,

&#x20;           resume\_id=resume.id,

&#x20;           report\_id=report.id

&#x20;       ))

&#x20;      &#x20;

&#x20;       return report

&#x20;  &#x20;

&#x20;   async def generate\_interview\_questions(self, command: GenerateInterviewQuestionsCommand) -> list\[GeneratedQuestion]:

&#x20;       # 检查并扣除积分

&#x20;       await self.point\_service.deduct\_points(

&#x20;           user\_id=command.user\_id,

&#x20;           amount=15,  # 假设生成面试题消耗15积分

&#x20;           description="Interview question generation service"

&#x20;       )

&#x20;      &#x20;

&#x20;       # 获取简历

&#x20;       resume = await self.resume\_repository.get\_resume\_by\_id(command.resume\_id)

&#x20;       if not resume or resume.user\_id != command.user\_id:

&#x20;           raise ValueError("Resume not found or access denied")

&#x20;      &#x20;

&#x20;       # 调用AI生成面试题

&#x20;       ai\_prompt = self.\_build\_question\_generation\_prompt(resume.content)

&#x20;       ai\_response = await self.ai\_service.generate\_response(ai\_prompt)

&#x20;      &#x20;

&#x20;       # 解析并保存生成的问题

&#x20;       questions = self.\_parse\_questions(ai\_response, resume.id)

&#x20;       await self.resume\_repository.save\_questions(questions)

&#x20;      &#x20;

&#x20;       # 发布事件

&#x20;       from domain.resume.events import InterviewQuestionsGenerated

&#x20;       await self.event\_bus.publish(InterviewQuestionsGenerated(

&#x20;           user\_id=command.user\_id,

&#x20;           resume\_id=resume.id,

&#x20;           question\_count=len(questions)

&#x20;       ))

&#x20;      &#x20;

&#x20;       return questions

&#x20;  &#x20;

&#x20;   def \_build\_diagnostic\_prompt(self, resume\_content: str) -> str:

&#x20;       return f"""Please analyze the following resume and provide a detailed diagnostic report:

&#x20;       \- Highlight strengths and weaknesses

&#x20;       \- Suggest improvements for better job applications

&#x20;       \- Evaluate the clarity and effectiveness of the content

&#x20;      &#x20;

&#x20;       Resume content:

&#x20;       {resume\_content}

&#x20;       """

&#x20;  &#x20;

&#x20;   def \_build\_question\_generation\_prompt(self, resume\_content: str) -> str:

&#x20;       return f"""Based on the following resume, generate 10-15 interview questions that are relevant to the candidate's experience and skills:

&#x20;       \- Include both technical and behavioral questions

&#x20;       \- Tailor questions to the candidate's work history and skills

&#x20;       \- Vary the difficulty level

&#x20;      &#x20;

&#x20;       Resume content:

&#x20;       {resume\_content}

&#x20;       """

&#x20;  &#x20;

&#x20;   def \_parse\_questions(self, ai\_response: str, resume\_id: UUID) -> list\[GeneratedQuestion]:

&#x20;       # 解析AI响应并创建问题对象

&#x20;       questions = \[]

&#x20;       for line in ai\_response.split('\n'):

&#x20;           line = line.strip()

&#x20;           if line and (line.startswith('-') or line\[0].isdigit()):

&#x20;               question\_text = line.lstrip('- .0123456789').strip()

&#x20;               if question\_text:

&#x20;                   questions.append(GeneratedQuestion(

&#x20;                       resume\_id=resume\_id,

&#x20;                       question\_text=question\_text

&#x20;                   ))

&#x20;       return questions
```

## 8. 部署架构



```
┌─────────────────┐

│    客户端浏览器   │

└────────┬────────┘

&#x20;        │

&#x20;        ▼

┌─────────────────┐

│    Nginx 服务器  │  # 反向代理、静态资源服务、负载均衡

└────────┬────────┘

&#x20;        │

&#x20;        ▼

┌─────────────────┐

│   FastAPI 应用   │  # 后端API服务

└───────┬─────────┘

&#x20;        │

&#x20;        ├───┬───────┬───────┬────────┬────────┐

&#x20;        │   │       │       │        │        │

&#x20;        ▼   ▼       ▼       ▼        ▼        ▼

┌────────┐┌──────┐┌────────┐┌───────┐┌───────┐┌────────┐

│PostgreSQL│ Redis │ AI服务 │ 邮件服务 │ 文件存储 │ 支付宝API │

└────────┘└──────┘└────────┘└───────┘└───────┘└────────┘
```

## 9. 总结与展望

本设计文档基于 DDD 思想，为 "职麦 AI" 系统提供了全面的架构设计，主要特点包括：



1. 清晰的限界上下文划分，实现业务领域的分离与聚焦

2. 严格的分层架构，确保业务逻辑与技术实现的解耦

3. 基于领域事件的集成方式，实现上下文间的松耦合通信

4. 完整的积分体系设计，支持系统的商业模式

未来可以从以下方面进行扩展：



1. 引入 CQRS 模式，分离读写操作，优化系统性能

2. 实现更细粒度的微服务拆分，提高系统的可扩展性

3. 增强系统监控与日志分析能力，提升可维护性

4. 引入更多 AI 能力，如面试表现分析、简历自动优化等

通过本设计，"职麦 AI" 系统将具备良好的可扩展性、可维护性和业务适应性，能够支持未来的功能扩展和用户增长。

> （注：文档部分内容可能由 AI 生成）