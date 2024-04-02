#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
from neo4j.graph import Node

from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs

def lsIsEmpty(ls:typing.List[typing.Any])->bool:
    empty:bool = ls is None or len(ls) == 0
    return empty

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


