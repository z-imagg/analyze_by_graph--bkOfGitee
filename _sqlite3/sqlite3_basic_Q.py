#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 sqlite3查询函数
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from sqlite3_basic_func import sq3Rows2Dcts
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
