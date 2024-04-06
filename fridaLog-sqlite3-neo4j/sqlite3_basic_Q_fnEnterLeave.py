#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 按照fnCallId查询出 函数进入、函数离开 日志
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

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
def queryFnEnterLeave(sq3dbConn,fnCallId:int):
    _rowLs=sq3dbConn.execute(sqlTmpl_t_FnCallLog_query_by_fnCallId, [fnCallId]).fetchall()
    # print(_rowLs)
    assert len(_rowLs) == 2
    ls_1=list(filter(lambda r:r["direct"]==Direct.EnterFn, _rowLs)); assert len(ls_1) == 1
    ls_2=list(filter(lambda r:r["direct"]==Direct.LeaveFn, _rowLs)); assert len(ls_1) == 1
    fnEnter=ls_1[0]
    fnLeave=ls_2[0]
    
    fnEnter,fnLeave=_rowLs
    return fnEnter,fnLeave