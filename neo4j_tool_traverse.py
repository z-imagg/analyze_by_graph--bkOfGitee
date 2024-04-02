from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver
from neo4j import Record,Result,Session
from neo4j.graph import Node
import pandas
import typing
import numpy
from pathlib import Path

from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
from file_tool import readTxt


cypher__getE=readTxt("cypher_src/getE.cypher") 
cypher__getL=readTxt("cypher_src/getL.cypher") 
cypher__isLeaf=readTxt("cypher_src/isLeaf.cypher") 
cypher__query__起_t入_B0=readTxt("cypher_src/query__起_t入_B0.cypher") 
cypher__query_BJ_fJ_LJ_tJ_=readTxt("cypher_src/query_BJ_fJ_LJ_tJ_.cypher") 



from cypher_tmpl_render import cypherTmplRender
from neo4j_tool import neo4j_query_1row, neo4j_update, neo4j_query,neo4j_query_1field1row

class NTT:
    def __init__(self,sess:Session) -> None:
        self.sess:Session= sess

    def getE_byFnCallId(self,fnCallId:int)->Node:
        return neo4j_query_1field1row(self.sess,"getE",cypher__getE,params={"fnCallId":fnCallId},filedName="logV")

    def getL(self,RE:Node)->Node:
        fnCallId=RE["fnCallId"]
        return neo4j_query_1field1row(self.sess,"getL",cypher__getL,params={"fnCallId":fnCallId},filedName="logV")

    def isLeaf(self,RE:Node)->bool:
        fnCallId=RE["fnCallId"]
        匹配起点个数= neo4j_query_1field1row(self.sess,"isLeaf",cypher__isLeaf,params={"fnCallId":fnCallId},filedName="匹配起点个数")
        if 匹配起点个数>0:
            assert 匹配起点个数 ==1
        return 匹配起点个数 == 1


    _LIMIT_SON_CNT:int = 10_0000  #拍脑袋写的，意思是 任何一个函数内容（循环展开后）不应该含有10_0000次函数调用
    #【测试用例】fnCallId,  13 有直接孩子链 [14, 162005, 162007, 162026, 162033, 175635, 175640, 205785, 205790, 225167, 227838]
    def getChild__by__query_BJ_fJ_LJ_tJ_(self,RE:Node)->typing.List[Node]:
        B:Node; #t:?
        fnCallId:int=RE["fnCallId"]
        B2:Node= neo4j_query_1field1row(self.sess,"query__起_t入_B0",cypher__query__起_t入_B0,params={"fnCallId":fnCallId},filedName="B2" )
        ls:typing.List[Node]=[] ; fnCallId_k:int=B2["fnCallId"]
        for _ in range(0,NTT._LIMIT_SON_CNT):
            B,t= neo4j_query_1row(self.sess,f"往前拱到第{_}小节query_BJ_fJ_LJ_tJ_",cypher__query_BJ_fJ_LJ_tJ_,params={"fnCallId":fnCallId_k},filedNameLs=["BJ","tJ"] )
            assert B is not None
            ls.append(B) ; print(f"{B['fnCallId']}",end=", ")
            fnCallId_k=t["to_fnCallId"]
            if fnCallId_k == fnCallId: 
                son_chain=[k["fnCallId"] for k in ls] #变量son_chain 只为测试用，无业务作用
                # print(f"【测试用例】 fnCallId={fnCallId} 有直接孩子链 son_chain={son_chain}")
                return ls

        raise Exception("不应该到这里")
    
    

