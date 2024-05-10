#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 torch函数调用日志文件(frida日志文件) 装入 sqlite3 / 重初始化sqlite3数据库、表结构
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from pathlib import Path
import sqlite3

from util_file import unlink_verbose

##  torch函数调用日志文件(frida日志文件) 装入 sqlite3 

### 重初始化sqlite3数据库、表结构

def reinit_sq3_db_tabDef(sq_db_fp:str)->sqlite3.Connection: 


    #### 删除已有的sqlite3数据库文件
    Path(sq_db_fp).unlink(missing_ok=True)
    unlink_verbose(sq_db_fp)

    #### 创建sqlite3数据库文件
    # sq3dbConn = sqlite3.connect(':memory:')
    sq3dbConn:sqlite3.Connection = sqlite3.connect(sq_db_fp)

    #  设置sqlite3.connect.execute.fetchall返回字典列表而非tuple列表
    origin_sq3dbConn_row_factory=sq3dbConn.row_factory #先备份
    sq3dbConn.row_factory = sqlite3.Row #再修改

    #sqlite3 不需要游标cursor,直接用连接执行语句
    # sq3Cursr = sq3dbConn.cursor()

    print(origin_sq3dbConn_row_factory)
    # None

    #### 创建表t_FnSym
    #  2+8*2 == 18
    sq3dbConn.execute("drop TABLE if exists t_FnSym ")
    sq3dbConn.execute("""
    CREATE TABLE t_FnSym (
    address char(18) PRIMARY KEY,  
    name varchar(256), 
    moduleName  varchar(32), 
    fileName  varchar(256), 
    lineNumber integer,
    column integer
    )
    """)

    #### 创建表t_FnCallLog
    sq3dbConn.execute("drop TABLE if exists t_FnCallLog ")
    sq3dbConn.execute("""
    CREATE TABLE t_FnCallLog (
    logId integer PRIMARY KEY, 
    tmPnt integer,
    processId integer,
    curThreadId integer, 
    direct short, 
    fnAdr char(18),
    fnCallId integer,
    fnSymId char(18)
    )
    """)

    #### 创建索引
    #  有按字段t_FnCallLog.fnCallId查询，因此该字段得有索引
    sq3dbConn.execute("""
    CREATE INDEX idx__t_FnCallLog__fnCallId ON t_FnCallLog (fnCallId)
    """)
    #  有按字段t_FnCallLog.tmPnt查询，因此该字段得有索引
    sq3dbConn.execute("""
    CREATE INDEX idx__t_FnCallLog__tmPnt ON t_FnCallLog (tmPnt)
    """)

    #  执行删除非该 (processId,curThreadId)时候，需要按字段t_FnCallLog.processId_curThreadId执行删除，因此该两字段得有索引
    sq3dbConn.execute("""
    CREATE INDEX idx__t_FnCallLog__processId_curThreadId ON t_FnCallLog (processId,curThreadId)
    """)
    
    #### 创建表t_FnCallLog_notBalanced
    #  创建表t_FnCallLog_notBalanced 用于存放 不平衡的 函数调用日志
    #  t_FnCallLog_notBalanced 的 结构 ==  t_FnCallLog 的 结构
    sq3dbConn.execute("drop TABLE if exists t_FnCallLog_notBalanced ")
    sq3dbConn.execute("""
    CREATE TABLE t_FnCallLog_notBalanced as select * from t_FnCallLog where false
    """)

    return sq3dbConn


