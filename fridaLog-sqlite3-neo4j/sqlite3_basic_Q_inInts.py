#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 sqlite3查询函数:in整数们
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from basic_sqlite3_Q import sq3Q_2Dcts
from basic_sqlite3_func import sq3Q
from basic_tool import joinInts



## sqlite3查询函数:in整数们

### sq3Q_inInts_2Dcts: sqlite3执行sql查询 携带in整数列表条件 结果转字典



def sq3Q_inInts_2Dcts(sq3dbConn,sqlInIntLs,intLs):
    intStrLs=joinInts(intLs)
    sqlTxt=sqlInIntLs.format(lsVar=intStrLs)
    return sq3Q_2Dcts(sq3dbConn,sqlTxt)



### sq3Q_inInts: sqlite3执行sql查询 携带in整数列表条件 并 提取字段



def sq3Q_inInts(sq3dbConn,sqlInIntLs,intLs, fieldName):
    intStrLs=joinInts(intLs)
    sqlTxt=sqlInIntLs.format(lsVar=intStrLs)
    return sq3Q(sq3dbConn,sqlTxt, fieldName)





#调用举例
# sq3Q_inInts(sq3dbConn,"select  *  from t_FnCallLog where fnCallId in ({lsVar}) ",[1,20],"logId"   )
# [1, 8, 36, 37]
