#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象
import typing

from file_tool import readTxt
from neo4j_misc import update__init_deepth_as_null
from neo4j_tool import neo4j_update
T = typing.TypeVar('T')
from abc import abstractmethod,ABC
from neo4j import Session
from neo4j_tool_traverse import NTT

from neo4j.graph import Node

class TraverseAbs(ABC):
    def __init__(self,sess:Session) -> None:
        super().__init__()
        self.N:NTT= NTT(sess)

    def V(tz,RE:Node):
        fnCallId=RE['fnCallId']
        print(f"开始遍历 fnCallId={fnCallId}；",end=" ")
        RL:Node=tz.N.getL(RE)
        if tz.N.isLeaf(RE):
            print(f"是叶子")
            return tz.bz(RE,RL,True,None,None)
        C=tz.N.getChild__by__query_BJ_fJ_LJ_tJ_(RE)
        print(f"孩子个数{len(C)}")
        S=[tz.V(CkE) for CkE in C]
        return tz.bz(RE,RL,False,S,C)

    @abstractmethod
    def bz(self,RE,RL,isLeaf:bool,S,C)->T:
        raise Exception("你的抽象方法书写的不对，因为py应该自己确保不能调用此抽象方法，而不是靠我这个异常来确保")

class BzDeepth(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

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

    def bz(self,RE,RL,isLeaf:bool,deepth_ls,_)->int:
        E_fnCallId=RE['fnCallId']
        L_fnCallId=RL['fnCallId']
        assert E_fnCallId == L_fnCallId

        fnCallId=E_fnCallId

        
        d=0 if isLeaf  else 1+max(deepth_ls)
        neo4j_update(sess,"update_setFieldDeepth",BzWriteDeepth.cypher__update_setFieldDeepth,params={"prm_fnCallId":fnCallId,"prm_deepth":d},filedName="更新记录数")
        
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
            
            #遍历
            RE:Node=NTT(sess).getE_byFnCallId(RootFnCallId)
            # BzDeepth(sess).V(RE)
            BzWriteDeepth(sess).V(RE)
            # BzWriteWidth().V(RE)
            # BzWrite成份().V(RE)

    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


    

