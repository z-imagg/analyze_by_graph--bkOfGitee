#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 
#【备注】 
#【术语】 

import typing
from neo4j import Driver, EagerResult, GraphDatabase, ResultSummary, Session,Result
from neo4j.graph import Node


#例子cypher语句: 删除索引、创建索引 V_Demo.logId
Cypher_recreateIdx__V_Demo__logId=\
"DROP INDEX idxName__V_Demo__logId IF EXISTS"
"CREATE INDEX idxName__V_Demo__logId FOR (n:V_Demo) ON (n.logId)"
"show indexes"
# "DROP INDEX ON :V_Demo(logId)" #这种index语句更直白，但不支持if exists，可以手工用，但程序里不好用

#neo4j重建索引（neo4j删除索引、创建索引）
def neo4j_recreateIdx(sess:Session,Cypher_Txt:str)->int:

    result:Result=sess.run(Cypher_Txt)
    # s=result.single()
    # v=result.value()
    summry:ResultSummary=result.consume()

    print(f"删除索引{summry.counters.indexes_removed}条, 创建索引{summry.counters.indexes_added}条")
    return summry.counters.indexes_removed + summry.counters.indexes_added


#例子cypher语句: 删除约束、创建约束 unique(V_Demo.logId)
Cypher_recreateConstraint__V_Demo__logId=\
"DROP CONSTRAINT uq__V_Demo__logId IF EXISTS"
"CREATE CONSTRAINT uq__V_Demo__logId FOR (x:V_Demo) REQUIRE x.logId IS UNIQUE"

#neo4j重建约束（neo4j删除约束、创建约束）
def neo4j_recreateConstraint(sess:Session,Cypher_Txt:str)->int:

    result:Result=sess.run(Cypher_Txt)
    # s=result.single()
    # v=result.value()
    summry:ResultSummary=result.consume()

    print(f"删除索引{summry.counters.constraints_removed}条, 创建索引{summry.counters.constraints_added}条")
    return summry.counters.constraints_removed + summry.counters.constraints_added
