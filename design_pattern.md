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


## 设计模式的7原则
- 单一职责（SRP）：不要将太多杂乱的功能放到一个类中 要聚焦 高内聚 低耦合 降低类的复杂度 提高代码可读性 可维护性和可重用性
- 开闭原则（OCP）：对扩展开放 对修改关闭 可以通过抽象化来避免修改已有代码的风险 而从降低软件维护的成本
- 里氏替换（LSP）：任何基类出现的地方 子类也可以出现 这个原则强调的是面向对象的继承和多态特性 通过保证子类的行为和父类一致 从而提高代码的可维护性和可扩展性
- 依赖反转（DIP）：要依赖抽象 而不是依赖具体实现 通过抽象化减少组件之间的耦合性 使得代码更加灵活 易于维护和扩展
- 合成/聚合复用（CARP）：要尽量使用对象组合或者聚合关系，而不是继承关系以达到代码复用目的
- 迪米特法则（LoD）：系统中的类尽量不要与其他类相互作用 减少类之间的耦合度, 换句话来说就是 一个对象应对其他对象有尽可能少的了解 不需要了解的内容尽量不了解  强调组件之间的松耦合
- 接口隔离（ISP） 客户端不应依赖它不需要的接口 即一个类对其它类的的依赖应该建立在最小的接口上  强调接口设计的合理性 避免暴露不必要的接口导致类之间的耦合性过高且增加了安全风险

## 参考链接
+ https://www.cnblogs.com/liugp/p/17134320.html#9%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8Fstrategy
