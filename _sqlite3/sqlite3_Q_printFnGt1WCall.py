#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 打印 大于1万次调用的函数们
#【术语】 
#【备注】 为了方便frida_js人工确定不重要函数
#【术语】 


import typing
import sqlite3
from sqlite3_basic_Q   import  sq3Q_print

#大于1万次调用的函数们
sql_t_FnCallLog_query_fnGt1WCall="""
select * from 
(select fnAdr, count(fnAdr) as logCnt from t_FnCallLog group by fnAdr HAVING logCnt>10000 order by logCnt desc ) tFn1W
join t_FnSym tSym on tFn1W.fnAdr=tSym.address
"""
    
#打印 大于1万次调用的函数们
def sq3Q_printFnGt1WCall(sq3dbConn:sqlite3.Connection)->None:
    sq3Q_print(sq3dbConn,sql_t_FnCallLog_query_fnGt1WCall,"大于1万次调用的函数们")
    return



