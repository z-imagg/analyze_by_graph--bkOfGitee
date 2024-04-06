#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Driver, EagerResult, GraphDatabase, ResultSummary, Session,Result
from neo4j.graph import Node
import pandas
from util_basic import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from file_tool import readTxt
from neo4j_2db_main import neo4j2dbMain
from neo4j_db_basic import Neo4J_DB_Entity
from neo4j_delete_all import deleteAll
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

def executeDropCreateIdx(sess_anlz:Session,Cypher_:str)->int:

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

def _visual_main(sess:Session, sess_anlz:Session, _:Driver,  __:Driver):
    # executeDropCreateIdx(sess_anlz, Cypher_IdxDropCreate)
    deleteAll(sess_anlz,Cypher_delete__E_P2S)
    deleteAll(sess_anlz,Cypher_delete__V_FnCallLog_Analz)

    rowLs:typing.List[typing.Dict[str,typing.Any]]=neo4j_query_RowLs(sess,"_visual_main", cypher__query__链条_宽_宽1深, params={})
    nodeTab= dict([ (r["fnCallId"],r)for r in rowLs])

    ####循环插入点V_FnCallLog_Analz
    for k,r in enumerate(rowLs):
        result:EagerResult=sess_anlz.run(
"CREATE (x:V_FnCallLog_Analz {logId: $logId, tmPnt: $tmPnt, curThreadId: $curThreadId, direct:$direct, fnAdr:$fnAdr, fnCallId:$fnCallId, width:$width, deepth:$deepth,   fnSym_address:$fnSym_address, fnSym_name:$fnSym_name, fnSym_moduleName:$fnSym_moduleName, fnSym_fileName:$fnSym_fileName, fnSym_lineNumber:$fnSym_lineNumber, fnSym_column:$fnSym_column})",
logId=r["logId"], tmPnt=r["tmPnt"],  curThreadId=r["curThreadId"],  direct=r["direct"], 
fnAdr=r["fnAdr"], fnCallId=r["fnCallId"], width=r["width"], deepth=r["deepth"],   fnSym_address=r["fnSym_address"], fnSym_name=r["fnSym_name"], 
fnSym_moduleName=r["fnSym_moduleName"], fnSym_fileName=r["fnSym_fileName"], fnSym_lineNumber=r["fnSym_lineNumber"], 
fnSym_column=r["fnSym_column"],)
        
        s=result.single()
        v=result.value()
        summary:ResultSummary=result.consume()
        # summary_4driver:ResultSummary=result.summary
        if k % 1000 == 0:
            print(f"创建点;k={k},fnCallId={r['fnCallId']},创建节点{summary.counters.nodes_created}个,创建Label{summary.counters.labels_added}个")
    
    print(f"k={k}")
    
    for k,r in enumerate(rowLs):
        fnCallId=r["fnCallId"]
        sonFnCallIdLs:typing.List[int]=json.loads(r["sonFnCallIdLs"])
        for j,sonFnCallId in enumerate(sonFnCallIdLs):
            son=nodeTab.get(sonFnCallId,None)
            if son is not None:
                result:Result=sess_anlz.run(
"MATCH (parent:V_FnCallLog_Analz {fnCallId:$parent__fnCallId})"
#  找到最小时刻点
"MATCH   (son:V_FnCallLog_Analz  {fnCallId:$son__fnCallId})"
#构建 边 parentFnCallId --> sonFnCallId
"CREATE (parent  )-[:E_P2S  {parent__logId:$parent__logId, son__logId:$son__logId, parent__tmPnt:$parent__tmPnt, son__tmPnt:$son__tmPnt, parent__fnCallId:$parent__fnCallId, son__fnCallId: $son__fnCallId,   parent__width:$parent__width, parent__deepth:$parent__deepth,  son__width:$son__width, son__deepth:$son__deepth}]->(son   )"
,

parent__logId=r["logId"], parent__tmPnt=r["tmPnt"],  parent__curThreadId=r["curThreadId"],  parent__direct=r["direct"], 
parent__fnAdr=r["fnAdr"], parent__fnCallId=r["fnCallId"], parent__width=r["width"], parent__deepth=r["deepth"],   parent__fnSym_address=r["fnSym_address"], parent__fnSym_name=r["fnSym_name"], 
parent__fnSym_moduleName=r["fnSym_moduleName"], parent__fnSym_fileName=r["fnSym_fileName"], parent__fnSym_lineNumber=r["fnSym_lineNumber"], 
parent__fnSym_column=r["fnSym_column"],
son__logId=son["logId"], son__tmPnt=son["tmPnt"],  son__curThreadId=son["curThreadId"],  son__direct=son["direct"], 
son__fnAdr=son["fnAdr"], son__fnCallId=son["fnCallId"], son__width=son["width"], son__deepth=son["deepth"],   son__fnSym_address=son["fnSym_address"], son__fnSym_name=son["fnSym_name"], 
son__fnSym_moduleName=son["fnSym_moduleName"], son__fnSym_fileName=son["fnSym_fileName"], son__fnSym_lineNumber=son["fnSym_lineNumber"], 
son__fnSym_column=son["fnSym_column"]

)
            
                # s=result.single()
                # v=result.value()
                summary:ResultSummary=result.consume()
                if k % 1000 == 0:
                    print(f"创建边;k={k},j={j}; 【fnCallId={fnCallId}】 --> 【sonFnCallId={son['fnCallId']}】; sonFnCallIdLs尺寸={len(sonFnCallIdLs)}; 创建边{summary.counters.relationships_created}个 ")


if __name__=="__main__":
    db_main= Neo4J_DB_Entity(URI="neo4j://localhost:7687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")
    db_anlz= Neo4J_DB_Entity(URI="neo4j://localhost:5687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")
    neo4j2dbMain(db1=db_main, db2=db_anlz, func=_visual_main)



    
