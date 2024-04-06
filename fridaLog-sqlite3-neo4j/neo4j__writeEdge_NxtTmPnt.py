#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 写 neo4j 边（时刻点 到 下一个 时刻点） 
#【术语】 
#【备注】 
#【术语】 

import typing
import sqlite3
import neo4j

#循环操作neo4j过程中,打印进度时所用的判定整数
from const import Neo4j_Integer_Print

from sqlite3_basic_Q_fnCallLog import queryFnCallLogByTmPnt
from tool_basic import lsIsEmpty, nowDateTimeTxt




##  写 neo4j 边（时刻点 到 下一个 时刻点） 




### 术语

#  tmPnt == timePoint == 时刻点 == 给定的 进程id_线程id 下的 时刻点

### 说明

#  给定的 进程id_线程id 下的 时刻点 取值 总是 一些列 连续整数, 

#  具体实现 参见  [frida_js.git/DebugSymbolUtil.ts](http://giteaz:3000/frida_analyze_app_src/frida_js/src/branch/main/DebugSymbolUtil.ts) 中的 变量 gTmPntTb

### sqlite3 sql语句模板






### 按照tmPnt查询出 调用日志








# #最小时刻点
# tmPnt_min:int=sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_min).fetchone()["tmPnt_min"]

# #最大时刻点
# tmPnt_max:int=sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_max).fetchone()["tmPnt_max"]



#  from_tmPnt 取值范围为 区间[tmPnt_min,tmPnt_max-1]

#  to_tmPnt 取值范围为 区间[tmPnt_min+1,tmPnt_max]

### 跳过不平衡的 to_tmPnt
def skipNotBalanced__to_tmPnt(notBalancedTmPntLs:typing.List[int],from_tmPnt:int) -> int:
    to_tmPnt=from_tmPnt+1
    
    while to_tmPnt in notBalancedTmPntLs:
        print(f"跳过不平衡的 to_tmPnt={to_tmPnt}")
        to_tmPnt+=1
    
    return to_tmPnt


# print(f"notBalancedFnCallIdLs={notBalancedFnCallIdLs}")
    # notBalancedFnCallIdLs=[1]

# 遍历 时刻点TmPnt
def neo4j_writeVFnCallLog_writeEFnEL_whenTraverseSq3FnCallId(
sq3dbConn:sqlite3.Connection,  neo4j_sess:neo4j.Session,
notBalancedTmPntLs:typing.List[int],
notBalancedFnCallIdLs:typing.List[int],
tmPnt_max:int,tmPnt_min:int,
):
    for from_tmPnt in range(tmPnt_min,tmPnt_max):
        
        #打印 进度
        if from_tmPnt % Neo4j_Integer_Print == 0 : print(f"{nowDateTimeTxt()},from_tmPnt={from_tmPnt}")

        # 查询 '来源时刻点from_tmPnt' 下 仅有的一条日志
        fromLog=queryFnCallLogByTmPnt(sq3dbConn,from_tmPnt)
        if fromLog is None:
            assert from_tmPnt in notBalancedTmPntLs, \
    f"TmPnt链条断裂处点一定在notBalancedTmPntLs中, from_tmPnt={from_tmPnt}, notBalancedTmPntLs={notBalancedTmPntLs}"
            #跳过 TmPnt链条断裂处点
            continue
        
        #从 来源时刻点from_tmPnt 指向 下一个时刻点to_tmPnt
        to_tmPnt:int=skipNotBalanced__to_tmPnt(from_tmPnt)

        from_fnCallId:int=fromLog["fnCallId"]
        assert from_fnCallId not in notBalancedFnCallIdLs ,\
    f"断言 遍历 时刻点TmPnt 中 无应该有 不平衡的from_fnCallId={from_fnCallId}, notBalancedFnCallIdLs={notBalancedFnCallIdLs}"

                
        # 查询 '下一个时刻点to_tmPnt' 下 仅有的一条日志
        toLog=queryFnCallLogByTmPnt(sq3dbConn,to_tmPnt)
        
        fromLogId=fromLog["logId"]
        toLogId=toLog["logId"]

        
        to_fnCallId=toLog["fnCallId"]
        # print(f"fromLogId={fromLogId},toLog={toLogId}")
        
        neo4j_sess.run(
#'neo4j 索引 V_FnCallLog.logId' 加速 以下两个MATCH查询
#  找到最小时刻点
"MATCH (from_Log:V_FnCallLog {logId: $fromLogId})"
#  找到最小时刻点
"MATCH   (to_Log:V_FnCallLog {logId: $toLogId})"
#创建 时刻边
"CREATE (from_Log)-[:E_NxtTmPnt {fromLogId: $fromLogId, toLogId:$toLogId, from_fnCallId:$from_fnCallId, to_fnCallId:$to_fnCallId }]->(to_Log)",
# 以下这些是作为 参数 parameters_ 的
fromLogId=fromLogId, 
toLogId=toLogId, 
from_fnCallId=from_fnCallId,
to_fnCallId=to_fnCallId,
)
    


    # 2024-04-03 18:46:33 573101,from_tmPnt=100000
    # 2024-04-03 18:48:49 402940,from_tmPnt=200000
    # 2024-04-03 18:51:04 668170,from_tmPnt=300000
    # 2024-04-03 18:53:20 252960,from_tmPnt=400000
    # 2024-04-03 18:55:40 755761,from_tmPnt=500000
    # 2024-04-03 18:58:14 580239,from_tmPnt=600000
    # 2024-04-03 19:00:32 925351,from_tmPnt=700000
    # 2024-04-03 19:03:12 796370,from_tmPnt=800000
    # 2024-04-03 19:05:45 081395,from_tmPnt=900000
    # 2024-04-03 19:08:02 524231,from_tmPnt=1000000
    # 2024-04-03 19:10:21 903764,from_tmPnt=1100000
    # 2024-04-03 19:13:00 016782,from_tmPnt=1200000
    # 2024-04-03 19:15:30 202599,from_tmPnt=1300000
    # 2024-04-03 19:17:56 961675,from_tmPnt=1400000
    # 2024-04-03 19:20:28 632259,from_tmPnt=1500000
    # 2024-04-03 19:22:48 274321,from_tmPnt=1600000


### 开发调试用语句
# { **sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_min).fetchall()[0] }
    # {'tmPnt_min': 2}

# { **sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_max).fetchall()[0] }
    # {'tmPnt_max': 1619593}

# tmPnt_min,tmPnt_max, len(range(tmPnt_min,tmPnt_max+1))
    # (2, 1619593, 1619592)

