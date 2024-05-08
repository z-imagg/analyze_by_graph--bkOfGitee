#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 sqlite3查询函数
#【术语】 
#【备注】 
#【术语】 

import sqlite3
import typing

from sqlite3_basic_func import sq3Rows2Dcts, sq3RowsPrint
from util_basic import lsIsEmpty



## sqlite3查询函数

### sq3Q_2Dcts: sqlite3执行sql查询 并 转为字典列表
def sq3Q_2Dcts(sq3dbConn,sqlTxt):
    # print(sqlTxt)
    rowLs=sq3dbConn.execute(sqlTxt).fetchall()
    if lsIsEmpty(rowLs): return None
    return sq3Rows2Dcts(rowLs)

##调用举例
# sq3Q_2Dcts(sq3dbConn,"select  tmPnt,fnCallId from t_FnCallLog  limit 2 "     )
# [{'tmPnt': 1, 'fnCallId': 1}, {'tmPnt': 2, 'fnCallId': 2}]


#打印 sql语句查询结果
def sq3Q_print(sq3dbConn:sqlite3.Connection,sqlTxt:str,title:str)->typing.List[sqlite3.Row]:
    _rowLs:typing.List[sqlite3.Row]=sq3dbConn.execute(sqlTxt).fetchall()
    sq3RowsPrint(_rowLs,title)
    return _rowLs
