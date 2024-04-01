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
    BzDeepth().V(None)
    # BzWriteDeepth().V(None)
    # BzWriteWidth().V(None)
    # BzWrite成份().V(None)
    

