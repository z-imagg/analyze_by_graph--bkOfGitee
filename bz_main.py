#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

from collections import defaultdict
import typing
from neo4j import Session
from neo4j.graph import Node
from file_tool import readTxt
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt

def lsIsEmpty(ls:typing.List[typing.Any])->bool:
    empty:bool = ls is None or len(ls) == 0
    return empty

def assertSonLsEmptyWhenLeaf(isLeaf:bool,sonLs:typing.List[Node]):
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

class BzDeepth(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度
    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[int], _)->int:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,_)

        #deepth数值列表即为S
        deepth_ls:typing.List[int]= S
        
        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)

        #叶子的deepth为0,非叶子的deepth为 1+直接孩子们的deepth的最大值
        d=0 if isLeaf  else 1+max(deepth_ls)

        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return d

class BzWriteDeepth(TraverseAbs):

    cypher__update_setFieldDeepth=readTxt("cypher_src/update_setFieldDeepth.cypher") 

    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度 并 写deepth字段为深度值
    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[int], _)->int:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,_)
    
        #deepth数值列表即为S
        deepth_ls:typing.List[int]= S

        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)
        
        #叶子的deepth为0,非叶子的deepth为 1+直接孩子们的deepth的最大值
        d=0 if isLeaf  else 1+max(deepth_ls)
        neo4j_update(sess,"update_setFieldDeepth",BzWriteDeepth.cypher__update_setFieldDeepth,params={"prm_fnCallId":fnCallId,"prm_deepth":d},filedName="更新记录数")
        print(f"BzWriteDeepth.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段deepth={d}; 第{self.Vi}次遍历")
        
        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return d

class BzWriteWidth(TraverseAbs):
    cypher__update_setFieldWidth=readTxt("cypher_src/update_setFieldWidth.cypher") 

    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

    def bz(self, RE:Node, RL:Node, isLeaf:bool, _, C:typing.List[Node])->Node:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,C)
        
        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)

        #叶子的width为0,非叶子的width为直接孩子个数
        width=0 if isLeaf  else len(sonLs)
        #写width字段
        neo4j_update(sess,"update_setFieldWidth",BzWriteWidth.cypher__update_setFieldWidth,params={"prm_fnCallId":fnCallId,"prm_width":width},filedName="更新记录数")
        print(f"BzWriteWidth.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段width={width}; 第{self.Vi}次遍历")

        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return None
    
class 址数:
    def __init__(self,fnAdr:str,cnt:int) -> None:
        self.址:str=fnAdr
        self.数:int=cnt

class 成份:
    def __init__(self) -> None:
        self.内容:typing.List[址数] = []
    
    def 填1个(self,fnAdr:str ):
        self.内容.append(址数(fnAdr,1))
        return self
    
    @staticmethod
    def merge(*成份们:typing.List['成份'])-> '成份':
        k:成份
        dct = defaultdict(int)
        for k in 成份们:
            for j in k.内容:
                dct[j.址] += j.数
        新=成份()
        新.内容.extend(dct.items())
        return 新


class BzWrite成份(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[成份], _) -> 成份:

        #断言起点、终点fnAdr相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnAdr=assertRE_fnAdr_eq_RL__return_fnAdr(RE,RL)

        markup=None
        if isLeaf:
            #不写成份字段
            markup= 成份( ).填1个(fnAdr)
        else:
            #写成份字段
            markup= 成份( ).merge(*S)
        
        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return markup



if __name__=="__main__":
    from neo4j import Driver,GraphDatabase
    from neo4j_tool_traverse import NTT
    RootFnCallId=13#1,2,5,
    NEO4J_DB="neo4j"
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")

    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            #初始化: 全体置空deepth字段
            update__init_deepth_as_null(sess)
            
            # 起点RE
            RE:Node=NTT(sess).getE_byFnCallId(RootFnCallId)
            # 遍历过程中 计算深度
            # BzDeepth(sess).V(RE)
            # 遍历过程中 计算深度 并 写deepth字段为深度值
            BzWriteDeepth(sess).V(RE)
            # BzWriteWidth().V(RE)
            # BzWrite成份().V(RE)

    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


    

