#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 打印大于1万次调用的函数们（方便返工修改frida_js以跳过大量调用函数）
#【术语】 
#【备注】 
#【术语】 


import typing
import sqlite3
from sqlite3_basic_Q   import  sq3Q_print
from sqlite3_basic_func import sq3DU
import pyinputplus



#按进程Id、线程Id分组统计日志行数
sql_t_FnCallLog__grp_rowCnt__processId_curThreadId="""
select processId,curThreadId, count(logId) as logCnt from t_FnCallLog group by processId,curThreadId  order by logCnt desc 
"""
#删除非该进程id、线程id的日志
sql_t_FnCallLog__del_by__not__processId_curThreadId="""
delete from t_FnCallLog where   (processId,curThreadId) != ({processId},{curThreadId})
"""
#打印（进程id、线程id）列表，询问保留哪一个？，执行删除
def sq3QD_askKeepWhichProcessIdThreadId(sq3dbConn:sqlite3.Connection)->int:
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
    print(f"保留<进程id、线程id>为<{processId_keep},{curThreadId_keep}>,引起删除t_FnCallLog记录行数为{rowCnt_del}. sqlTxt_del=[{sqlTxt_del}]")
    return rowCnt_del

