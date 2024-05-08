#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 为了方便frida_js人工确定不重要函数，而 打印 大于1万次调用的函数们
#【术语】 
#【备注】 
#【术语】 


import typing
import sqlite3
from sqlite3_basic_Q   import sq3Q_2Dcts, sq3Q_print
from sqlite3_basic_func import sq3DU
from sqlite3_basic_func import sq3RowsPrint
import pyinputplus

#大于1万次调用的函数们
sql_t_FnCallLog_query_fnGt1WCall="""
select * from 
(select fnAdr, count(fnAdr) as logCnt from t_FnCallLog group by fnAdr HAVING logCnt>10000 order by logCnt desc ) tFn1W
join t_FnSym tSym on tFn1W.fnAdr=tSym.address
"""
    
#打印 大于1万次调用的函数们
def sq3_printFnGt1WCall(sq3dbConn:sqlite3.Connection)->None:
    sq3Q_print(sq3dbConn,sql_t_FnCallLog_query_fnGt1WCall,"大于1万次调用的函数们")
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
    _rowLs:typing.List[sqlite3.Row]=sq3Q_print(sq3dbConn,sql_t_FnCallLog__grp_rowCnt__processId_curThreadId,"<进程id、线程id>列表")
    _rowCnt:int=_rowLs.__len__()
    if _rowCnt <= 1:
        print(f"<进程id、线程id>只有{_rowCnt}个，无需选择,直接返回")
        return 0
    
    _min_rowK:int=0
    _max_rowK:int=_rowCnt-1
    _promptTxt:str=f"保留哪个<进程id、线程id>？请输入 _rowK '{_min_rowK}~{_max_rowK}' : "
    rowK_keep:int=pyinputplus.inputInt(prompt=_promptTxt,min=_min_rowK,max=_max_rowK)
    row_keep=_rowLs[rowK_keep]
    processId_keep:int=row_keep['processId']
    curThreadId_keep:int=row_keep['curThreadId']
    sqlTxt_del=sql_t_FnCallLog__del_by__not__processId_curThreadId.format(processId=processId_keep,curThreadId=curThreadId_keep)
    rowCnt_del:int=sq3DU(sq3dbConn,sqlTxt_del)
    return rowCnt_del


if __name__=="__main__":
    #测试代码
    sq_db_fp="/home/z/FnCallLog.db"
    sq3dbConn:sqlite3.Connection = sqlite3.connect(sq_db_fp)
    #  设置sqlite3.connect.execute.fetchall返回字典列表而非tuple列表
    origin_sq3dbConn_row_factory=sq3dbConn.row_factory #先备份
    sq3dbConn.row_factory = sqlite3.Row #再修改
    sq3_printFnGt1WCall(sq3dbConn)
    sq3_askKeepWhichProcessIdThreadId(sq3dbConn)