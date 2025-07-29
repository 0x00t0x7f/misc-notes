## 创建型模式
怎么创建对象，将对象的创建与使用分离；降低系统的耦合度
### 类模式
- 工厂模式（分为 简单工厂模式、工厂方法模式） 其中简单工厂模式不属于GOF设计模式之一，因为它的缺点是增加新产品时会违背”开闭原则“
### 对象模式
- 单例
- 原型
- 抽象工厂
- 建造者

## 结构型模式
将类或对象按某种布局组成更复杂庞大的结构

### 类模式
- （类）适配器
### 对象模式
- （对象）适配器
- 代理
- 桥接
- 装饰
- 外观
- 享元
- 组合

## 行为型模式
类或对象之间怎样相互协作共同完成单个对象无法单独完成的任务，以及怎样分配职责

### 类模式
- 模板方法
- 解释器
### 对象模式
- 策略
- 命令
- 责任链
- 状态
- 观察者
- 中介者
- 迭代器
- 访问者
- 备忘录

## 设计模式示例
### 简单工厂模式
```
class Product:
    def operate(self):
        pass


class ProductA(Product):
    def operate(self):
        return "product a"


class ProductB(Product):
    def operate(self):
        return "product b"


class SimpleFactory:

    @staticmethod
    def create_product(product_name):
        if pruduct_name == "a":
            return ProductA()
        elif product_name == "b":
            return ProductB()
        else:
            raise ValueError


if __name__ == "__main__":
    product_a = SimpleFactory.create_product("ProductA")
    product_b = SimpleFactory.create_product("ProductB")

    for product in [product_a, product_b, ...]  # 产品流水线
        product.operate()

    # 如果需要增加新的产品线，不得不修改简单工厂类的代码，破坏了SRP和OCP原则
```

### 工厂方法模式
将对象的创建过程委托给子类的方式
#### 工厂方法的基本原理
+ 定义一个接口或者抽象类表示要创建的对象
+ 创建一个或多个具体的子类 实现工厂接口并实现工厂方法来创建对象
+ 创建一个工厂类 该类包含一个工厂方法 该方法根据需要创建对象并返回该对象

```
from abc import ABC, abstractmethod

# 定义抽象产品类
class Product(ABC):

    @abstractmethod
    def operate(self):
        pass


class ProductA(Product):

    def operate(self):
        print("ProductA operate")


class ProductB(Product):

    def operate(self):
        print("ProductB operate")


# 定义抽象工厂类
class Factory(ABC):

    @abstractmethod
    def factory_method(self) -> Product:
        pass

    def operation(self):
        product = self.factory_method()
        product.operate()


# 定义具体工厂类
class FactoryA(Factory):

    def factory_method(self) -> Product:
        return ProductA()


class FactoryB(Factory):

    def factory_method(self) -> Product:
        return ProductB()    


if __name__ == "__main__":
    factory_a = FactoryA()
    factory_b = FactoryB()

    for factory in [factory_a, factory_b]:  # 不同工厂生产不同的产品，将产品的生产与工厂解耦  每个工厂生产一种产品
        factory.operate()
```
### 抽象工厂模式
比如我们要设计一个GUI软件，这个软件有一个文本框和按钮，并需要兼容不同的操作系统，目前需要兼容 mac 和 windows 系统
```
class TextBox(ABC):

    @abstractmethod
    def paint(self):
        pass


class Button(ABC):

    @abstractmethod
    def paint(self):
        pass


# 具体的控件类
class WindowsTextBox(TextBox):

    def paint(self):
        print("painting a windows stype textbox")


class WindowsButton(Button):

    def paint(self):
        print("painting a windows style button")


class MacTextBox(TextBox):

    def paint(self):
        print("painting a mac os style textbox")


class MacButton(Button):

    def paint(self):
        print("painting a mac os style button")


# 定义抽象工厂类
class GUIFactory(ABC):

    @abstractmethod
    def create_textbox(self) -> TextBox:
        pass

    @abstractmethod
    def create_button(self) -> Button:
        pass


class WindowsFactory(GUIFactory):

    def create_textbox(self) -> TextBox:
        return WindowsTextBox()

    def create_button(self) -> Button:
        return WindowsButton()


class MacFactory(GUIFactory):

    def create_textbox(self) -> TextBox:
        return MacTextBox()

    def create_button(self) -> Button:
        return MacButton()


def create_gui(factory: GUIFactory):
    textbox = factory.create_textbox()
    button = factory.create_button()
    return textbox, button


windows_gui = create_gui(WindowsFactory())
```
### 建造者模式
将复杂对象的构建和它的表示分离 使得同样的构建过程可以创建不同的表示
按照特定顺序组装一个复杂的对象，将对象的构造过程分解为多个步骤，每个步骤由一个具体的构造者完成，客户端可以根据需要使用不同的构造者构建不同对象，不用知道构造过程的细节

#### 建造者模式四个主要角色
+ 产品（表示要构建的复杂对象）
+ 建造者（builder）: 定义创建产品的抽象接口，包含构造产品各个零件的方法
+ 具体建造者类：实现 builder接口，完成复杂对象各个零件的实际构造工作
+ 指挥者（director）：负责管理（builder），按照顺序调用 builder中方法按步骤构建产品

#### 建造者模式应用场景
+ 构建复杂对象， 且构建过程中步骤固定但顺序不同活部分步骤凯旋，适合用建造者模式
+ 隔离复杂对象的创建和使用，使用建造者模式让用户专注于使用对象，不需要关心对象的构造过程
+ 多种配置对象，当一个类实例有不同的配置方式，建造者模式可以帮助简化对象的创建

```
class Doll:
    def __init__(self):
        self.name = None
        # 其他属性省略..

    def singsong(self, lyrics):
        print(f"我是, {self.name}, 唱歌给你听,~ {lyrics}..")


class DollBuilder(ABC):

    @abstractmethod
    def set_name(self, name):
        pass


class RagDollBuilder(DollBuilder):

    def __init__(self):
        self.doll = Doll()

    def set_name(self, name):
        self.doll.name = name


class Director:

    def __init__(self, builder):
        self.builder = builder

    def build_labubu_ragdoll_doll(self):
        self.builder.set_name("拉布布")
        return self.builder.doll


doll_builder = RagDollBuilder()
director = Director(doll_builder)
labubu_doll = director.build_labubu_ragdoll_doll()  # 创建一个拉布布的毛绒玩具对象
labubu_doll.singsong("拉布, 拉布拉布布, 我是最棒的拉布布..")
```
### 适配器模式
用于将一个类的接口转换为另一个类的接口 解决两个不兼容的接口之间的兼容问题 使得他们协同工作
#### 适配器模式的组件组成
+ 源接口（adaptee interface）: 是需要被适配的接口，通常由一个或多个具体类或接口表示
+ 适配器（adapter）： 实现目标接口的对象，并包装一个需要适配的对象，并实现目标接口来实现适配的效果
+ 目标接口（target interface）：客户端代码期望的接口， 通常由抽象类或接口表示
#### 适配器模式两种实现方式
+ 类适配器模式：通过继承实现适配器
+ 对象适配器模式：通过组合来实现适配器
```
# 源接口-需要被适配的类
class OLDInterface:

    def old_request(self):
        pass


# 目标接口-当前正在使用的类或客户端期望的接口
class TargetInterface:

    def request(self):
        pass


# 类适配器
class AdapterCls(OLDInterface, TargetInterface):

    def request(self):
        self.old_request()  # 调用旧式的old_request方法


# 对象适配器
class AdapterObj(TargetInterface):

    def __init__(self, old_instance):
        self._old_instance = old_instance

    def request(self):
        self._old_instance.old_request()  # 调用旧式的old_request方法


# 客户端代码
def client_request(target):
    target.request()


# 类适配器调用示例
adapter = AdapterCls()
client_request(adapter)

# 对象适配器调用示例
old_obj = OLDInterface()
adapter = AdapterObj(old_obj)
client_request(adapter)
```

### 桥接模式
原理是基于面向对象的多态特性 基于类的最小设计原则 使用封装、聚合和继承等行为将抽象部分和实现部分解耦（这里的实现部分并不是具体的实现类，而是一个具体实现类的接口，抽象类的操作都会委托给具体实现类执行） 使得它们可以独立变化互不影响 它们之间通过一个桥梁接口联系
#### 桥接模式实现步骤
+ 定义抽象类和实现类接口
+ 定义桥梁接口：包含了一个对实现类的引用 以及一些委托方法
+ 定义具体桥梁类：继承桥梁接口，实现了委托方法，将调用转发给实现类的方法
+ 实例化具体桥梁类 并将实现类对象作为参数传递给具体桥梁类的构造函数
+ 调用具体桥梁类的方法：桥梁类将委托给实现类的方法来完成具体的操作

#### 桥接模式的四种角色
+ 抽象类： 该类包含一个对实现类角色的引用， 抽象角色中的方法一般需要实现角色实现。
+ 修正对象：抽象类的具体实现类
+ 实现类：提供给抽象类使用，一般为接口或者抽象类
+ 实现类的具体实现

#### 桥接模式python示例
比如我们平时点外卖，平台给派单，骑实不用关心他送的是什么外卖，他只需要负责把外卖按时送到顾客手里就算完成了任务。 在这个例子中，有几个角色： 商家、外卖骑手、顾客。对于商家来说，并不关心哪个骑手配送他家的外卖，商家只需要打包好外卖，等骑手过来领取； 商家和顾客之间是通过外卖小哥间接接触的，那我们可以将这个逻辑关系抽象出来。 我们我们暂时只关注商家和骑手，不用关注顾客订餐的细节。

于是我们杜撰出一个超级大杂烩平台，且虚构出一个胡扯的故事..
##### 商家&外卖骑手的UML类图如下

```
# 实现类接口
class DeliveryMan(ABC):
    platform = None

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def send(self, food, customer):
        pass


class MeituanDeliveryMan(DeliveryMan):
    platform = "某团"

    def send(self, food, customer):
        print(f"\t[{self.platform}]-外卖骑手-({self.name})正在配送: (客户-{customer}) 点的 {food}.")


# 抽象类
class Business(ABC):
    """ 外卖商家-接口"""
    platform = None

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def delivery(self, food: str, deliveryman: DeliveryMan, customer: str):
        """ 商家只负责做饭"""
        pass


class MeituanBusiness(Business):
    """ 某团商家"""
    platform = "某团"

    def delivery(self, food: str, deliveryman: DeliveryMan,  customer: str):
        print(f"{self.platform}-商家[{self.name}] 委托:")
        deliveryman.send(food, customer)

if __name__ == "__main__":
    # 小马哥点了一杯奶茶  商家委托骑手（bridge）送外卖到顾客手里
    business1 = MeituanBusiness("霸王奶茶")
    delivery1 = MeituanDeliveryMan("张全蛋")
    business1.delivery("伯牙琴弦", delivery1, "小马哥")

某团-商家[霸王奶茶] 委托:
	[某团]-外卖骑手-(张全蛋)正在配送: (客户-小马哥) 点的 伯牙琴弦.
```
一个夏日的午后 小马哥在连线投资部的会议前在某团平台点了一杯奶茶
某团将这单派送了附近的骑手张全蛋

1h later..
张全蛋：（气喘吁吁） 马总，不好意思  路上有点堵，您的奶茶送慢了
小马哥：你这送奶茶的速度比我们TX开会还慢啊
张全蛋：（挠头）马总，真的不好意思，刚才有个大妈非要让我帮她修手机，我一时好心就耽误了点时间
小马哥：（无奈）行了，你这服务态度倒是不错，就是效率有点感人。这奶茶都凉了，我这人最讲究“趁热喝”，你这是让我喝“冷知识”啊
张全蛋：（尴尬）马总，我下次一定快点，保证让您喝到热乎的！

小马哥喝着奶茶突然冒出了一个大胆的想法.. 给战略合作伙伴JD的东哥拨通了电话..
小马哥：（拿起电话，语气兴奋）喂，老刘啊，你JD物流这么强，为什么不搞外卖？现在外卖市场这么火，你们完全有条件啊！你要是搞，我继续追加对JD的投资！
东子哥：（笑着接电话）老马啊，你这主意倒是不错，我这几天正在琢磨这件事呢，不过你得答应我一个条件——我要是搞外卖，不许点我们JD的奶茶哦！
小马哥：（愣了一下，随即大笑）哈哈哈，行啊，没问题！不过你JD搞外卖，我可就不点某团的外卖了，直接喝你JD的奶茶（笑）
东子哥：（瞬间黑脸）老马，你这样开涮我不合适吧，我JD搞外卖，你要是敢点奶茶，我就让你知道什么是“JD速度”！

2 month later.. 
用我们的桥接模式可以很方便的扩充了JD商家，招募了骑手，很快JD外卖平台上线了..
##### 商家&外卖骑手的UML类图如下

```
class JDBusiness(Business):
    """ JD商家"""
    platform = "JD"

    def delivery(self, food: str, deliveryman: DeliveryMan,  customer: str):
        print(f"{self.platform}-商家[{self.name}] 委托:")
        deliveryman.send(food, customer)


class JDDeliveryMan(DeliveryMan):
    platform = "JD"

    def send(self, food, customer):
        print(f"\t[{self.platform}]-外卖骑手-({self.name})正在配送: (客户-{customer}) 点的 {food}.")
```

小马哥：（坐在办公室，看着手机，坏笑）“老刘啊，你JD外卖今天第一天，之前某团的有点慢，我得亲自测一下JD的速度！
东子哥：对着新招募的骑手说，今天是我们JD外卖第一天，我要和兄弟们一起干！

```
# 于是小马哥在JD外卖平台偷偷的点了一杯奶茶，想尝尝JD的奶茶是什么味道..
business2 = MeituanBusiness("霸王奶茶")

# 没想到的是，今天的配送员其中就有东子哥，好巧不巧，小马哥这单子被系统随机分派给了东哥
delivery2 = MeituanDeliveryMan("东子哥")
business2.delivery("伯牙琴弦", delivery2, "小马哥")

JD-商家[霸王奶茶] 委托:
	[JD]-外卖骑手-(东子哥)正在配送: (客户-小马哥) 点的 伯牙琴弦.
```
15min later..
（叮咚一声，奶茶到了。小马哥开门，看到送奶茶的是东哥本人，愣了一下。）
小马哥：（假装惊讶）“哎哟，这不是老刘吗？你亲自送奶茶啊！这服务也太到位了吧！”
东子哥：（尴尬地咳嗽一声，递上奶茶）“老马，你之前可答应过我的，我刚搞外卖第一天，你就给我来了个大单子？”
小马哥：（笑嘻嘻）“嘿嘿，我这不是想支持你嘛！对了，奶茶还热乎着，你这JD速度果然名不虚传！”
东子哥：（无奈地摇摇头有点生气）“你这人啊，真是让人无语。不过话说回来，你要是以后点奶茶，我可不给你送了
小马哥：（举起奶茶，假装认真）“放心放心，我以后再也不点奶茶了！（偷偷在心里笑）”

### 组合模式
#### 组合模式的三种角色
+ 抽象组件： 定义组合中所有对象共有的方法和行为以及属性等
+ 叶子组件：组合中的单个对象
+ 容器组件：容器组件可以包含其他容器组件和叶子组件
```
class FileComp(metaclass=ABCMeta):

    @abstractmethod
    def list(self):
        pass


class File(FileComp):

    def __init__(self, name):
        self.name = name

    def list(self):
        print(self.name)


class Folder(FileComp):

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, comp):
        self.children.append(comp)

    def list(self):
        print(self.name)
        for item in self.children:
            item.list()


if __name__ == "__main__":
    root = Folder("root")
    folder1 = Folder("folder1")
    folder2 = Folder("folder2")
    file1 = File("file1")
    file2 = File("file2")

    root.add(folder1)
    root.add(folder2)
    root.add(file1)
    folder2.add(file2)

    root.list() 
```

### 装饰器模式

### 外观模式
用来封装系统的底层实现，颖仓系统复杂性，提供一组更加简单易用，更高层的接口。
#### 外观模式的2种角色
+ 外观（facade）：提供访问子系统一组统一接口，将客户端请求委派给对应的子系统处理
+ 子系统（subsystem）：实现了子系统的具体功能，并处理来自外观对象的请求
#### 外观模式的优缺点
##### 优点
+ 简化接口
+ 解耦： 客户端只需要和外观类交互
+ 灵活：可以灵活调整子系统的实现细节，而不会影响客户端调用
##### 缺点
+ 不符合开闭原则：如果新增或者修改子系统或者子系统的功能，可能需要相应的修改外观类
+ 不符合大规模系统：当子系统很复杂且分散，或者子系统之间的交互方式变化频繁，使用外观模式就不太灵活了

金将军在一次科学技术大会上提出一项计划，朝鲜也要发展新能源汽车，要求”工信部“牵头3个月内搞出来样车
这个计划可难倒了”工信部“的领导，因为他们清楚自己国家的技术水平
但是将军的命令只能无条件执行，不能说办不到；于是时任”工信部“的领导抽了一包又一包的白头山牌香烟终于想到了一个可行的办法，就是所有无法自产的核心零部件从东大采购。
他们梳理了需要采购的核心部件： 电机、电控、电池等； 再加上自产部件就可以组装成一辆车了， 于是找来了和平牌汽车的总设计师设计新能源汽车外观。

2 months later..
样车终于问世了，为啥这么快就提前完成了？是因为用了 "外观模式", 套壳生产出的。
领导兴奋的给这辆国产的首辆新能源汽车取名"阿里郎牌"
随即向将军汇报这一喜讯
```
class ElectricMachine:

    def work(self):
        print("进口电机开始工作..")


class ElectricControl:

    def init(self):
        print("电控正在初始化..")

    def work(self):
        print("电控单元已开始工作")


class BatteryEngine:

    def init(self):
        print("电池正在初始化..")

    def work(self):
        print("电池正在放电..")


# 外观类
class GreenCar:
    name = "阿里郎"

    def __init__(self):
        self.elec_machine = ElectricMachine()
        self.elec_ctrl = ElectricControl()
        self.engine = BatteryEngine()

    # 驾驶接口-普通驾驶模式
    def normal_drive(self):
        print(f"欢迎驾驶 {self.name}牌新能源汽车..")
        self.engine.init()
        self.engine.work()
        self.elec_ctrl.init()
        self.elec_ctrl.work()
        self.elec_machine.work()
```

第二天将军来到总装车间视察指导, 发现车机部分是中文的（其他地方是黑盒将军看不到），就现场问道，为什么开机画面是中文？ 
吓得负责人连忙解释道: 中文是联合国的官方语言之一，我们阿里郎到时要向东大出口赚外汇..
将军岂能这么好糊弄，一怒之下当场换了项目负责人，并要求限期整改回炉重造.. 并且这次要将启动界面部分以及内容注入具有朝鲜特色的主体思想..,并且在普通模式的基础上增加主体思想驾驶模式..

2 weeks later..
经过研发人员的日夜赶工.. 朝鲜的国产新能源汽车来了一次大换样..
```
class GreenCar:
    name = "아리랑"

    def __init__(self):
        self.elec_machine = ElectricMachine()
        self.elec_ctrl = ElectricControl()
        self.engine = BatteryEngine()

    def normal_drive(self):
        ...

    # 驾驶接口-主体思想驾驶模式
    def main_idea_drive(self):
        print(f"아리랑 신에너지 차량 운전을 환영합니다")
        self.engine.init()
        self.engine.work()
        self.elec_ctrl.init()
        self.elec_ctrl.work()

        # 开始播报主体思想指导下的生产建设新闻..
        self.elec_ctrl.play_news()

        # 开始播放主体思想歌曲
        self.elec_ctrl.play_song()

        # 新加入的主体思想含量极高的其他功能..
        # todo
        
        self.elec_machine.work()
```
这次改造之后车机界面部分换成了朝文并且增加了主体思想驾驶模式，不过这个模式由于项目赶工，做的比较糙，仅增加了一些主体思想新闻、歌曲内容..
因为要彻底改头换面不仅仅要改外观类，而且还要改动外购的"子系统"，这是一项大工程，由于时间紧，任务重，只能优先改改外观部分，就看这次能否被将军验收通过了..

### 代理模式
允许客户端在访问实际对象时添加一些其他行为（如权限检查、缓存、日志等），中间的代理对象充当客户端和实际对象间的中介。客户端通过代理类访问实际对象。
在代理模式中，代理主题和真实主题需要实现同样的接口，代理主题可以额外实现一些方法来增加一些附加功能， 代理主题和真实主题是抽象主题的子类
代理模式的核心定义是 控制对某个对象的访问，不改变被代理对象的情况下，增强或者限制其功能。
##### 代理模式的3种角色
+ 抽象主题：定义和规范了代理主题和真实主题的公共接口；
+ 真实主题：是实际执行一系列操作的对象
+ 代理主题：通过实现抽象主题接口，控制对真实主题的访问
```
# 抽象主题类
class Ticket(ABC):

    @abstractmethod
    def buy(self, start, end, money, seat):
        pass


# 真实主题类
class TicketServer(Ticket):

    def buy(self, start, end, money, seat):
        print(f"出发地: {start}, 目的地: {end}, 支付金额: {money}, 座位: {seat}")


# 代理主题类
class TicketProxy(Ticket):

    def __init__(self, server):
        self.server = server

    def is_logged_in(self):
        return True

    def buy(self, start, end, money, seat):
        if self.is_logged_in():
            self.server.buys(start, end, money, seat)
        else:
            print("请先登录系统")

# 客户端
ticketserver = TicketServer()
ticketproxy = TicketProxy(ticketserver)
ticketproxy.buy("北京", "上海", 550, "二等座13F")
```
比如我们购票可以通过代理软件购买，可以设定座位偏好等配置，代理软件会轮询通过官方购票服务进行购票。

### 责任链模式
将请求的发送者和接收者解耦，使得多个对象都可以参与到处理请求的过程中。每个处理器对象都包含下一个处理器对象的引用，环环相扣，当有请求产生时，沿着这条请求链传递，直到有对象处理它。
#### 责任链优缺点
优点：
+ 每个处理者都有明确的职责，避免职责混杂，降低对象间的耦合度
+ 增强了系统的可扩展性，可以动态的增加或者修改处理链，满足开闭原则
+ 可以动态的调整链内对象次序，可以动态的增加和删除链内对象
+ 每个链内对象只需保存一个指向后面节点的引用，无需保存所有链内对象的引用
+ 明确分工，每个处理类只处理自己关心的请求，不满足的请求传递给下一个对象即可，符合类的单一职责原则

缺点：
+ 不能保证每个请求都会被处理，某个请求可能从链首传递到链尾都得不到处理
+ 对于长责任链，可能会影响系统性能，也可能导致复杂度上升，系统维护难度加大

#### 责任链的角色
+ 处理类接口： 包含处理请求的方法和对下一个处理器对象的引用
+ 具体处理器类：实现处理器接口
+ 客戶端：创建处理器对象链，并将请求发送给链得第一个处理器对象

#### 应用场景
+ 审批流程
+ 权限管理
+ 日志记录
+ 异常处理

```
# 比如鼠标事件，计算机的外设包含鼠标、键盘等输入设备在和计算机交互时的事件处理模拟

# 事件处理类接口
class Event:

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


# 具体事件处理类1
class MouseClickEvent(Event):
    name = "鼠标点击事件"

    def handle(self, request):
        if request == "click":
            return "handle click event"
        else:
            return super().handle(request)


# 具体事件处理类2
class MouseMoveEvent(Event):
    name = "鼠标移动事件"

    def handle(self, request):
        if request == "move":
            return "handle move event"
        else:
            return super().handle(request)


# 具体事件处理类3
class KeyBoardEvent(Event):
    name = "键盘按下事件"

    def handle(self, request):
        if request == "space":
            return "handle space event"
        else:
            return super().handle(request)

# 客户端
event1 = MouseClickEvent()
event2 = MouseMoveEvent()
event3 = KeyBoardEvent()
event1.set_next(event2).set_next(event3)
requests = ["click", "move", "space", "enter"]

for request in requests:
    resp = event1.handle(request)
    if resp:
        print(resp)
    else:
        print(f"无法识别该事件:{request}")
```
县水利局的办公室里，一股烟味弥漫。股长周明远手里捏着一份河道清淤工程的审批表，眉头紧锁。这工程预算报了五百万，可实际成本，他心里门儿清，三百万撑死了。​
办事员小孙凑过来，低声说：“周股长，这工程老板可是张总的远房亲戚，您看这审批……”​
周明远狠狠吸了口烟，吐出个烟圈：“你小子懂什么？这表我要是批了，出了事谁担着？往上递。” 说着，就把审批表往副局长刘志强桌上送。​
刘志强拿起审批表，手指在数字上敲了敲，似笑非笑地说：“明远啊，你这是把难题给我送来了。张总前阵子还请咱们局里人吃饭，这面子不能不给。但这数儿，也太扎眼了。我看，还是让局长定夺。”​
局长王建军正在打电话，挂了电话，拿起审批表看了看，脸色沉了下来：“你们俩，一个推一个。这工程是县里的重点项目，出了岔子谁都跑不了。周股长，你去核实一下实际工程量，看看有没有虚报；志强，你去查查张总的公司资质，有没有问题；小孙，你把近几年类似工程的预算整理出来，做个对比。”​
周明远心里咯噔一下，他知道，这核实工程量就是走个过场，张总早就打点好了下面的人。刘志强也明白，查公司资质不过是掩人耳目，张总的关系网，他可不敢得罪。小孙更是清楚，整理预算就是做做样子，最后还得按上面的意思来。​
这就像一条绳上的蚂蚱，谁也跑不掉。周明远要是不把审批表往上递，自己独吞好处，万一被查，就是死路一条。刘志强要是不顺着来，张总那边不好交代，以后在局里也不好混。王建军要是把事情捅出去，整个水利局都会受牵连，他这个局长也别想当了。
```
# 上面的虚构故事用下面的责任链模式模拟其如何运作
# 审批事件处理类接口
class Event:

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


# 具体事件处理类1
class Event1(Event):
    name = "股长审批环节"

    def handle(self, request):
        if request.event_flow == "股长审批止":
            # 扣40%  直接通过审批
            request.money -= request.money * 0.4
            request.result = "pass"
            return request 
        else:
            # 自己扣5%  交给上一级处理
            request.money -= request.money * 0.05
            return super().handle(request)


# 具体事件处理类2
class Event2(Event):
    name = "副局长审批环节"

    def handle(self, request):
        if request.event_flow == "副局审批止":
            # 扣35%  直接通过审批
            request.money -= request.money * 0.35
            request.result = "pass"
            return request
        else:
            # 自己扣10%  交给上一级处理
            request.money -= request.money * 0.1
            return super().handle(request)


# 具体事件处理类3
class Event3(Event):
    name = "局长审批环节"

    def handle(self, request):
        if request.event_flow == "局长审批止":
            # 扣25%  直接通过审批
            request.money -= request.money * 0.25
            request.result = "pass"
            return request
        else:
            # 自己扣15%  交给上一级处理
            request.money -= request.money * 0.15
            return super().handle(request)

# 客户端
event1 = Event1()
event2 = Event2()
event3 = Event3()
event1.set_next(event2).set_next(event3)


class Request:
    def __init__(self, event_flow, money, result=None):
        self.event_flow = event_flow
        self.money = money
        self.result = result


# 河道清淤工程的审批申请, 该项目需要局长审批才能通过，工程总预算500w
request = Request("局长审批止", 5000000)

# 通过层层克扣后，实际用于工程实施的项目款只剩下300w
resp = event1.handle(request)
```

### 中介者模式 
用于多个对象之间的交互解耦，使得对象间通信更加灵活和简单
#### 中介者的角色
+ 抽象中介者
+ 具体中介者： 实现抽象中介者接口，负责协调各个通信对象间的交互关系
+ 抽象同事类：定义各个同事对象的接口，包含一个指向中介者对象的引用，以便与中介者通信
+ 具体同事类：实现了抽象同事类的接口，负责实现各自的行为，和中介者对象进行通信，通常会在中介者中注册自己
#### 中介者模式的优缺点
优点：
+ 降低耦合度： 同事间不在互相通信，而是通过中介者
+ 集中管理： 所有的交互逻辑都集中一个地方，易于维护和管理扩展

缺点：
+ 增加中介者的复杂度： 由于所有交互逻辑都集中在中介者中，可能导致中介者的代码变得越来越复杂
+ 导致系统瓶颈： 中介者可能成为系统瓶颈

#### 应用场景
+ gui组件协作： 中介者模式可以用于在不同的gui控件间提供协调和管理
+ 聊天应用
+ 工作流管理：不同任务或节点之间的交互可以通过中介者进行管理
```
class User:

    def __init__(self, name):
        self.name = name
        self.mediator = None

    def send_msg(self, msg):
        self.mediator.send_msg(msg, self)

    def receive_msg(self, msg):
        print(f"{self.name} received msg: {msg}")


class ChatRoom:

    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)
        user.mediator = self

    def send_msg(self, msg, sender):
        for user in self.users:
            if user != sender:
                user.receive_msg(msg)


chat_room = ChatRoom()

bob = User("Bob")
sam = User("Sam")
peter = User("Peter")

chat_room.add_user(bob)
chat_room.add_user(sam)
chat_room.add_user(peter)

bob.send_msg("Hello, every one!")
sam.send_msg("Hi, Bob!")
peter.send_msg("Hello, I'm Peter!")
```

### 其他设计模式 未完待续, 点赞关注不迷路!

## 设计模式的7原则
- 单一职责（SRP）：不要将太多杂乱的功能放到一个类中 要聚焦 高内聚 低耦合 降低类的复杂度 提高代码可读性 可维护性和可重用性
- 开闭原则（OCP）：对扩展开放 对修改关闭 可以通过抽象化来避免修改已有代码的风险 而从降低软件维护的成本
- 里氏替换（LSP）：任何基类出现的地方 子类也可以出现 这个原则强调的是面向对象的继承和多态特性 通过保证子类的行为和父类一致 从而提高代码的可维护性和可扩展性
- 依赖反转（DIP）：要依赖抽象 而不是依赖具体实现 通过抽象化减少组件之间的耦合性 使得代码更加灵活 易于维护和扩展
- 合成/聚合复用（CARP | 组合优于继承）：要尽量使用对象组合或者聚合关系，而不是继承关系以达到代码复用目的
- 迪米特法则（LoD）：系统中的类尽量不要与其他类相互作用 减少类之间的耦合度, 换句话来说就是 一个对象应对其他对象有尽可能少的了解 不需要了解的内容尽量不了解  强调组件之间的松耦合
- 接口隔离（ISP） 客户端不应依赖它不需要的接口 即一个类对其它类的的依赖应该建立在最小的接口上  强调接口设计的合理性 避免暴露不必要的接口导致类之间的耦合性过高且增加了安全风险

## 参考链接
+ https://blog.csdn.net/qq_18529581/article/details/149184981?spm=1001.2014.3001.5502
+ https://www.cnblogs.com/liugp/p/17134320.html#9%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8Fstrategy
