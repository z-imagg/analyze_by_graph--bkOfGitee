#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 写 neo4j 顶点(日志行号）、边（同fnCallId的进和出） 
#【术语】 Sq3Log==Sq3FnCallLog, wrt==write,whn==when,trv==Traverse
#【备注】 
#【术语】 

import typing
import sqlite3

from neo4j import Driver, EagerResult, GraphDatabase, ResultSummary, Session,Result
## 写 neo4j 顶点(日志行号）、边（同fnCallId的进和出） 


# 写 neo4j 顶点(日志行号）、边（同fnCallId的函数进入指向函数退出） 
# ，来自 https://neo4j.com/docs/api/python-driver/5.18/#quick-example


### python连接neo4j



from neo4j import GraphDatabase, RoutingControl

from const import Neo4j_Integer_Print
from neo4j_db_basic import Neo4J_DB_Entity, getDriver
from neo4j_delete_all import deleteAll
from neo4j_index_constraint import neo4j_recreateConstraint, neo4j_recreateIdx
from util_datetime import nowDateTimeTxt, printLn
from sqlite3_basic_Q_fnCallLog import queryFnEnterLeave

# driver.close() #到最后再关闭neo4j的连接

### 删除现有顶点、边
def neo4j_del_v_e(sess:Session):
    #### 删除关系 E_FnEL
    # E_FnEL == "Edge FunctionEnter  ---> FunctionLeave"
    #  删除关系 E_FnEL
    Cypher_delete_E_FnEL="""
MATCH ()-[r:E_FnEL]-()
WITH r
LIMIT 100000
DETACH DELETE r
"""
    # 循环删除, 因为一次行删除 可能报内存超出
    deleteAll(sess,Cypher_delete_E_FnEL,"E_FnEL")

    #### 删除关系 E_NxtTmPnt
    #  E_NxtTmPnt == "Edge 时刻点TmPnt  ---> 下一个 时刻点TmPnt"
    #  删除关系 E_FnEL
    Cypher_delete_E_NxtTmPnt="""
MATCH ()-[r:E_NxtTmPnt]-()
WITH r
LIMIT 100000
DETACH DELETE r
"""
    # 循环删除, 因为一次行删除 可能报内存超出
    deleteAll(sess,Cypher_delete_E_NxtTmPnt,"E_NxtTmPnt")



    #### 删除顶点 V_FnCallLog

    #  删除顶点 V_FnCallLog
    Cypher_delete_V_FnCallLog="""
MATCH (n:V_FnCallLog)
WITH n
LIMIT 100000
DETACH DELETE n
"""

    # 循环删除, 因为一次行删除 可能报内存超出
    deleteAll(sess,Cypher_delete_V_FnCallLog,"V_FnCallLog")



"""
一次删除全部顶点(边)可能报内存超出

一次删除全部顶点语句如下
cypher
MATCH (n:V_FnCallLog)
DELETE n


一次删除全部边语句如下
cypher
MATCH ()-[r:E_FnEL]-()
DELETE r
"""

### neo4j创建索引

#### neo4j 删除 索引 V_FnCallLog.logId

# neo4j重建索引 V_FnCallLog.logId
def neo4j_recreate___idx__V_FnCallLog__logId(sess:Session):
    Cypher_recreateIdx_V_FnCallLog__logId=\
    "DROP INDEX idx__V_FnCallLog__logId IF EXISTS"
    "CREATE INDEX idx__V_FnCallLog__logId FOR (n:V_FnCallLog) ON (n.logId)"
    neo4j_recreateIdx(sess,Cypher_recreateIdx_V_FnCallLog__logId)

### neo4j创建unique约束
    # neo4j重建unique约束 V_FnCallLog.logId
def neo4j_recreate___uq__V_FnCallLog__logId(sess:Session):
#### neo4j 创建  unique约束 V_FnCallLog.logId
    _Cypher__uq__V_FnCallLog__logId=\
    "DROP CONSTRAINT uq__V_FnCallLog__logId IF EXISTS"
    "CREATE CONSTRAINT uq__V_FnCallLog__logId FOR (x:V_FnCallLog) REQUIRE x.logId IS UNIQUE"
    neo4j_recreateConstraint(sess,_Cypher__uq__V_FnCallLog__logId)
#### neo4j 创建  unique约束 V_FnCallLog.tmPnt
    _Cypher__uq__V_FnCallLog__tmPnt=\
    "DROP CONSTRAINT uq__V_FnCallLog__tmPnt IF EXISTS"
    "CREATE CONSTRAINT uq__V_FnCallLog__tmPnt FOR (x:V_FnCallLog) REQUIRE x.tmPnt IS UNIQUE"
    neo4j_recreateConstraint(sess,_Cypher__uq__V_FnCallLog__tmPnt)


### 遍历fnCallId过程中写neo4j顶点、边
def neo4j_wrtVFnCallLog_EFnEL_whnTrvSq3Log(sq3dbConn:sqlite3.Connection,notBalancedFnCallIdLs:typing.List[int],sess:Session):
#### sqlite3 sql语句模板
    sqlTmpl_t_FnCallLog_query_fnCallId_ls="select distinct fnCallId  from t_FnCallLog order by fnCallId asc"
    sqlTmpl_t_FnSym_query_by_address="select  *  from t_FnSym where address=?"
    #开发调试用
    # sqlTmpl_t_FnCallLog_query_fnCallId_ls="select distinct fnCallId  from t_FnCallLog limit 1000"

#### 遍历fnCallId
    #循环操作neo4j过程中,打印进度时所用的判定整数

    #  遍历fnCallId
    for fnCallIdRow in sq3dbConn.execute(sqlTmpl_t_FnCallLog_query_fnCallId_ls):
        fnCallId=fnCallIdRow["fnCallId"]
        
        if fnCallId % Neo4j_Integer_Print == 0 : printLn(f"write V_FnCallLog__E_FnEL,fnCallId={fnCallId}")
        # print("开发调试打印",type(fnCallId), fnCallId.keys())
        
        assert fnCallId not in notBalancedFnCallIdLs, \
    f"断言 遍历fnCallId 中 无应该有 不平衡的fnCallId={fnCallId}, notBalancedFnCallIdLs={notBalancedFnCallIdLs}"

        #按照fnCallId查询出 函数进入、函数离开 日志
        fnEnter,fnLeave=queryFnEnterLeave(sq3dbConn,fnCallId)

        fnEnter_logId=fnEnter["logId"]
        fnLeave_logId=fnLeave["logId"]
        assert fnEnter_logId != fnLeave_logId, "断言 函数进入、函数离开 日志 中的 logId 是 不相同的"
        
        fnEnter_tmPnt=fnEnter["tmPnt"]
        fnLeave_tmPnt=fnLeave["tmPnt"]
        assert fnEnter_tmPnt != fnLeave_tmPnt, "断言 函数进入、函数离开 日志 中的 tmPnt 是 不相同的"
        
        fnEnter_fnAdr=fnEnter["fnAdr"]
        fnLeave_fnAdr=fnLeave["fnAdr"]
        assert fnEnter_fnAdr == fnLeave_fnAdr, "断言 函数进入、函数离开 日志 中的 函数地址 是 相同的"
        
        fnEnter_curThreadId=fnEnter["curThreadId"]
        fnLeave_curThreadId=fnLeave["curThreadId"]
        assert fnEnter_curThreadId == fnLeave_curThreadId, "断言 函数进入、函数离开 日志 中的 curThreadId 是 相同的"
        
        fnEnter_direct=fnEnter["direct"]
        fnLeave_direct=fnLeave["direct"]
        assert fnEnter_direct != fnLeave_direct, "断言 函数进入、函数离开 日志 中的 direct 是 不相同的"
        
        # print(fnEnter["fnAdr"]) #开发调试语句
        # break

        #按照函数地址 查询函数调试信息
        _fnSymLs=sq3dbConn.execute(sqlTmpl_t_FnSym_query_by_address, [fnEnter_fnAdr]).fetchall()
        # 断言 该函数地址 只能查询到一个调试信息
        assert len(_fnSymLs) == 1
        fnSym=_fnSymLs[0]
        # print(fnSym)
        
        fnSym_address=fnSym["address"]
        fnSym_name=fnSym["name"]
        fnSym_moduleName=fnSym["moduleName"]
        fnSym_fileName=fnSym["fileName"]
        fnSym_lineNumber=fnSym["lineNumber"]
        fnSym_column=fnSym["column"]

        #插入到neo4j
        sess.run(
"CREATE (fnEnter_:V_FnCallLog \
{logId: $fnEnter_logId, tmPnt: $fnEnter_tmPnt, curThreadId: $curThreadId, direct:$fnEnter_direct, \
fnAdr:$fnAdr, fnCallId:$fnCallId, fnSym_address:$fnSym_address, fnSym_name:$fnSym_name, \
fnSym_moduleName:$fnSym_moduleName, fnSym_fileName:$fnSym_fileName, fnSym_lineNumber:$fnSym_lineNumber, \
fnSym_column:$fnSym_column}) "
"CREATE (fnLeave_:V_FnCallLog \
{logId: $fnLeave_logId, tmPnt: $fnLeave_tmPnt, curThreadId: $curThreadId, direct:$fnLeave_direct, \
fnAdr:$fnAdr, fnCallId:$fnCallId, fnSym_address:$fnSym_address, fnSym_name:$fnSym_name, \
fnSym_moduleName:$fnSym_moduleName, fnSym_fileName:$fnSym_fileName, fnSym_lineNumber:$fnSym_lineNumber, \
fnSym_column:$fnSym_column}) "
"CREATE (fnEnter_)-[:E_FnEL  {fnCallId:$fnCallId, fromLogId: $fnEnter_logId, toLogId:$fnLeave_logId, fnEnter_tmPnt:$fnEnter_tmPnt, fnLeave_tmPnt:$fnLeave_tmPnt}]->(fnLeave_)",
# "CREATE (fnEnter)-[:Edge2]->(fnLeave)",
# 以下这些是作为 参数 parameters_ 的
fnEnter_logId=fnEnter_logId,fnLeave_logId=fnLeave_logId,
fnEnter_tmPnt=fnEnter_tmPnt,fnLeave_tmPnt=fnLeave_tmPnt,
curThreadId=fnEnter_curThreadId, 
fnEnter_direct=fnEnter_direct, fnLeave_direct=fnLeave_direct, 
fnAdr=fnEnter_fnAdr, 
fnCallId=fnCallId, 
fnSym_address=fnSym_address,
fnSym_name=fnSym_name,
fnSym_moduleName=fnSym_moduleName,
fnSym_fileName=fnSym_fileName,
fnSym_lineNumber=fnSym_lineNumber,
fnSym_column=fnSym_column,

)

#  2024-04-03 18:24:28 061030,fnCallId=100000
#  2024-04-03 18:27:30 800301,fnCallId=200000
#  2024-04-03 18:30:08 995134,fnCallId=300000
#  2024-04-03 18:32:42 058069,fnCallId=400000
#  2024-04-03 18:35:21 108303,fnCallId=500000
#  2024-04-03 18:38:26 945242,fnCallId=600000
#  2024-04-03 18:40:58 851231,fnCallId=700000
#  2024-04-03 18:43:47 817747,fnCallId=800000

#### 开发调试用语句

#设置sqlite3.connect.execute.fetchall返回tuple列表而非字典列表 （人类可读用）
# sq3dbConn.row_factory=origin_sq3dbConn_row_factory

# sq3dbConn.execute("select distinct fnCallId from t_FnCallLog limit 10").fetchall()
    # [(2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,)]


# sq3dbConn.execute(" PRAGMA table_info(t_FnCallLog) ").fetchall()
    # [(0, 'logId', 'INTEGER', 0, None, 1),
    #  (1, 'tmPnt', 'INTEGER', 0, None, 0),
    #  (2, 'processId', 'INTEGER', 0, None, 0),
    #  (3, 'curThreadId', 'INTEGER', 0, None, 0),
    #  (4, 'direct', 'short', 0, None, 0),
    #  (5, 'fnAdr', 'char(18)', 0, None, 0),
    #  (6, 'fnCallId', 'INTEGER', 0, None, 0),
    #  (7, 'fnSymId', 'char(18)', 0, None, 0)]

# sq3dbConn.execute(" PRAGMA table_info(t_FnSym) ").fetchall()
    # [(0, 'address', 'char(18)', 0, None, 1),
    #  (1, 'name', 'varchar(256)', 0, None, 0),
    #  (2, 'moduleName', 'varchar(32)', 0, None, 0),
    #  (3, 'fileName', 'varchar(256)', 0, None, 0),
    #  (4, 'lineNumber', 'INTEGER', 0, None, 0),
    #  (5, 'column', 'INTEGER', 0, None, 0)]

# sq3dbConn.execute("select * from t_FnCallLog where logId <=2").fetchall()
#     [(2, 2, 21580, 21580, 1, '0x555555565000', 2, '0x555555565000')]

#还原 
# 设置sqlite3.connect.execute.fetchall返回字典列表而非tuple列表  （程序用）
# sq3dbConn.row_factory = sqlite3.Row

# sq3dbConn.execute(sqlTmpl_t_FnCallLog_query_by_fnCallId, [1]).fetchall()

