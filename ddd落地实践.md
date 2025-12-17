在学习ddd如何落地实践之前，先了解什么是限界上下文？

限界上下文是 DDD用于战略设计上提出的概念，用来确定语义所在的领域边界。  
限界就是 领域的边界， 上下文是 语义环境。 通过领域的限界上下文，可以在统一的领域边界内用统一的语言进行交流。  

其定义： 用来封装通用语言和领域对象，提供上下文环境，保证在领域内的一些术语、业务相关对象等（通用语言）有一个确切的含义，没有二义性。  
这个边界定义了模型的适用范围，使团队成员明确的知道什么应该在模型中实现，什么不应该在模型中实现。 比如 商品在销售阶段是商品，而在运输阶段是货物。同一个东西，由于业务领域不同，赋予这些术语不同的含义和职责边界，这个边界就是微服务设计的边界。领域边界就是通过限界上下文来定义的。

# DDD概念
## 统一语言和概念明确，同一个团队，同一种语言
DDD中最重要的是要明确概念。 像做语文题一样，深究每个名词的含义。

### 概念不明确的常见情况
+ 概念过大、宽泛、涵盖了多层含义
+ 概念在不同上下文含义不同
+ 相似名称混用，比如混用同义词，但实际意义是有差别的
+ 同一个概念，随意的使用多个名称

### 明确概念的建议
+ 概念是名词
+ 概念是符合行业标准的
+ 概念是有边界的，有典型案例
+ 概念是分上下文语境的
+ 同一个概念，只有一个名词标表示
+ 命名直接，不产生歧义

### 概念可能混用的举例——用户、客户、账户、租户的区别
```mermaid
graph TD

A[客户]
B[租户]
C[账户]
D[登录方式]
E[功能权限]
F[用户]
A-->|订购开通后拥有 1..N|B---->|N..N|C---->|1..N|D
B-->|拥有 N..N|E
F--->|注册开通后拥有 1..1|C
C--->|拥有授权 N..N|E
```

## 领域模型是技术无关的，是问题的核心
领域模型<——领域服务<——应用服务<——用户界面 （箭头指向依赖方向）
基础设施依赖  框架、DB、外部服务

## 建模的方式
理解领域——>明晰概念——>建立概念之间的关系
### 事件风暴
+ 命令
+ 实体
+ 事件
举例： 围绕商品； 商品（实体）、创建商品（命令）、商品已创建（事件）、上架商品（命令）、商品已上架（事件）

### 四色建模法
+ monent-interval
+ 角色
+ 人——事——物
+ 描述

### 用户故事地图
+ 角色： 如 上班族、父亲、工程师
+ 活动：活动分解
+ 任务：任务分解

### 建模==分析语言
张三去买房，中介让留个电话，有合适的房源了，会通知他过来看房

分析这个场景
+ 买房者：张三
+ 房产中介： 中介公司、中介员工
+ 电话： 联系方式
+ 工作机会
+ 看房：预约看房

中介公司——（1..*）——中介员工——（1..服务..*）——买房者——（1..预约..*）——>看房<——（*..产生..1）——房源
其实这个场景中还包含房主，房主也可以发布房源，也可以由中介录入房源。
中介和房主之间存在关联关系。

### 实体vs.值对象
先分析识别实体和值对象构建领域模型，再根据领域模型将其转为数据模型。

**实体**  
具有唯一标识（ID），且状态会随业务变化的对象。例如，订单上下文的 “订单”（有唯一订单 ID，状态会从【待支付】变为【已支付】）、用户上下文的 “用户”（有唯一用户 ID，信息会更新）。实体的核心是 “状态与行为的封装”—— 例如，订单实体中应包含 “取消订单” 的方法（判断当前状态是否可取消，若可取消则更新状态并触发退款事件），而非将 “取消逻辑” 放在订单服务的接口中

**值对象**  
无唯一标识，仅通过属性值判断相等性，且状态不可变的对象。例如，订单上下文的 “收货地址”（包含省、市、区、详细地址，只要属性值相同，就是同一个地址，无需 ID）、支付上下文的 “金额”（包含数值和货币类型，如 100 元、20 美元，不可修改，修改时需创建新的金额对象）。值对象的作用是简化实体设计 —— 若将收货地址的属性（省、市、区）直接放在订单实体中，会导致订单实体属性冗余，而用值对象封装后，订单实体只需关联一个 “收货地址” 值对象

比如：
将 【领域模型】用户（ID、姓名、年龄、性别、地址），其中地址引用 地址值对象（省、市、县、街道）
再将【领域模型】转为【数据模型】。 可以用一张数据库表示数据模型； 用户（ID、姓名、年龄、性别、省、市、县、街道），其中（省、市、县、街道）属于地址相关的属性。这部分属性也可以根据实际情况单独成表。

### 聚合和聚合根
+ 聚合 能让 实体和值对象协同工作，它是用来确保这些领域对象在实现共同的业务逻辑时，能保证数据一致性。
+ 聚合 就是由 业务和逻辑紧密关联的实体和值对象组合而成的。 聚合是数据修改和持久化的基本单元，每一个聚合对应一个仓储，实现数据的持久化。
+ 聚合 有一个聚合根和上下文边界，这个边界根据业务单一职责和高内聚原则，定义了聚合内部应该包含哪些实体和值对象，而聚合之间的边界是松耦合的。

**聚合根**
+ 如果把聚合比作组织，聚合根就是这个组织的负责人
+ 聚合根作为实体本身，拥有实体的属性和业务行为，实现自身的业务逻辑
+ 聚合根作为聚合的管理者，在聚合内部负责协调实体和值对象按照固定的业务规则协同完成共同的业务逻辑
+ 最后在聚合之间，它还是聚合对外的接口人，以聚合根ID关联的方式接受外部任务和请求，在上下文内实现聚合之间的业务协同。
+ 聚合之间通过聚合根ID关联引用，如果需要访问其他聚合的实体，就先访问聚合根，在导航到聚合内部实体，外部对象不能直接访问聚合内实体。

### 聚合设计的步骤、方法
+ 事件风暴找出实体和值对象（哪些属于实体、哪些属于值对象，先列出来）
+ 找出聚合根（归类、确认聚合根）
+ 找出聚合
+ 对象引用和依赖模型

### 领域服务
封装跨实体 / 值对象的业务逻辑，无法归属到单个实体或值对象。例如，订单上下文的 “计算订单总金额” 服务 —— 总金额 = 商品金额 + 运费 - 折扣，涉及 “订单项”（实体）、“运费规则”（值对象）、“折扣券”（值对象），需通过领域服务协调多个对象完成计算

### 领域事件
记录领域内发生的重要事件，用于实现跨领域 / 跨上下文的异步通信。也主要用于软件中各个组件、模块、子系统甚至第三方系统之间的数据同步与集成。
例如，订单上下文的 “订单支付成功事件”，支付成功后，订单上下文发布该事件，库存上下文订阅该事件并扣减库存，物流上下文订阅该事件并创建配送单。领域事件的核心价值是解耦跨领域依赖 —— 订单上下文无需直接调用库存和物流服务，只需发布事件，其他上下文按需订阅。
领域事件的命名一般约定是  XXX已经XXX的形式，实际建模时，通常先建立一个公共基类 DomainEvent，其他事件类继承自该基类。 如 OrderPaidEvent、UserCreatedEvent等。

```python
class DomainEvent:
    def __init__(self, type, status="CREATED"):
        self.event_id = gen_snow_fake_id()
        self.type = type  # 事件类型 DomainEventType
        self.status = status  # 事件状态  CREATED、PUBLISH_SUCCESS、PUBLISH_FAILED
        self.create_at = now()  # 事件发生时间
```

## 领域驱动设计（架构分层）
用户接口层——>应用层——>领域层——>基础设施层。
+ 接入层：只负责系统的输入和输出，只关心沟通协议，数据格式，而不关心数据内容、业务相关的数据校验，但无业务逻辑。
+ 应用层：只负责组织业务场景，编排业务，隔离场景对领域层的差异。关心处理完一个完整的业务，不关心具体内部业务逻辑。不关心请求从何处来、关心谁来、做什么、有没有权限做；此层可以包含简单查询逻辑，但核心业务逻辑必须下沉到领域层
+ 领域层：实现具体的业务逻辑、规则，为应用层提供无差别服务能力。业务在这里组装。仓储（资源库）接口在此层定义。不关心场景，关心模型完整性和业务规则。强一致性事务在领域层处理，领域层做业务规则校验，数据权限控制，跨上下文使用值对象做必要的数据冗余。
+ 基础设施层：仓储（资源库）实现层+PO持久化层。提供具体的技术实现，比如存储、消息传递、通知，基础设施对业务保持透明。基础设施的权限由配置到应用的凭证控制。 比如 数据库、对象存储的凭证，技术设施层不涉及用户的权限。
+ 最核心是领域层，承载领域知识（业务规则，业务逻辑）
+ 理想状态下，领域层不依赖任何层。持久化也不在领域层操作，具体实现为在领域层定义 repository接口，在基础设施层是袭警案，并在 应用层调用。

## 架构分层示例
<img width="351" height="793" alt="image" src="https://github.com/user-attachments/assets/90409c32-fa92-425e-84e4-2dac9e6d0bc4" />

## 服务调用
### 域内调用
领域内调用，随便调用。至于实现，可以由一个核心域的仓储实现层（第四层）去实现多个Repository接口。（比如这里A是核心域的实体名，B是支撑域、通用域等）

<img width="339" height="237" alt="image" src="https://github.com/user-attachments/assets/4e79519d-db5b-49f0-a452-8d4587cd64c6" />

### 跨域调用
+ 同上下文跨域：ACL层->Adapter适配器层→调用其它域的repository。--->不得已才使用，不推荐使用。
  - 使用领域事件 eventbus来做解耦（推荐）
  - 考虑是否有可能合并为一个领域.

+ 跨上下文（肯定跨域）：ACL层->Adapter适配器层->feign调用
<img width="561" height="514" alt="image" src="https://github.com/user-attachments/assets/31db6e15-a6fd-44bf-8aed-fc35d57b1a99" />

## 包结构示例
<img width="433" height="325" alt="image" src="https://github.com/user-attachments/assets/db2721db-2637-4ba6-b8d8-9de159e9e94e" />

## 防腐层&依赖倒置

# DDD在Django项目中的实践
在ddd落地django项目前，先了解下分层设计模式。常见的主要有两种分层设计模式（MVT）和（MVC），django采用的是MVT模式，也就是 Model、View、Template，但其实在如今前后端分离项目中，我们很少用到django的template，我们只用到了MV，那T去哪了？
T就是前端的vue、react、等前端框架，前后端通过api接口交互。 那C（控制器）是什么？C就是Django框架本身， 它通过配置的路由将请求分发给匹配的视图处理。
```
@startuml
package "Django框架" {
    component [路由]  as Router
    [视图] as View
    [模板] as Template
    [模型] as Model
    [Django中间件] as MiddleWare
}

'cloud 服务器 as Server
'actor 用户 as User
'component 浏览器 as Browser
'User .-> Browser: 访问浏览器
'Browser .-> Server: http/https请求
'Server <-.-> "Django框架"

Router .-> MiddleWare: 路由匹配
MiddleWare .-> View: 中间件预处理
View -.-> Model: 业务逻辑、模型交互
Model -.-> View: 返回数据
View -.-> Template: 数据嵌入，视图函数将处理后的数据传递给模板
Template -.-> View: 模板引擎渲染成最终的HTML内容
View .-> MiddleWare: 中间件后处理
@enduml
```

## MVC分层模式
|名称|功能|
|---|---|
|Model|负责和数据相关的逻辑，数据库表操作相关|
|View|负责数据展示，将从model中或者用户处获取的数据进行展示，在循序MVC设计模式框架开发的web项目中，所有通过浏览器向用户展示的功能都由 视图模块实现|
|Controller|负责控制数据流向以及视图和模型之间的交互。 控制器会基于请求，由模型协助从数据库中获取数据，然后通过视图呈现|

## MVT分层模式
|名称|功能|
|---|---|
|Model|负责和数据相关的逻辑，数据库表操作相关|
|View|主要用于执行业务逻辑，从模型获取数据，将数据给到特定模板进行渲染后呈现给用户|
|Template|可视为表示层，主要是用户界面相关，也就是我们所说的前端|

如果拿MVC分层模式和MVT找对应关系，可以将MVC模式中的 控制器理解为 MVT模式中的视图， 将MVC模式中的视图理解为MVT模式中的模板。

## MVT和MVC的区别？
MVC和MVT两种模式的主要区别在于：在MVC模式中，开发者需要编写所有和控制器相关的代码，但是在MVT模式中，框架本身完成了控制器相关功能
在经典的MVC模式下，当用户通过浏览器发起一个请求后，将触发控制器中的一个功能调用，然后控制器要么告诉模型修改数据库并更新视图，要么基于模型返回一个更新后的视图。也就是说视图是由控制器和模型控制的
MVT模式的处理逻辑稍有不同：当一个用户发起一次HTTP请求后，相关的视图将通过模型执行一次查询，进而获取查询的结果，最后视图将结果数据填进模板后发送给用户

+ 职责划分
  - 在MVC中，Controller负责处理用户输入和业务逻辑，View负责展示数据
  - 在MTV中，View（视图）负责处理HTTP请求，协调Model和Template，而Template负责展示数据

+ 灵活性
  - MVC模式在桌面应用和Web应用中都有广泛应用
  - MTV模式特别适合Web开发，尤其是数据驱动的应用，因为Template可以更灵活地生成动态内容

<img width="810" height="480" alt="image" src="https://github.com/user-attachments/assets/b883c2bf-d0cf-4af0-86fc-2d754cb7cb9b" />


## DDD分层与Django分层模式对应关系（DDD视角）
|Level|DDD|Django|
|-----|-----|------|
|表现层|负责与用户交互，展示数据和处理用户输入|View+Temaplte共同构成DDD表现层、无业务逻辑|
|应用层|协调业务流程，处理用例，调用领域层服务；此层可以包含简单的查询逻辑，但核心复杂业务逻辑必须下沉到领域层|View+自定义Service类（处理复杂的业务逻辑，而不直接在视图中实现）；\n视图可以作为应用层的入口，调用服务类处理业务逻辑；应用服务类协调领域层的服务。|
|领域层|包含业务逻辑、实体、值对象、仓储接口定义等核心业务模型|Model（避免直接依赖django的orm）+自定义领域服务（在模型中或外部实现领域服务，处理核心业务逻辑）|
|基础设施层|处理与外部系统的交互，如数据库访问、消息队列、外部API调用等；仓储实现层+PO持久化层|数据库后端+管理器类+第三方库和API；django中的某些中间件也属于基础设施层|
|仓储模式|用于将数据库访问逻辑从领域层分离保持领域层的独立性|django可以通过 自定义仓储类+使用django的orm 实现仓储模式（确保领域层不直接依赖ORM）。见[示例代码](#ddd01)|
|领域事件|用于处理领域内的事件驱动逻辑|可以使用信号 signals 实现领域事件的处理|

**<span id='ddd01'>仓储模式示例代码</span>**   
```
# 仓储接口
class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id):
        pass

# 仓储实现
class DjangoUserRepository(UserRepository):
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
```

## DDD示例项目一：图书管理系统
故事：我需要一个图书管理系统，包含图书入库，借阅，归还，借阅临近日短信提醒等功能，请使用DDD分层架构思想实现这样的系统
我们使用 fastapi+sqlalchemy来实现这样一个系统
### 1、项目初始化
```
mkdir library_management_system
cd library_management_system
python -m venv venv
source venv/bin/activate  # 在Windows上使用 .\venv\Scripts\activate
pip install fastapi sqlalchemy python-dotenv
```
### 2、项目结构设计
根据DDD分层架构，设计项目的目录结构：
```
library_management_system/
├── app/
│   ├── domain/
│   │   ├── models.py  # 实体类
│   │   └── services.py  # 领域服务
│   ├── application/
│   │   └── services.py  # 应用服务
│   └── infrastructure/
│       ├── repositories/
│       │   └── book_repository.py
│       └── notification_service.py
├── presentation/
│   └── routes.py
├── main.py  # FastAPI应用入口
└── .env  # 环境变量配置
```
### 3、领域层实现
**在app/domain/models.py中定义实体类**：  
```python
from datetime import datetime

class Book:
    def __init__(self, book_id, title, author, isbn):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = "available"  # available, borrowed, maintenance

    def borrow(self):
        if self.status == "available":
            self.status = "borrowed"
            return True
        return False

    def return_book(self):
        if self.status == "borrowed":
            self.status = "available"
            return True
        return False

class BorrowRecord:
    def __init__(self, record_id, book, user, borrow_date):
        self.record_id = record_id
        self.book = book
        self.user = user
        self.borrow_date = borrow_date
        self.return_date = borrow_date + datetime.timedelta(days=14)  # 默认借期14天

    def days_remaining(self):
        today = datetime.datetime.today()
        delta = self.return_date - today
        return delta.days

    def is_overdue(self):
        today = datetime.datetime.today()
        return today > self.return_date
```
**在app/domain/services.py中定义领域服务**：  
```python
class BookManagementService:
    def __init__(self, book_repository):
        self.book_repository = book_repository

    def add_book(self, book):
        self.book_repository.save(book)

    def borrow_book(self, book_id, user):
        book = self.book_repository.find_by_id(book_id)
        if book.borrow():
            borrow_record = BorrowRecord(
                record_id=generate_id(),
                book=book,
                user=user,
                borrow_date=datetime.datetime.today()
            )
            self.book_repository.save_borrow_record(borrow_record)
            return True
        return False

    def return_book(self, book_id):
        book = self.book_repository.find_by_id(book_id)
        if book.return_book():
            self.book_repository.update_book(book)
            return True
        return False
```
### 4、应用层实现
**在app/application/services.py中定义应用服务**：  
```python
class BookApplicationService:
    def __init__(self, book_management_service, notification_service):
        self.book_management_service = book_management_service
        self.notification_service = notification_service

    def add_book(self, book):
        self.book_management_service.add_book(book)

    def borrow_book(self, book_id, user):
        success = self.book_management_service.borrow_book(book_id, user)
        if success:
            self.notification_service.send_borrow_confirmation(user, book_id)
        return success

    def return_book(self, book_id):
        success = self.book_management_service.return_book(book_id)
        if success:
            self.notification_service.send_return_confirmation(book_id)
        return success

    def check_overdue(self):
        records = self.book_management_service.get_all_borrow_records()
        for record in records:
            if record.is_overdue():
                self.notification_service.send_overdue_notification(record.user, record.book)
```
### 5、基础设施层实现
**在app/infrastructure/repositories/book_repository.py中定义书籍仓库**：  
```python
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BookDB(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)
    status = Column(String)

class BorrowRecordDB(Base):
    __tablename__ = 'borrow_records'
    record_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    user_id = Column(Integer)
    borrow_date = Column(Date)
    return_date = Column(Date)

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class BookRepository:
    def save(self, book):
        book_db = BookDB(
            book_id=book.book_id,
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            status=book.status
        )
        session.add(book_db)
        session.commit()

    def find_by_id(self, book_id):
        book_db = session.query(BookDB).filter_by(book_id=book_id).first()
        if not book_db:
            return None
        return Book(
            book_id=book_db.book_id,
            title=book_db.title,
            author=book_db.author,
            isbn=book_db.isbn,
            status=book_db.status
        )

    def save_borrow_record(self, borrow_record):
        borrow_record_db = BorrowRecordDB(
            record_id=borrow_record.record_id,
            book_id=borrow_record.book.book_id,
            user_id=borrow_record.user.user_id,
            borrow_date=borrow_record.borrow_date,
            return_date=borrow_record.return_date
        )
        session.add(borrow_record_db)
        session.commit()

    def get_all_borrow_records(self):
        records_db = session.query(BorrowRecordDB).all()
        records = []
        for record_db in records_db:
            book = self.find_by_id(record_db.book_id)
            user = User(user_id=record_db.user_id, name="", phone_number="")
            record = BorrowRecord(
                record_id=record_db.record_id,
                book=book,
                user=user,
                borrow_date=record_db.borrow_date
            )
            records.append(record)
        return records

    def update_book(self, book):
        book_db = session.query(BookDB).filter_by(book_id=book.book_id).first()
        if book_db:
            book_db.status = book.status
            session.commit()
```
**在app/infrastructure/notification_service.py中定义通知服务**：  
```python
class SMSNotificationService:
    def send_borrow_confirmation(self, user, book_id):
        message = f"您已成功借阅书籍，ID: {book_id}。请按时归还。"
        self.send_sms(user.phone_number, message)

    def send_return_confirmation(self, book_id):
        message = f"书籍ID: {book_id}已成功归还。感谢您的使用。"
        self.send_sms("library@system.com", message)

    def send_overdue_notification(self, user, book):
        message = f"您借阅的书籍《{book.title}》已逾期，请尽快归还。"
        self.send_sms(user.phone_number, message)

    def send_sms(self, recipient, message):
        # 调用短信API发送短信
        pass
```

### 6、表现层实现
**在presentation/routes.py中定义API路由**：  
```python
from fastapi import APIRouter, HTTPException
from app.domain.models import Book
from app.application.services import BookApplicationService

router = APIRouter()

@router.post("/books")
async def add_book(book: Book):
    try:
        BookApplicationService.add_book(book)
        return {"message": "Book added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/borrow")
async def borrow_book(book_id: int, user: User):
    try:
        success = BookApplicationService.borrow_book(book_id, user)
        if success:
            return {"message": "Book borrowed successfully"}
        else:
            return {"message": "Book is not available"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/return")
async def return_book(book_id: int):
    try:
        success = BookApplicationService.return_book(book_id)
        if success:
            return {"message": "Book returned successfully"}
        else:
            return {"message": "Return failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check-overdue")
async def check_overdue():
    try:
        BookApplicationService.check_overdue()
        return {"message": "Overdue check completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
### 7、FastAPI应用入口
**在main.py中定义FastAPI应用**：  
```python
from fastapi import FastAPI
from app.domain.services import BookManagementService
from app.infrastructure.repositories import BookRepository
from app.infrastructure.notification_service import SMSNotificationService
from app.application.services import BookApplicationService
from presentation.routes import router

app = FastAPI()

# 依赖注入
book_repository = BookRepository()
notification_service = SMSNotificationService()
book_management_service = BookManagementService(book_repository)
book_application_service = BookApplicationService(book_management_service, notification_service)

app.include_router(router)
```
### 8、环境变量配置
**在.env文件中配置数据库连接和其他环境变量**：  
```
DATABASE_URL = "sqlite:///library.db"
```

### 9、运行应用
```
uvicorn main:app --reload
```

### 10、解释
用DDD做项目的核心结论是：“从大到小、从抽象到具体” 的层级关联，核心逻辑是 “领域拆分子域，子域用限界上下文落地，上下文内用聚合封装数据行为，聚合根统一对外交互”
+ 领域：整个图书管理系统是一个大领域，包含了所有与图书管理相关的业务逻辑
+ 子域：如电商系统中（领域），订单管理、库存管理、用户管理是不同的子域
  - 图书管理子域（图书管理上下文）
  - 借阅管理子域（借阅管理上下文）
+ 限界上下文：限界上下文定义了子域的边界和语义。并帮助我们明确不同子域之间的关系和交互方式

## DDD示例项目二：电商系统
接着要做一个电子商务平台，用户可在平台购买东西

### 1、领域：最大的“业务范围容器”
+ 定义：定义：对应一个完整的业务领域，是所有相关业务的集合，范围最广、最抽象。
+ 举例：“电商系统” 就是一个领域，包含所有和 “网上买东西” 相关的业务（下单、付款、发货、商品管理等）

### 2、子域：领域的“功能拆分模块”
+ 定义： 把大领域按 “职责 + 重要性” 拆成的小模块，避免领域过于庞大
+ 分类 + 电商举例
  - 核心子域：业务核心价值（订单子域、商品子域、支付子域）
  - 支撑子域：辅助核心业务（物流子域，负责发货配送）
  - 通用子域：多个子域共用（用户认证子域，负责登录授权）
+ 关系： 一个领域包含多个子域， 子域之间是“协作关系”（比如订单子域要依赖商品子域查库存）

### 3、限界上下文： 子域的“边界” + 具体实现
+ 定义：给子域划清 “语义边界” 和 “技术边界”，边界内的术语、规则、对象有统一含义，外部不能直接干涉内部逻辑。
+ 电商举例：
  - 商品子域对应 “商品管理上下文”（里面的 “库存”“规格” 术语仅在此上下文内统一，比如 “库存” 指商品可售数量，和其他上下文的 “库存” 无关）
  - 订单子域对应 “订单管理上下文”（里面的 “下单”“取消订单” 规则只适用于订单业务）
+ 关系：1 个子域通常对应 1 个限界上下文（复杂子域可拆多个），限界上下文是子域的 “落地载体”。

### 4、聚合：限界上下文内的“最小业务单元”
+ 定义：把限界上下文内 “强关联的对象” 打包成一个整体，确保数据一致性（比如改一个对象必须同步改关联对象）。
+ 电商举例：
  - 商品管理上下文内，“商品”“商品规格”“库存” 强关联（改商品规格要同步调整库存，删商品要一起删规格和库存），打包成 “商品聚合”
  - 订单管理上下文内，“订单”“订单项”“收货地址” 强关联（删订单要一起删订单项和地址），打包成 “订单聚合”。
+ 关系：1 个限界上下文包含多个聚合，聚合之间是 “松耦合”（比如商品聚合和订单聚合通过 “商品 ID” 关联，不直接操作对方内部对象）

### 5、聚合根：聚合的“入口+管理者”
+ 定义：聚合内的 “核心对象”，外部只能通过它访问聚合内的其他对象，负责维护聚合的数据一致性。
+ 电商举例：
  - 商品聚合的聚合根是 “商品”：要扣减库存，必须通过 “商品。扣减库存 ()” 方法，不能直接改 “库存” 对象；
  - 订单聚合的聚合根是 “订单”：要添加订单项，必须通过 “订单。添加订单项 ()” 方法，不能直接创建订单项。
+ 关系：1 个聚合只有 1 个聚合根，聚合根是聚合对外的 “唯一接口”。

### 可视化关系图（电商场景）
用简单的层级图展示，直观看到从大到小的关联：
<img width="3796" height="1072" alt="image" src="https://github.com/user-attachments/assets/0159fd85-e6b5-434f-9da2-49796578913a" />

### 电商场景ER图详解
<img width="836" height="2291" alt="image" src="https://github.com/user-attachments/assets/125cbfe0-d8b6-40ed-9444-47ce0213ea6c" />

### 总结电商领域
把电商领域比作 “一个大商场”：
+ 领域 = 整个商场
+ 子域 = 商场里的 “服装区、食品区、收银台、保安部”
+ 限界上下文 = 每个区域的 “围栏 + 工作人员”（围栏划清边界，工作人员按区域规则做事）
+ 聚合 = 服装区里的 “一套穿搭（衣服 + 裤子 + 鞋子）”（强关联，买一套要一起拿）
+ 聚合根 = 这套穿搭的 “导购”（要试穿、购买只能找导购，不能直接拿衣服）

### 项目目录结构示例
```
application/  # 应用层
├── services/  # 应用服务，处理用户的请求并协调领域服务
│   ├── order_service.py
│   └── user_service.py
├── commands/  # 定义命令处理器， 处理用户命令请求
│   ├── create_order_command.py
│   └── update_product_command.py
└── queries/  # 定义查询处理器，处理用户查询请求
    ├── get_order_query.py
    └── list_products_query.py

core/  # 核心领域层
├── entities/  # 业务实体
│   ├── order.py
│   ├── product.py
│   └── user.py
├── value_objects/  # 值对象
│   ├── money.py
│   └── address.py
├── domain_services/  # 领域服务
│   ├── order_service.py
│   └── inventory_service.py
└── repositories/  # 仓库接口，用于数据持久化
    ├── order_repository.py
    └── product_repository.py
    
infrastructure/  # 基础设施层
├── database/
│   ├── models/  # ORM模型
│   │   ├── order_model.py
│   │   └── product_model.py
│   ├── repositories/  # 仓库的具体实现  如 xxxImpl
│   │   ├── order_repository_impl.py
│   │   └── product_repository_impl.py
│   └── db_config.py  # 数据库配置
├── logging/
│   └── logger.py
├── external_apis/  # 外部API客户端，如支付网关、通知服务
│   ├── payment_gateway.py
│   └── notification_service.py
└── cache/  # 缓存实现
    └── redis_cache.py

docs/
├── architecture.md
├── domain_model.md
└── api_reference.md

# .env
DB_NAME=my_project
DB_USER=root
DB_PASSWORD=secret
```

## DDD示例项目三：简历解析工具

### 项目目标
1. 用户注册（邮箱 + 验证码）
2. 上传简历（PDF/Word）
3. 后台异步解析简历内容（如姓名、电话、工作经历等）
4. 用户可刷新查看解析结果
5. 用户注册成功发送时间异步发送欢迎邮件

### DDD分层架构涉及（六边形架构）
```
+-------------------------+
|         API Layer     | ← FastAPI 路由 + Pydantic
+-------------------------+
            ↓
+-------------------------+
|       Application Layer | ← 应用服务（Use Case）
+-------------------------+
            ↓
+-------------------------+
|      Domain Layer     | ← 核心领域模型 + 领域服务
+-------------------------+
            ↓
+-------------------------+
|   Infrastructure Layer | ← 数据库、消息队列、邮件服务
+-------------------------+
```

### 技术栈
+ FastAPI：异步 Web 框架，支持 OpenAPI/Swagger
+ Pydantic：数据校验与序列化
+ SQLModel / SQLAlchemy：ORM（用于存储用户、简历元数据）
+ RabbitMQ 或 Redis：异步任务队列（解析简历）
+ Celery：分布式任务处理（可选）
+ Nodemailer / SendGrid / SMTP：发送邮件验证码
+ PDFMiner / docx2txt / PyPDF2：简历文件解析
+ Redis：缓存解析结果、验证码（临时）

### 项目目录结构
```
resume-parser/
├── main.py                          # FastAPI 入口
├── config.py                        # 配置类（数据库、邮件、Redis等）
│
├── domain/
│   ├── entities/                  # 领域实体
│   │   ├── user.py
│   │   ├── resume.py
│   │   └── parsed_resume.py
│   │
│   ├── value_objects/           # 值对象（不可变）
│   │   ├── email.py
│   │   ├── phone.py
│   │   └── verification_code.py
│   │
│   ├── repositories/              # 领域仓库接口
│   │   ├── user_repository.py
│   │   ├── resume_repository.py
│   │   └── parsed_resume_repository.py
│   │
│   ├── services/                  # 领域服务（业务逻辑）
│   │   ├── user_service.py
│   │   ├── resume_parser_service.py
│   │   └── verification_service.py
│   │
│   └── events.py                   # 领域事件（如：ResumeParsedEvent）
│
├── application/
│   ├── use_cases/                 # 应用服务（Use Case）
│   │   ├── register_user_use_case.py
│   │   ├── upload_resume_use_case.py
│   │   ├── get_parsed_resume_use_case.py
│   │   └── verify_email_use_case.py
│   │
│   └── dtos/                        # 数据传输对象（DTO）
│       ├── user_dto.py
│       ├── resume_dto.py
│       └── parsed_resume_dto.py
│
├── infrastructure/
│   ├── database/                    # 数据库连接
│   │   ├── session.py
│   │   └── models.py
│   │
│   ├── messaging/                   # 消息队列（RabbitMQ/Redis）
│   |   |__ event_publisher.py       # 发布事件
│   |   |__ event_handler.py         # 处理事件（Celery 任务）
│   |   |__ __init__.py
│   │   ├── task_queue.py
│   │   └── publish_parsed_event.py
│   │
│   ├── email/                         # 发送邮件验证码
│   │   ├── email_service.py
│   │   └── templates/
│   │       └── verification.html
│   │
│   ├── file_storage/                # 文件存储（本地 / MinIO / S3）
│   │   └── file_service.py
│   │
│   └── parsers/                       # 简历解析器
│       ├── pdf_parser.py
│       ├── docx_parser.py
│       └── resume_parser.py
│
├── api/
│   ├── routes/
│   │   ├── auth.py                # /auth/register, /auth/verify
│   │   ├── resume.py              # /resume/upload, /resume/result
│   │   └── health.py              # /health
│   │
│   └── dependencies.py            # 依赖注入（如 DB Session）
│
└── tests/
    ├── unit/
    └── integration/
```

### 核心功能实现（代码片段）
**用户实体（domain/entities/user.py）**  
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from domain.value_objects.email import Email
from domain.value_objects.verification_code import VerificationCode

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**定义领域事件（domain/events.py）**  
```python
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DomainEvent(BaseModel):
    event_id: str
    occurred_at: datetime
    event_type: str

class UserRegisteredEvent(DomainEvent):
    email: str
    user_id: int
    event_type: str = "UserRegisteredEvent"
```

**领域服务中发布事件（domain/services/user_service.py）**  
```python
from domain.events import UserRegisteredEvent
from infrastructure.messaging import event_publisher  # 新增：事件发布器

class UserService:
    def __init__(self, user_repository, verification_service):
        self.user_repository = user_repository
        self.verification_service = verification_service

    async def create_unverified_user(self, email: str) -> User:
        user = User(email=email, is_verified=False)
        return await self.user_repository.save(user)

    async def send_verification_code(self, email: str) -> str:
        code = self.verification_service.generate_code()
        await self.verification_service.send_code(email, code)
        return code

    async def confirm_registration(self, email: str, code: str) -> bool:
        if not await self.verification_service.verify_code(email, code):
            return False

        user = await self.user_repository.find_by_email(email)
        user.is_verified = True
        await self.user_repository.update(user)

        # ✅ 发布领域事件：用户注册成功
        event = UserRegisteredEvent(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.utcnow(),
            email=email,
            user_id=user.id
        )
        await event_publisher.publish(event)

        return True
```

**注册用例（application/use_cases/register_user_use_case.py）**  
```
from domain.services.user_service import UserService
from application.dtos.user_dto import UserDTO
from application.dtos.verification_dto import VerificationDTO

class RegisterUserUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def execute(self, email: str) -> VerificationDTO:
        user = await self.user_service.create_unverified_user(email)
        code = await self.user_service.send_verification_code(user.email)
        return VerificationDTO(email=email, code=code)
```

**邮件验证码服务（infrastructure/email/email_service.py）**  
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

class EmailService:
    def send_verification_email(self, email: str, code: str):
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_SENDER
        msg['To'] = email
        msg['Subject'] = "【简历平台】邮箱验证码"

        body = f"""
        <h2>您好！</h2>
        <p>您的验证码是：<strong>{code}</strong></p>
        <p>请在5分钟内完成验证。</p>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_SENDER, email, msg.as_string())
```

**简历上传接口（api/routes/resume.py）**  
```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from application.use_cases.upload_resume_use_case import UploadResumeUseCase
from application.dtos.resume_dto import ResumeDTO

router = APIRouter()

@router.post("/upload", response_model=ResumeDTO)
async def upload_resume(file: UploadFile = File(...), use_case: UploadResumeUseCase = Depends()):
    try:
        resume_dto = await use_case.execute(file)
        return resume_dto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**异步解析简历（infrastructure/parsers/resume_parser.py）**  
```python
import pdfplumber
from docx import Document
from typing import Dict

class ResumeParser:
    def parse(self, file_path: str, file_extension: str) -> Dict:
        if file_extension == ".pdf":
            return self._parse_pdf(file_path)
        elif file_extension == ".docx":
            return self._parse_docx(file_path)
        else:
            raise ValueError("Unsupported file type")

    def _parse_pdf(self, file_path: str) -> Dict:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            # 简单关键词提取（实际应使用 NLP）
            return {
                "name": self._extract_name(text),
                "phone": self._extract_phone(text),
                "email": self._extract_email(text),
                "experience": self._extract_experience(text)
            }

    # 其他辅助方法...

# 使用 celery + redis 异步执行：
# tasks.py
from celery import Celery
from infrastructure.parsers.resume_parser import ResumeParser
from infrastructure.file_storage.file_service import FileService

app = Celery('resume_tasks', broker='redis://localhost:6379/0')

@app.task
def parse_resume_task(file_id: str, file_path: str):
    parser = ResumeParser()
    result = parser.parse(file_path, ".pdf")
    
    # 保存到数据库
    # ...
    return result
```

**事件发布器（infrastructure/messaging/event_publisher.py）**  
```python
from typing import List
from pydantic import BaseModel
import json
import uuid
from celery import Celery

# 使用 Celery 作为事件广播机制（可替换为 RabbitMQ/Kafka）
app = Celery('event_broker', broker='redis://localhost:6379/0')

class EventPublisher:
    async def publish(self, event: BaseModel):
        # 序列化事件
        event_json = event.model_dump_json()
        event_id = str(uuid.uuid4())

        # 异步发布到 Celery 任务队列
        app.send_task(
            name='handle_domain_event',
            args=[event_id, event_json],
            kwargs={}
        )

event_publisher = EventPublisher()
```

**事件处理器（infrastructure/messaging/event_handler.py）**  
```python
from celery import Celery
from infrastructure.email.email_service import EmailService
from domain.events import UserRegisteredEvent
import json

app = Celery('event_handlers', broker='redis://localhost:6379/0')

@app.task
def handle_domain_event(event_id: str, event_json: str):
    try:
        # 反序列化事件
        data = json.loads(event_json)
        event_type = data.get("event_type")

        if event_type == "UserRegisteredEvent":
            event = UserRegisteredEvent(**data)
            send_welcome_email(event.email, event.user_id)
        else:
            print(f"Unknown event type: {event_type}")
    except Exception as e:
        print(f"Error handling domain event: {e}")

def send_welcome_email(email: str, user_id: int):
    # 发送欢迎邮件
    email_service = EmailService()
    subject = "🎉 欢迎注册简历解析平台！"
    body = f"""
    <h2>亲爱的用户，您好！</h2>
    <p>您已成功注册简历解析平台，账号 ID：{user_id}</p>
    <p>现在可以上传简历，开始智能解析啦！</p>
    <p>祝您使用愉快！</p>
    """
    email_service.send_email(email, subject, body)
```

### API接口设计（Swagger UI 自动展示）
```
方法	路径	功能
POST	/auth/register	注册用户（邮箱）
POST	/auth/verify	验证邮箱验证码
POST	/resume/upload	上传简历（支持 PDF/DOCX）
GET	/resume/result/{resume_id}	获取解析结果（支持轮询）
```

### 流程图
用户注册流程：
1. 用户提交邮箱 → 注册接口
2. 生成验证码 → 发送至邮箱
3. 用户输入验证码 → 验证通过
4. ✅ 更新用户状态为已验证
5. ✅ 触发领域事件：UserRegisteredEvent
6. 🔄 事件被异步消费：处理函数 `handle_domain_event`
7. 🔔 异步发送欢迎邮件（无需阻塞主流程）

### 部署建议
+ 开发：本地运行 FastAPI + PostgreSQL + Redis + RabbitMQ
+ 生产：
  - 使用 Docker Compose 管理服务
  - Nginx 反向代理 + HTTPS
  - Celery worker 集群处理任务
  - 使用 SendGrid 或 AWS SES 发送邮件

### 补充：确保事件处理服务启动
在 main.py 或启动脚本中，确保 Celery worker 启动
```python
# 启动 Celery worker 监听事件
celery -A infrastructure.messaging.event_handler app worker -l info
```
### 总结
项目完整实践了 DDD 分层架构 与 FastAPI 框架 的结合，具备：
+ 清晰的领域边界：分层清晰（领域层、应用层、基础设施层）
+ 业务逻辑集中在领域层
+ 高内聚、低耦合的模块设计
  - 事件驱动解耦：注册逻辑与发邮件逻辑完全分离
+ 异步任务处理能力
  - 异步无阻塞：用户注册完成后立刻返回，不影响体验
+ 可扩展、易维护的结构
  - 可扩展性强：未来可增加“发送短信”、“通知管理员”等处理逻辑

# 相关资料
+ https://www.cnblogs.com/dennyzhangdd/p/14376904.html
+ https://www.cnblogs.com/davenkin/p/ddd-introduction.html
+ https://blog.csdn.net/fsfjdtpzus/article/details/144009232
+ https://www.cnblogs.com/letjs/articles/18790630
