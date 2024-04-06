#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 按照fnCallId查询出 函数进入、函数离开 日志
#【术语】 
#【备注】 
#【术语】 


import sqlite3
import typing

from util_basic import lsIsEmpty

sqlTmpl_t_FnCallLog_query_by_fnCallId="select  *  from t_FnCallLog where fnCallId=?"
#按字段t_FnCallLog.fnCallId查询，因此该字段得有索引

#  http://giteaz:3000/frida_analyze_app_src/frida_js/src/branch/main/DebugSymbolUtil.ts

#  javascript
#  //方向枚举: 函数进入 或 函数离开
#  enum Direct{
#    // 函数进入
#    EnterFn = 1,
#    // 函数离开
#    LeaveFn = 2,
#  }

#方向枚举: 函数进入 或 函数离开
class Direct:
    #函数进入
    EnterFn = 1
    #函数离开
    LeaveFn = 2
    
#按照fnCallId查询出 函数进入、函数离开 日志
def queryFnEnterLeave(sq3dbConn:sqlite3.Connection,fnCallId:int):
    _rowLs=sq3dbConn.execute(sqlTmpl_t_FnCallLog_query_by_fnCallId, [fnCallId]).fetchall()
    # print(_rowLs)
    assert len(_rowLs) == 2
    ls_1=list(filter(lambda r:r["direct"]==Direct.EnterFn, _rowLs)); assert len(ls_1) == 1
    ls_2=list(filter(lambda r:r["direct"]==Direct.LeaveFn, _rowLs)); assert len(ls_1) == 1
    fnEnter=ls_1[0]
    fnLeave=ls_2[0]
    
    fnEnter,fnLeave=_rowLs
    return fnEnter,fnLeave


sqlTmpl_t_FnCallLog_query_by_tmPnt="select  *  from t_FnCallLog where tmPnt=?"
### 按照tmPnt查询出 调用日志
def queryFnCallLogByTmPnt(sq3dbConn:sqlite3.Connection,tmPnt):
    _rowLs=sq3dbConn.execute(sqlTmpl_t_FnCallLog_query_by_tmPnt, [tmPnt]).fetchall()
    # print(_rowLs)
    if lsIsEmpty(_rowLs): return None
    assert len(_rowLs) == 1, "一个时刻点tmPnt只应该有一条调用日志"
    callLog=_rowLs[0]
    
    return callLog


sqlTmpl_t_FnCallLog_tmPnt_min="select  min(tmPnt) tmPnt_min  from t_FnCallLog "
sqlTmpl_t_FnCallLog_tmPnt_max="select  max(tmPnt) tmPnt_max  from t_FnCallLog "
### 查询 最大时刻点、最小时刻点
def queryFnCallLogTmPntMaxMin(sq3dbConn:sqlite3.Connection)->typing.Tuple[int,int]:
    #最小时刻点
    tmPnt_min:int=sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_min).fetchone()["tmPnt_min"]
    #最大时刻点
    tmPnt_max:int=sq3dbConn.execute(sqlTmpl_t_FnCallLog_tmPnt_max).fetchone()["tmPnt_max"]

    
    return (tmPnt_max,tmPnt_min)