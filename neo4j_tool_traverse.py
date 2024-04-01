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
cypher__getChild=readTxt("cypher_src/query__fE_t__fEL_t_multipleK__t_fL__tmpl.cypher") 



from cypher_tmpl_render import cypherTmplRender
from neo4j_tool import neo4j_update, neo4j_query,neo4j_query_1field1row

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

    def getChild_len_i(self,fnCallId,len_i:int):
        cypherTxt=cypherTmplRender("cypher_src/query__fE_t__fEL_t_multipleK__t_fL__tmpl.cypher",len_i, "//直接调用平链元素(模板)(match)\n", "//直接调用平链元素(模板)(where)\n")
        return neo4j_query_1field1row(self.sess, f"getChild_len_i_{len_i}", cypherTxt, params={"fnCallId":fnCallId}, filedName="路径")

    def getChild(self,RE:Node):
        fnCallId=RE["fnCallId"]
        tnPnt_delta=100
        for i in range(1,tnPnt_delta+1):
            c=self.getChild_len_i(fnCallId,i)
            if c is not None: 
                return c
        return None

