#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 
#【备注】 
#【术语】 

import typing
from neo4j import Driver, EagerResult, GraphDatabase, ResultSummary, Session,Result
from neo4j.graph import Node


#例子cypher语句: 删除关系 E_Demo， 一页
_Cypher_delete__E_Demo="""
MATCH ()-[r:E_Demo]-()
WITH r
LIMIT 1000
DETACH DELETE r
"""
#例子cypher语句: 删除关系 V_Demo， 一页
_Cypher_delete__V_Demo="""
MATCH (n:V_Demo)
WITH n
LIMIT 1000
DETACH DELETE n
"""

#neo4j逐页删除所有记录行
def deleteAll(sess_anlz:Session,Cypher_:str,tilte:str="无标题")->int:
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
            print(f"{tilte},一共删除{del_node_cnt+del_edge_cnt}条记录")
            return
