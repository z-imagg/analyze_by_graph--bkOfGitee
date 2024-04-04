#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Driver, GraphDatabase, ResultSummary, Session,Result
from neo4j.graph import Node
import pandas
from bz_util import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from file_tool import readTxt
from neo4j_2db_main import neo4j2dbMain
from neo4j_db_entity import Neo4J_DB_Entity
from neo4j_main import neo4jMain
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_query, neo4j_query_RowLs, neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
from math import log2


from itertools import chain
from pathlib import Path
import json

cypher__query__链条_宽_宽1深=readTxt("cypher_src/query__链条_宽_宽1深.cypher") 


Cypher_IdxDropCreate=\
"DROP CONSTRAINT uq__V_FnCallLog_Analz__fnCallId IF EXISTS"
"CREATE CONSTRAINT uq__V_FnCallLog_Analz__fnCallId FOR (x:V_FnCallLog_Analz) REQUIRE x.fnCallId IS UNIQUE"
"DROP CONSTRAINT uq__V_FnCallLog_Analz__logId IF EXISTS"
"CREATE CONSTRAINT uq__V_FnCallLog_Analz__logId FOR (x:V_FnCallLog_Analz) REQUIRE x.logId IS UNIQUE"
"DROP CONSTRAINT uq__V_FnCallLog_Analz__tmPnt IF EXISTS"
"CREATE CONSTRAINT uq__V_FnCallLog_Analz__tmPnt FOR (x:V_FnCallLog_Analz) REQUIRE x.tmPnt IS UNIQUE"

def executeDropCreate(sess_anlz:Session,Cypher_:str)->int:
    delete_row_cnt:int = 0

    result:Result=sess_anlz.run(Cypher_)
    s=result.single()
    v=result.value()
    summry:ResultSummary=result.consume()
    return

# 删除关系 E_P2S
Cypher_delete__E_P2S="""
MATCH ()-[r:E_P2S]-()
WITH r
LIMIT 1000
DETACH DELETE r
"""
# 删除关系 V_FnCallLog_Analz
Cypher_delete__V_FnCallLog_Analz="""
MATCH (n:V_FnCallLog_Analz)
WITH n
LIMIT 1000
DETACH DELETE n
"""
def deleteAll(sess_anlz:Session,Cypher_:str)->int:
    del_node_cnt:int = 0
    del_edge_cnt:int = 0

    # 循环删除, 因为一次行删除 可能报内存超出
    while True:
        result:Result=sess_anlz.run(Cypher_)
        # s=result.single()
        # v=result.value()
        summry:ResultSummary=result.consume()
        del_node_cnt += summry.counters.nodes_deleted
        del_edge_cnt += summry.counters.relationships_deleted
        if summry.counters.nodes_deleted == 0 and summry.counters.relationships_deleted == 0:
            print(f"一共删除{del_node_cnt}条记录")
            return

def _visual_main(sess:Session,sess_anlz:Session):
    executeDropCreate(sess_anlz, Cypher_IdxDropCreate)
    deleteAll(sess_anlz,Cypher_delete__E_P2S)
    deleteAll(sess_anlz,Cypher_delete__V_FnCallLog_Analz)

    rowLs:typing.List[typing.Dict[str,typing.Any]]=neo4j_query_RowLs(sess,"_visual_main", cypher__query__链条_宽_宽1深, params={})
    nodeTab= dict([ (r["fnCallId"],r)for r in rowLs])
    fnCallIdLs= [ r["fnCallId"]for r in rowLs]

    for r in rowLs:
        result:Result=sess_anlz.run(
query=
#构建 节点parent
"CREATE (parent:V_FnCallLog_Analz {logId: $logId, tmPnt: $tmPnt, curThreadId: $curThreadId, direct:$direct, \
fnAdr:$fnAdr, fnCallId:$fnCallId, width:$width, deepth:$deepth,   fnSym_address:$fnSym_address, fnSym_name:$fnSym_name, \
fnSym_moduleName:$fnSym_moduleName, fnSym_fileName:$fnSym_fileName, fnSym_lineNumber:$fnSym_lineNumber, \
fnSym_column:$fnSym_column})",
parameters=r)
        
    
    for r in rowLs:
        fnCallId=r["fnCallId"]
        sonFnCallIdLs:typing.List[int]=json.loads(r["sonFnCallIdLs"])
        for sonFnCallId in sonFnCallIdLs:
            son=nodeTab.get(sonFnCallId,None)
            if son is not None:
                result:Result=sess_anlz.run(
query=
#
"MATCH (parent:V_FnCallLog_Analz {fnCallId:$parent__fnCallId})"
#  找到最小时刻点
"MATCH   (son:V_FnCallLog_Analz  {fnCallId:$son__fnCallId})"
#构建 边 parentFnCallId --> sonFnCallId
"CREATE (parent  )-[:E_P2S  {parent_logId:$parent_logId, son_logId:$son_logId, parent__tmPnt:$parent__tmPnt, son__tmPnt:$son__tmPnt, parent__fnCallId:$parent__fnCallId, son__fnCallId: $son__fnCallId,   parent__width:$parent__width, parent__deepth:$parent__deepth,  son__width:$son__width, son__deepth:$son__deepth}]->(son   )"
,

parent_logId=r["logId"], parent__tmPnt=r["tmPnt"],  parent__curThreadId=r["curThreadId"],  parent__direct=r["direct"], 
parent__fnAdr=r["fnAdr"], parent__fnCallId=r["fnCallId"], parent__width=r["width"], parent__deepth=r["deepth"],   parent__fnSym_address=r["fnSym_address"], parent__fnSym_name=r["fnSym_name"], 
parent__fnSym_moduleName=r["fnSym_moduleName"], parent__fnSym_fileName=r["fnSym_fileName"], parent__fnSym_lineNumber=r["fnSym_lineNumber"], 
parent__fnSym_column=r["fnSym_column"],
son_logId=son["logId"], son__tmPnt=son["tmPnt"],  son__curThreadId=son["curThreadId"],  son__direct=son["direct"], 
son__fnAdr=son["fnAdr"], son__fnCallId=son["fnCallId"], son__width=son["width"], son__deepth=son["deepth"],   son__fnSym_address=son["fnSym_address"], son__fnSym_name=son["fnSym_name"], 
son__fnSym_moduleName=son["fnSym_moduleName"], son__fnSym_fileName=son["fnSym_fileName"], son__fnSym_lineNumber=son["fnSym_lineNumber"], 
son__fnSym_column=son["fnSym_column"]

)
            # if sonFnCallId in fnCallIdLs:
                #构建 节点r 、 节点son
                #节点字段 logId, fnCallId, width, deepth, fnAdr, 调试信息等
                pass


if __name__=="__main__":
    db_main= Neo4J_DB_Entity(URI="neo4j://localhost:7687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")
    db_anlz= Neo4J_DB_Entity(URI="neo4j://localhost:5687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")
    neo4j2dbMain(db1=db_main, db2=db_anlz, func=_visual_main)



    
#neo4j社区版 同一个服务下 同时只能访问一个数据库，因此再开一个neo4j服务
#docker run -d -p 5474:7474 -p 5687:7687 --name neo4j_anlz -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community