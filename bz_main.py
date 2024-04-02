#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Session
from neo4j.graph import Node
from file_tool import readTxt
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt

class BzDeepth(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度
    def bz(self,RE,RL,isLeaf:bool,deepth_ls:typing.List[int],_)->int:
        E_fnCallId=RE['fnCallId']
        L_fnCallId=RL['fnCallId']
        assert E_fnCallId == L_fnCallId

        if isLeaf: return 0
        else:
            return 1+max(deepth_ls)

class BzWriteDeepth(TraverseAbs):

    cypher__update_setFieldDeepth=readTxt("cypher_src/update_setFieldDeepth.cypher") 

    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度 并 写deepth字段为深度值
    def bz(self,RE,RL,isLeaf:bool,deepth_ls,_)->int:


        E_fnCallId=RE['fnCallId']
        L_fnCallId=RL['fnCallId']
        assert E_fnCallId == L_fnCallId

        fnCallId=E_fnCallId

        
        d=0 if isLeaf  else 1+max(deepth_ls)
        neo4j_update(sess,"update_setFieldDeepth",BzWriteDeepth.cypher__update_setFieldDeepth,params={"prm_fnCallId":fnCallId,"prm_deepth":d},filedName="更新记录数")
        print(f"BzWriteDeepth.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段deepth={d}; 第{self.Vi}次遍历")
        
        return d

class BzWriteWidth(TraverseAbs):
    def bz(self,RE,RL,isLeaf:bool,_,childLs):
        pass

class BzWrite成份(TraverseAbs):
    def bz(self,RE,RL,isLeaf:bool,S,_):
        pass



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


    

