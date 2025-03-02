#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 Sq3Log==Sq3FnCallLog, wrt==write,whn==when,trv==Traverse
#【备注】 
#【术语】 

import signal
import sys
import typing
import sqlite3
import neo4j
from neo4j import Driver

from db_conn_inject.dbConn_inject__sqlite3_neo4j import dbConn_inject__sqlite3_neo4j
from neo4j__simple_visual__by_networkx import neo4j_visual__by_networkx
from neo4j__writeEdge_NxtTmPnt import neo4j_wrtENxtTmPnt_whnTrvSq3Log
from neo4j__writeVertex_FnCallLog__writeEdge_FnEL import  neo4j_recreate___uq__V_FnCallLog__logId, neo4j_wrtVFnCallLog_EFnEL_whnTrvSq3Log
from sqlite3_basic_Q_fnCallLog import queryFnCallLogTmPntMaxMin
from config import sqlite3_dbFilePath,neo4jDB_default
from util_file import unlink_verbose


def fridaLog_to_sqlite3_to_neo4j(sq3dbConn:sqlite3.Connection,neo4j_sess:neo4j.Session
    # ,neo4j_dbDriver:neo4j.Driver # dbConn_inject__sqlite3_neo4j.py 中 要不要给neo4j_dbDriver是有待考虑的
    ) ->int :

## torch函数调用日志文件(frida日志文件) 装入 sqlite3 
    from fridaLog__sqlite3_writeTabFnSym import sq3_wTab_FnSym
    from fridaLog__sqlite3_writeTabFnCallLog import sq3_wTab_FnCallLog
    from sqlite3_Q_printFnGt1WCall import sq3Q_printFnGt1WCall
    from sqlite3_QD_askKeepWhichProcessIdThreadId import sq3QD_askKeepWhichProcessIdThreadId
## 只需要存入sqlite3 （不需要存入neo4j）么？
    import os
    fridaLog_to_sqlite3_only:bool=os.environ.get("envVar__analyze_by_graph__fridaLog_to_sqlite3_only","Empty")=="True"

### 写 表 FnSym
    sq3_wTab_FnSym(sq3dbConn)
###  写 表FnCallLog
    sq3_wTab_FnCallLog(sq3dbConn)
###  打印大于1万次调用的函数们（方便返工修改frida_js以跳过大量调用函数）
    sq3Q_printFnGt1WCall(sq3dbConn)
## 只需要存入sqlite3 （不需要存入neo4j）么？
    if fridaLog_to_sqlite3_only:
###    提交、关闭sqlite3数据库
            sq3dbConn.commit()
###    退出
            return -1

###  打印（进程id、线程id）列表，询问保留哪一个？，执行删除
    sq3QD_askKeepWhichProcessIdThreadId(sq3dbConn)
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
    # neo4j重建索引 V_FnCallLog.logId （和uniqe约束重复了，不再单独创建索引）
### neo4j创建unique约束
    # neo4j重建unique约束 V_FnCallLog.logId
    neo4j_recreate___uq__V_FnCallLog__logId(neo4j_sess)
### 遍历fnCallId过程中写neo4j顶点、边
    neo4j_wrtVFnCallLog_EFnEL_whnTrvSq3Log(sq3dbConn,notBalancedFnCallIdLs,neo4j_sess)


##  写 neo4j 边（时刻点 到 下一个 时刻点） 
### 按照tmPnt查询出 调用日志
### 最大时刻点、最小时刻点
    tmPnt_max:int; tmPnt_min:int
    tmPnt_max,tmPnt_min=queryFnCallLogTmPntMaxMin(sq3dbConn)
    #  from_tmPnt 取值范围为 区间[tmPnt_min,tmPnt_max-1]
    #  to_tmPnt 取值范围为 区间[tmPnt_min+1,tmPnt_max]
### 跳过不平衡的 to_tmPnt
# 遍历 时刻点TmPnt
    neo4j_wrtENxtTmPnt_whnTrvSq3Log(
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

#退出信号处理：退出前执行清理
def clean_before_exit(_signal:signal.Signals, frame):
    print(f'收到信号{_signal},执行清理逻辑后正常退出')
    unlink_verbose(sqlite3_dbFilePath)
    sys.exit(0)


if __name__=="__main__":
    
    #linux进程退出信号处理
    signal.signal(  signal.SIGINT  , clean_before_exit)
    signal.signal(  signal.SIGPIPE, clean_before_exit)
    
    fnCallLogCnt:int = dbConn_inject__sqlite3_neo4j(sqlite3_dbFilePath, neo4jDB_default, func=fridaLog_to_sqlite3_to_neo4j)