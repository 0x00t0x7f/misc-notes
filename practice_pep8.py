# Copyright 2025 by kleex, Inc. All Rights Reserved.

"""开头
模块名要简短，采用小写字母，必要时使用下划线提高可读性。
包名和模块名类似，包名中不推荐使用下划线
模块说明balabala..
"""  # 单独成行   对于单行的文档说明 尾部三引号和单行文本在同一行


from __future__ import barry_as_FLUFL  # __future__ 导入位于文件顶部 在模块注释和文档字符串之后 在模块的__all__和__version__等之前

__all__ = [
  'BaseClass',
  'HTTPServerError'
]
__version__ = '0.1 alpha'

import os  # 导入内置模块， 导入位于文件顶部 在模块注释和文档字符串之后 在模块的全局变量和常量之前
import sys
# 不推荐 import os, sys

import requests  # 导入三方模块

from selfdefinedpackage import selfdefinedmodule  # 本地导入 导入自定义模块 推荐使用绝对路径导入 在绝对路径比较长时可使用相对路径
from functools import *  # 避免使用通配符导入


global_a = 1  # 全局变量: 尽量用于模块内部  为了避免使用 from M import * 导入该全局变量 可使用__all__机制或者为全局变量加前置下划线
CONSTANT_A = 1  # 常量


# 方式1：垂直缩进 左括号对齐, 没有使用垂直缩进时 禁止将参数放在第一行
def function1(args1, args2,
             arg3, arg4):
    return 1


# 悬挂缩进与其他行区分, 当缩进没有与其他行区分时  要增加缩进
def function2(
        args1, arg2, arg3):
    pass


# 当if语句条件太长需要换行时， 不妨增加一个空格并增加一个左括号
if condition1 and condition2 and condition3 and condition4 and \
    condition5 and condition6 and condition7:
    pass

# 可改为 换行后额外添加缩进（换行）
if (condition1 and condition2 and condition3 and condition4 
      and condition5 and condition6 and condition7):
    do_something()


mlist = [
    1, 2, 3,
    4, 5, 6,
    ]

# 或者（推荐）
mlist = [
    1, 2, 3,
    4, 5, 6,
]


# 调用函数
result = function1(
    "args1", "arg2",
    "arg3", "arg4",
    )


# 或者（推荐）
result = function1(
    "args1", "arg2",
    "arg3", "arg4",
)


# 限制行最大行宽不超过80个字符， pycharm中标称线最大是74个字符(和相关默认配置有关系)  现代宽屏显示器下可以适当提高到80~100之间，建议和团队的约定一致
# line>:零一二三四五六七八九零一二三四五六七八九零一二三四五六七八九零一二三四五六七八九零一二三四五六七八九零一二三四五六七八九零一二三四五六七八九零一二三|四五六七八九


# 传统风格通常在二元运算符之前断行 但是更推荐在二元运算符之后中断 具体写法和本地的约定保持一致
total = (first_value + second_value
         + third_value
         - forth_value)


# 优先级高的运算符或操作符的前后不建议添加空格 
x = x*3 + 1
# 不推荐
x = x * 3 + 1


# 赋值等操作符前后不能因为对齐而添加多个空格
x = 1
y = 2
long_var = "a"

# 不推荐这样
x        = 1
y        = 2
long_var = "a"


if a == 1:
    do_somethings()

# 不推荐
if a == 1: do_somethings()


# 推荐
if x is not None

# 不推荐
if not x is None


# 对序列非空判断
if seq:
  pass

if not seq:
  pass


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


# 注释: 求两数乘积（与代码矛盾的注释比没有注释更糟糕，修改代码后需更新注释和代码意图保持一致）
def add(x, y):
  """函数注释..

  补充注释..
  """
  return x + y

xy = Point(1, 2)空格空格# 坐标值   <-- 行内注释：行内注释是和语句在同一行，通常用两个空格和语句分开，行内注释尽量少用，重复啰嗦使人分心，除非这行语句不用行内注释会使阅读者困扰


# 首尾有下划线的情况
_model_global_name = "LLM_MODEL"  # 单前置下划线：弱内部使用标志 如 from M import * 不会导入下划线开头的对象
model_global_name_ = "LLM_MODEL"  # 单后置下划线：用于避免与python关键词的冲突   def main(class_="ClassName"): pass


class BaseClass(object):
    """ 类说明
    balabala..
    """

    def base_method(self):
        pass

    @classmethod
    def class_method(cls):
      pass

    @staticmethod
    def static_method(args1, args2):
      pass


class HTTPServerError(Exception):
  pass
