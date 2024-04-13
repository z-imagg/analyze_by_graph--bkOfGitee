#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 
#【备注】 
#【术语】 

import typing
from neo4j import Driver, EagerResult, GraphDatabase, ResultSummary, Session,Result
from neo4j.graph import Node

from util_basic import strIsEmpty

#neo4j执行cypher语句
def _neo4j_run_cypherTxt(sess:Session,Cypher_Txt:str)->ResultSummary:

    result:Result=sess.run(Cypher_Txt)
    # s=result.single()
    # v=result.value()
    summry:ResultSummary=result.consume()

    return summry



#例子cypher语句: 删除索引、创建索引 V_Demo.logId
Cypher_recreateIdx__V_Demo__logId="""
DROP INDEX idxName__V_Demo__logId IF EXISTS;
CREATE INDEX idxName__V_Demo__logId FOR (n:V_Demo) ON (n.logId);
show indexes;
"""
# "DROP INDEX ON :V_Demo(logId)" #这种index语句更直白，但不支持if exists，可以手工用，但程序里不好用

#neo4j重建索引（neo4j删除索引、创建索引）
def neo4j_recreateIdx(sess:Session,Multi_Cypher_Txt:str)->int:
    Cypher_Txt_ls=Multi_Cypher_Txt.split(";")
    rm_cnt=0
    add_cnt=0
    for Cypher_Txt  in Cypher_Txt_ls:
        Cypher_Txt=Cypher_Txt.strip()
        #跳过空行、跳过注释
        if strIsEmpty(Cypher_Txt) or Cypher_Txt.startswith("//"): continue
        
        summry:ResultSummary=_neo4j_run_cypherTxt(sess,Cypher_Txt)
        rm_cnt += summry.counters.indexes_removed
        add_cnt += summry.counters.indexes_added
        print(f"删除索引{summry.counters.indexes_removed}条, 创建索引{summry.counters.indexes_added}条")
    return rm_cnt + add_cnt


#例子cypher语句: 删除约束、创建约束 unique(V_Demo.logId)
Cypher_recreateConstraint__V_Demo__logId="""
DROP CONSTRAINT uq__V_Demo__logId IF EXISTS;
CREATE CONSTRAINT uq__V_Demo__logId FOR (x:V_Demo) REQUIRE x.logId IS UNIQUE;
"""

#neo4j重建约束（neo4j删除约束、创建约束）
def neo4j_recreateConstraint(sess:Session,Multi_Cypher_Txt:str)->int:

    Cypher_Txt_ls=Multi_Cypher_Txt.split(";")
    rm_cnt=0
    add_cnt=0
    for Cypher_Txt  in Cypher_Txt_ls:
        Cypher_Txt=Cypher_Txt.strip()
        #跳过空行、跳过注释
        if strIsEmpty(Cypher_Txt) or Cypher_Txt.startswith("//"): continue
            
        print(Cypher_Txt)
        summry:ResultSummary=_neo4j_run_cypherTxt(sess,Cypher_Txt)
        rm_cnt += summry.counters.constraints_removed
        add_cnt += summry.counters.constraints_added
        print(f"删除约束{summry.counters.indexes_removed}条, 创建约束{summry.counters.indexes_added}条")
    return rm_cnt + add_cnt

