
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 torch函数调用日志文件(frida日志文件) 装入 sqlite3 / 写 表FnCallLog
#【术语】 
#【备注】 
#【术语】 

import sqlite3
import typing
from config import FnCallLogFP
from iterLineOfFile import iterLineF
from util_path import assertFilePathExisted

## torch函数调用日志文件(frida日志文件) 装入 sqlite3 

###  写 表FnCallLog
def sq3_wTab_FnCallLog(sq3dbConn:sqlite3.Connection):
    fnCallLogFP:str=assertFilePathExisted(FnCallLogFP)
    print("从表t_FnCallLog删除行数 ",sq3dbConn.execute("delete from t_FnCallLog").rowcount)    
    LogLineCnt:int=iterLineF(fnCallLogFP,sq3dbConn,LineFunc=sq3_insert_t_FnCallLog)
    # 从表t_FnCallLog删除行数  0
    # 即将处理第0行日志
    # 即将处理第500000行日志
    # 即将处理第1000000行日志
    # 即将处理第1500000行日志
    # 已处理,文件/fridaAnlzAp/frida_js/frida-out-Pure-1712123780.log共1619593行


#### sql语句模板
sqlTmpl_t_FnCallLog_insert=f"INSERT INTO t_FnCallLog (logId,tmPnt,processId,curThreadId,direct,fnAdr,fnCallId,fnSymId) VALUES (?,?,?,?,?,?,?,?)"

#### 行回调函数中执行插入
def sq3_insert_t_FnCallLog(lnNum:int,ln:str,sq3dbConn:sqlite3.Connection):
    try:
        sq3dbConn.execute(sqlTmpl_t_FnCallLog_insert,[ ln['logId'],ln['tmPnt'],ln['processId'], ln['curThreadId'],ln['direct'],ln['fnAdr'],ln['fnCallId'],ln['fnSym']['address'] ])
    except (KeyError, ValueError) as e:
        print("出错行为",ln)
        import traceback
        traceback.print_exception(e)
        raise e
        

#### 开发调试用语句
# iterLogF(TorchFnCallLogFP,FirstLineFunc=sq3_insert_t_FnCallLog)
# sq3dbConn.execute("select count(*) from t_FnCallLog").fetchall()


### 提交、关闭sqlite3数据库
# sq3dbConn.commit()
# sq3dbConn.close()


