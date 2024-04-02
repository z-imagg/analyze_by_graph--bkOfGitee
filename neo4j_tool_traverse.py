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
cypher__query_入T入=readTxt("cypher_src/query_入T入.cypher") 
cypher__query_tinySeg=readTxt("cypher_src/query_tinySeg.cypher") 



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
    def getChild__by__query_tinySeg(self,RE:Node)->bool:
        fnCallId=RE["fnCallId"]
        B2= neo4j_query_1field1row(self.sess,"query_入T入",cypher__query_入T入,params={"fnCallId":fnCallId},filedName="B2" )
        ls=[]
        Bk=B2
        for _ in range(0,NTT._LIMIT_SON_CNT):
            ls.append(Bk)
            fnCallId_k=Bk["fnCallId"]
            B,t= neo4j_query_1row(self.sess,"query_tinySeg",cypher__query_tinySeg,params={"fnCallId":fnCallId_k},filedNameLs=["BJ","tJ"] )
            if t["fnCallId"] == fnCallId:
                return ls
            assert B is not None
            Bk=B

        raise Exception("不应该到这里")
    
    def getChild_len_i(self,fnCallId,len_i:int):
        cypherTxt=cypherTmplRender("cypher_src/query__tinySeg.cypher",len_i, "//直接调用平链元素(模板)(match)", "//直接调用平链元素(模板)(where)","//直接调用平链元素(模板)(return)")
        # print(cypherTxt)
        df:pandas.DataFrame=neo4j_query_1row(self.sess, f"getChild_len_i_{len_i}", cypherTxt, params={"fnCallId":fnCallId})
        records=df.to_dict(orient="records")
        rowCnt=len(records) #rowCnt==行数
        if rowCnt == 0:
            return None,cypherTxt
        if rowCnt>0:
            assert rowCnt == 1, "给定fnCallId, 直接方法链条 只能有一个 （即df的行数==1）"
        row0=records[0]#row0==首行
        columnCnt=len(row0)#columnCnt==列数
        B_cnt=columnCnt-1
        B_ls=[row0[f"B{i}"] for i in range(B_cnt)]
            
        return  B_ls, cypherTxt

    
    def _found_child_save_cypherTxt(self,fnCallId,len_i,cypherTxt)->None:
        outDir="./cypher_tmpl_reander_out/"
        Path(outDir).mkdir(parents=True,exist_ok=True)
        Path(f"{outDir}/query__fE_t__fEL_t_multipleK__t_fL__fnCallId_{fnCallId}__len_{len_i}.cypher").write_text(cypherTxt)
        # print(cypherTxt)
        return

