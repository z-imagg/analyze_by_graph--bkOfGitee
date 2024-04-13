#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 
#【备注】 
#【术语】 

import typing
import sqlite3
import neo4j
from neo4j import Driver

from db_conn_inject.dbConn_inject__sqlite3_neo4j import dbConn_inject__sqlite3_neo4j
from neo4j__simple_visual__by_networkx import neo4j_visual__by_networkx
from neo4j__writeVertex_FnCallLog__writeEdge_FnEL import neo4j_recreate___idx__V_FnCallLog__logId, neo4j_recreate___uq__V_FnCallLog__logId, neo4j_writeVFnCallLog_writeEFnEL_whenTraverseSq3FnCallId
from sqlite3_basic_Q_fnCallLog import queryFnCallLogTmPntMaxMin
from config import sqlite3_dbFilePath,neo4jDB_default


def fridaLog_to_sqlite3_to_neo4j(sq3dbConn:sqlite3.Connection,neo4j_sess:neo4j.Session
    # ,neo4j_dbDriver:neo4j.Driver # dbConn_inject__sqlite3_neo4j.py 中 要不要给neo4j_dbDriver是有待考虑的
    ) ->int :

## torch函数调用日志文件(frida日志文件) 装入 sqlite3 
    from fridaLog__sqlite3_writeTabFnSym import sq3_wTab_FnSym
    from fridaLog__sqlite3_writeTabFnCallLog import sq3_wTab_FnCallLog
### 写 表 FnSym
    sq3_wTab_FnSym(sq3dbConn)
###  写 表FnCallLog
    sq3_wTab_FnCallLog(sq3dbConn)
### 提交、关闭sqlite3数据库
    sq3dbConn.commit()

## 找进出不平衡的fnCallId
    from neo4j__writeVertex_FnCallLog__writeEdge_FnEL import neo4j_del_v_e
    from sqlite3_qeury_notBalanced_fnCallIdLs_tmPntLs import qeury_notBalanced_fnCallIdLs_tmPntLs,sq3_move_notBalanced_fnCallCallLog
### 找到 不平衡的fnCallId列表 和 不平衡的 TmPnt列表
    notBalancedFnCallIdLs, notBalancedTmPntLs=qeury_notBalanced_fnCallIdLs_tmPntLs(sq3dbConn)
### 删除不平衡的fnCallId的记录行(移到他表)
    sq3_move_notBalanced_fnCallCallLog(sq3dbConn,notBalancedFnCallIdLs)

## neo4j 社区版 安装、启动
#  neo4j_community_install_boot.md

## 写 neo4j 顶点(日志行号）、边（同fnCallId的进和出） 
### python连接neo4j
### 删除现有顶点、边
    neo4j_del_v_e(neo4j_sess)
### neo4j创建索引
    # neo4j重建索引 V_FnCallLog.logId
    neo4j_recreate___idx__V_FnCallLog__logId(neo4j_sess)
### neo4j创建unique约束
    # neo4j重建unique约束 V_FnCallLog.logId
    neo4j_recreate___uq__V_FnCallLog__logId(neo4j_sess)
### 遍历fnCallId过程中写neo4j顶点、边
    neo4j_writeVFnCallLog_writeEFnEL_whenTraverseSq3FnCallId(sq3dbConn,notBalancedFnCallIdLs,neo4j_sess)


##  写 neo4j 边（时刻点 到 下一个 时刻点） 
### 按照tmPnt查询出 调用日志
### 最大时刻点、最小时刻点
    tmPnt_max:int; tmPnt_min:int
    tmPnt_max,tmPnt_min=queryFnCallLogTmPntMaxMin(sq3dbConn)
    #  from_tmPnt 取值范围为 区间[tmPnt_min,tmPnt_max-1]
    #  to_tmPnt 取值范围为 区间[tmPnt_min+1,tmPnt_max]
### 跳过不平衡的 to_tmPnt
# 遍历 时刻点TmPnt
    neo4j_writeVFnCallLog_writeEFnEL_whenTraverseSq3FnCallId(
sq3dbConn,  neo4j_sess,
notBalancedTmPntLs,
notBalancedFnCallIdLs,
tmPnt_max,tmPnt_min,
)
    
## 简易可视化neo4j图（以networkx）
    # pip install networkx matplotlib

#### 可视化
    neo4j_visual__by_networkx(neo4j_sess)

    return 0



if __name__=="__main__":
    fnCallLogCnt:int = dbConn_inject__sqlite3_neo4j(sqlite3_dbFilePath, neo4jDB_default, func=fridaLog_to_sqlite3_to_neo4j)