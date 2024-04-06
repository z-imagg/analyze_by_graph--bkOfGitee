#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 基本工具函数
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

## 基本工具函数

### 列表判空
def lsIsEmpty(ls:typing.List[typing.Any]) -> bool:
    return ls is None or len(ls) == 0

### join 整数们
def joinInts(_intLs:typing.List[int],_sep:str=",")->str:
    _strLs=[f"{k}" for k in _intLs]
    return _sep.join(_strLs)