#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 torch函数调用日志文件(frida日志文件) 装入 sqlite3 / 写 表 FnSym
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from pathlib import Path
import sqlite3
from fridaLog_fullPath_get import getLogFullPath
from iterLineOfFile import iterLineF

## torch函数调用日志文件(frida日志文件) 装入 sqlite3 

### 写 表 FnSym
def sq3_wTab_FnSym(sq3dbConn:sqlite3.Connection):
    fnCallLogFP:str=getLogFullPath()
    print("从表t_FnSym删除行数 ",sq3dbConn.execute("delete from t_FnSym").rowcount)
    iterLineF(fnCallLogFP,LineFunc=sq3_insert_t_FnSym)
    # 从表t_FnSym删除行数  0
    # 即将处理第0行日志
    # 即将处理第500000行日志
    # 即将处理第1000000行日志
    # 即将处理第1500000行日志
    # 已处理,文件/fridaAnlzAp/frida_js/frida-out-Pure-1712123780.log共1619593行
    # 1619593


#### sql语句模板
sqlTmpl_t_FnSym_query=f"select address, name,moduleName,fileName,lineNumber,column from t_FnSym where  address = ?"
sqlTmpl_t_FnSym_insert=f"INSERT INTO t_FnSym (address, name,moduleName,fileName,lineNumber,column) VALUES (?,?,?,?,?,?)"


#### 行回调函数中执行插入
def assertRowEqFnSym(r,fnSym):
    assert  \
r["address"]==fnSym["address"] and \
r["name"]==fnSym["name"] and \
r["moduleName"]==fnSym["moduleName"] and \
r["fileName"]==fnSym["fileName"] and \
r["lineNumber"]==fnSym["lineNumber"] and \
r["column"]==fnSym["column"], f"断言 frida_js项目中 每次 写入的 从DebugSymb中按地址读取出来的 fnSym 是 不变的, rowInSqlite3Tab={r},fnSym={fnSym}"

def sq3_insert_t_FnSym(lnNum:int,ln:str,sq3dbConn:sqlite3.Connection):
    fnSym=ln['fnSym'] 
    try:
        row_ls=sq3dbConn.execute(sqlTmpl_t_FnSym_query,[ fnSym['address']  ]).fetchall()
        #若已经有fnSym,则跳过（即不必再插入）
        if row_ls is not None and len(row_ls) > 0:
            #下面断言意义不大 是在验证 sqlite3的主键 是否 真唯一
            assert len(row_ls) == 1, "断言失败，一个地址只能有一个fnSym"  
            #下面断言意义不大 是在验证 frida_js项目中 每次 写入的 从DebugSymb中按地址读取出来的 fnSym 是 不变的
            r=row_ls[0] ; assertRowEqFnSym(r,fnSym)
            return

        #torch源文件路径前的无意义部分换成相对路径
        fileName=fnSym['fileName'].replace('/home/z/torch-repo/pytorch/', './')
        
        sq3dbConn.execute(sqlTmpl_t_FnSym_insert,
[ fnSym['address'], fnSym['name'], fnSym['moduleName'], fnSym['fileName'], fnSym['lineNumber'], fnSym['column'] ])
    except (KeyError, ValueError) as e:
        print("出错行为",ln)
        import traceback
        traceback.print_exception(e)
        raise e



#### 开发调试用语句
# iterLogF(TorchFnCallLogFP,FirstLineFunc=sq3_insert_t_FnSym)
# sq3dbConn.execute(sqlTmpl_t_FnSym_query,[ '0x7ffff61cdd3c'  ]).fetchall()