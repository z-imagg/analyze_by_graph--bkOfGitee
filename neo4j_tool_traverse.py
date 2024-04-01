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
from neo4j_tool import neo4j_update, neo4j_query

class NTT:
    def __init__(self,sess:Session) -> None:
        self.sess:Session= sess

    def getE(self,fnCallId):
        return neo4j_query(self.sess,"getE",cypher__getE,params={"fnCallId":fnCallId})

    def getL(self,fnCallId):
        return neo4j_query(self.sess,"getL",cypher__getL,params={"fnCallId":fnCallId})

    def isLeaf(self,fnCallId):
        return neo4j_query(self.sess,"isLeaf",cypher__getL,params={"fnCallId":fnCallId})

    def getChild_len_i(self,fnCallId,len_i:int):
        cypherTxt=cypherTmplRender("cypher_src/query__fE_t__fEL_t_multipleK__t_fL__tmpl.cypher",len_i, "//直接调用平链元素(模板)(match)\n", "//开发调试用，生产不要使用\n")
        return neo4j_query(self.sess,f"getChild_len_i_{len_i}",cypherTxt,params={"fnCallId":fnCallId})

    def getChild(self,fnCallId):
        tnPnt_delta=100
        for i in range(1,tnPnt_delta+1):
            c=self.getChild_len_i(fnCallId,i)
            if c is not None: return c

