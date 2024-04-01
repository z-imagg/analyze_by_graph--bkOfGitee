#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象
import typing
T = typing.TypeVar('T')
from abc import abstractmethod,ABC
from neo4j import Session
from neo4j_tool_traverse import NTT


class TraverseAbs(ABC):
    def __init__(self,sess:Session) -> None:
        super().__init__()
        self.N:NTT= NTT(sess)

    def V(tz,RE):
        RL=tz.N.getL(RE)
        if tz.N.isLeaf(RE,RL):
            return tz.bz(RE,RL,True,None,None)
        C=tz.N.getChild(RE,RL)
        S=[tz.V(CkE) for CkE,CkL in C]
        return tz.bz(RE,RL,False,S,C)

    @abstractmethod
    def bz(self,RE,RL,isLeaf:bool,S,C)->T:
        raise Exception("你的抽象方法书写的不对，因为py应该自己确保不能调用此抽象方法，而不是靠我这个异常来确保")

class BzDeepth(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

    def bz(self,RE,RL,isLeaf:bool,deepth_ls:typing.List[int],_)->int:
        if isLeaf: return 0
        else:
            return 1+max(deepth_ls)

class BzWriteDeepth(TraverseAbs):
    def bz(self,RE,RL,isLeaf:bool,deepth_ls,_):
        pass

class BzWriteWidth(TraverseAbs):
    def bz(self,RE,RL,isLeaf:bool,_,childLs):
        pass

class BzWrite成份(TraverseAbs):
    def bz(self,RE,RL,isLeaf:bool,S,_):
        pass



if __name__=="__main__":
    from neo4j import Driver,GraphDatabase
    from neo4j_tool_traverse import NTT

    NEO4J_DB="neo4j"
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")

    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            RE=NTT(sess).getE_byFnCallId(1)
            BzDeepth(sess).V(RE)
            # BzWriteDeepth().V(RE)
            # BzWriteWidth().V(RE)
            # BzWrite成份().V(RE)
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


    

