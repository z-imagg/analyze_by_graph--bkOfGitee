#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象
#【术语】 V==traverse==遍历, tz==thiz==this==self, Vi==traverse index==第多少次遍历
#【术语】 RE==R Enter==进入函数==起点, RL==R Leave==离开函数==终点, C==children==起点RE的直接孩子链, bz==busy==业务函数, S==Sum==将bz应用到每个直接孩子所得列表
#【术语】 CkE==第k个孩子的起点, CkL==第k个孩子的终点
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
import typing

T = typing.TypeVar('T')
from abc import abstractmethod,ABC
from neo4j import Session
from neo4j_tool_traverse import NTT

from neo4j.graph import Node

class TraverseAbs(ABC):
    def __init__(self,sess:Session) -> None:
        super().__init__()
        self.N:NTT= NTT(sess)
        
        #记录遍历次数 （即调用遍历方法V的次数）, 主要用于观看遍历进度
        self.Vi:int=0

        #当遍历函数V结束时,self.cur_fnCallId==最后一个fnCallId
        self.cur_fnCallId:int=None
        #当遍历函数V结束时,self.cur_tmPnt==最后一个tmPnt
        self.cur_tmPnt:int=None

    def V(tz,RE:Node)->T:
        tz.Vi+=1

        fnCallId:int=RE['fnCallId'] ; tz.cur_fnCallId:int=fnCallId
        tmPnt:int=RE['tmPnt'] ; tz.cur_tmPnt:int=tmPnt
        
        print(f"{tz.__class__.__name__},开始遍历 fnCallId={fnCallId}； tmPnt={tmPnt}；",end=" ")
        RL:Node=tz.N.getL(RE)
        if tz.N.isLeaf(RE):
            print(f"是叶子")
            return tz.bz(RE,RL,True,None,None)
        C:typing.List[Node]=tz.N.getChild__by__query_BJ_fJ_LJ_tJ_(RE)
        print(f"孩子个数{len(C)}")
        S:typing.List[T]=[tz.V(CkE) for CkE in C]
        return tz.bz(RE,RL,False,S,C)

    @abstractmethod
    def bz(self,RE:Node,RL:Node,isLeaf:bool,S:typing.List[T],C:typing.List[Node])->T:
        raise Exception("你的抽象方法书写的不对，因为py应该自己确保不能调用此抽象方法，而不是靠我这个异常来确保")




if __name__=="__main__":
    raise Exception("请您去执行main.py,这里是遍历器算法，需要保持干净，且不能作为入口执行")


    

