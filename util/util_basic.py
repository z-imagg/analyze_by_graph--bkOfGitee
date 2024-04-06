#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 基本工具函数
#【术语】 
#【备注】 
#【术语】 

import typing
from neo4j.graph import Node

from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs

### 列表判空
def lsIsEmpty(ls:typing.List[typing.Any])->bool:
    empty:bool = ls is None or len(ls) == 0
    return empty


### join 整数们
def joinInts(_intLs:typing.List[int],_sep:str=",")->str:
    _strLs=[f"{k}" for k in _intLs]
    return _sep.join(_strLs)


from datetime import datetime
def nowDateTimeTxt():
    return datetime.now()   .strftime( '%Y-%m-%d %H:%M:%S %f' ) 


def assertSonLsEmptyWhenLeaf(isLeaf:bool,sonLs:typing.List[Node]) :
    #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
    if isLeaf:
        assert lsIsEmpty(sonLs)

def assertRE_fnCallId_eq_RL__return_fnCallId(RE:Node, RL:Node)->int:
    #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
    E_fnCallId=RE['fnCallId']
    L_fnCallId=RL['fnCallId']
    assert E_fnCallId == L_fnCallId
    fnCallId:int=E_fnCallId
    return fnCallId

def assertRE_fnAdr_eq_RL__return_fnAdr(RE:Node, RL:Node)->str:
    #断言起点、终点fnAdr相同，目的是 检验本项目的其他地方逻辑是否有问题
    E_fnAdr=RE['fnAdr']
    L_fnAdr=RL['fnAdr']
    assert E_fnAdr == L_fnAdr
    fnAdr:str=E_fnAdr
    return fnAdr

#断言数组作为集合只有1个元素， 即 数组中 都是某一个元素的重复
def assert_ls_as_set_only_1_element(intLs:typing.List[int])->int:
    intSet:typing.List[int]=[*set(intLs)]
    assert len(intSet) == 1
    _int:int=intSet[0]
    return _int