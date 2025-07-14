"""开头
模块名要简短，采用小写字母，必要时使用下划线提高可读性。
包名和模块名类似，包名中不推荐使用下划线
模块说明balabala..
"""  # 单独成行   对于单行的文档说明 尾部三引号和单行文本在同一行

from __future__ import barry_as_FLUFL  # __future__ 导入位于文件顶部 在模块注释和文档字符串之后 在模块的__all__和__version__等之前

__all__ = ['BaseClass']
__version__ = '0.1 alpha'

import os  # 导入内置模块， 导入位于文件顶部 在模块注释和文档字符串之后 在模块的全局变量和常量之前
import sys
# 不推荐 import os, sys

import requests  # 导入三方模块

from selfdefinedpackage import selfdefinedmodule  # 本地导入 导入自定义模块 推荐使用绝对路径导入


global_a = 1  # 全局变量
CONSTANT_A = 1  # 常量


# 方式1：垂直缩进 左括号对齐, 没有使用垂直缩进时 禁止将参数放在第一行
def function1(args1, args2,
             arg3, arg4):
    return 1


# 与其他行区分, 当缩进没有与其他行区分时  要增加缩进
def function2(
        args1, arg2, arg3):
    pass


# 当if语句条件太长需要换行时， 不妨增加一个空格并增加一个左括号
if condition1 and condition2 and condition3 and condition4 and \
    condition5 and condition6 and condition7:
    pass

# 可改为
if (condition1 and condition2 and condition3 and condition4 and
    condition5 and condition6 and condition7):
    pass


mlist = [
    1, 2, 3,
    4, 5, 6,
    ]

# 或者
mlist = [
    1, 2, 3,
    4, 5, 6,
]


# 调用函数
result = function1(
    "args1", "arg2",
    "arg3", "arg4",
    )


# 或者
result = function1(
    "args1", "arg2",
    "arg3", "arg4",
)


# 传统风格通常在二元运算符之前断行 但是更推荐在二元运算符之后中端 具体和本地的约定保持一致
total = (first_value + second_value
         + third_value
         - forth_value)


# 推荐
x = x*3 + 1
# 不推荐
x = x * 3 + 1


if a == 1:
    do_somethings()

# 不推荐
if a == 1: do_somethings()


# 建议尽量使用 def 申明函数 而不是 function = lambda x: x*2


# 返回的语句应保持一致 函数中的返回语句都应该返回一个表达式 或者都不返回
def function3(args1):
    if x >= 1:
        return True
    else:
        return None

# 不推荐
def function4(args1):
    if x >= 1:
        return True


class BaseClass(object):
    """ 类说明
    balabala..
    """

    def base_method(self):
        pass




