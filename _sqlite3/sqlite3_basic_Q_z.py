#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 为了方便frida_js人工确定不重要函数，而 打印 大于1万次调用的函数们
#【术语】 
#【备注】 
#【术语】 


import sqlite3
from sqlite3_basic_Q   import sq3Q_2Dcts
from sqlite3_basic_func import sq3DU


#大于1万次调用的函数们
sql_t_FnCallLog_query_fnGt1WCall="""
select * from 
(select fnAdr, count(fnAdr) as logCnt from t_FnCallLog group by fnAdr HAVING logCnt>10000 order by logCnt desc ) tFn1W
join t_FnSym tSym on tFn1W.fnAdr=tSym.address
"""
    
#打印 大于1万次调用的函数们
def sq3_printFnGt1WCall(sq3dbConn:sqlite3.Connection)->None:
    _rowLs=sq3dbConn.execute(sql_t_FnCallLog_query_fnGt1WCall).fetchall()
    print("大于1万次调用的函数们",_rowLs)
    return


#按进程Id、线程Id分组统计日志行数
sql_t_FnCallLog__grp_rowCnt__processId_curThreadId="""
select processId,curThreadId, count(logId) as logCnt from t_FnCallLog group by processId,curThreadId  order by logCnt desc 
"""
#删除非该进程id、线程id的日志
sql_t_FnCallLog__del_by__not__processId_curThreadId="""
delete from t_FnCallLog where  (processId,curThreadId)!=({processId},{curThreadId})
"""
#打印（进程id、线程id）列表，询问保留哪一个？，执行删除
def sq3_askKeepWhichProcessIdThreadId(sq3dbConn:sqlite3.Connection)->int:
    rowLs=sq3Q_2Dcts(sq3dbConn,sql_t_FnCallLog__grp_rowCnt__processId_curThreadId)
    idx_str=input("input processId_ThreadId to keep:")
    idx=int(idx_str)
    row_keep=rowLs(idx)
    sqlTxt=sql_t_FnCallLog__del_by__not__processId_curThreadId.format(processId=row_keep['processId'],curThreadId=row_keep['curThreadId'])
    rowCnt_del:int=sq3DU(sq3dbConn,sqlTxt)
    return rowCnt_del
