#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 基础sqlite3函数
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from basic_tool import lsIsEmpty


## 基础sqlite3函数

### sq3Rows1Field: 提取 sqlite3.Row 们 中的一个字段
def sq3Rows1Field(_rowLs:typing.List[sqlite3Row],fieldName:str)->typing.List[typing.Any]:
    fldValLs=[ r[fieldName] for r in _rowLs ]
    return fldValLs

### sq3Q: sqlite3执行sql查询 并 提取字段
def sq3Q(sq3dbConn,sqlTxt,fieldName):
    rowLs=sq3dbConn.execute(sqlTxt).fetchall()
    if lsIsEmpty(rowLs): return None
    return sq3Rows1Field(rowLs,fieldName)

### sq3DU: sqlite3执行sql删改 并 返回影响行数
def sq3DU(sq3dbConn,sqlTxt):
    # print(sqlTxt)
    rowCnt=sq3dbConn.execute(sqlTxt).rowcount
    return rowCnt

#调用举例
# sq3DU(sq3dbConn,"delete  from t_FnCallLog  where fnCallId < -1"     )
# 0

### sq3Rows2Dcts: sqlite3.Row转为字典Dict
# 由于　sqlite3.Row没有合理的__str__, 因此　要转为Dict

def sq3Rows2Dcts(_rowLs:typing.List[sqlite3Row])->typing.List[typing.Dict]:
    dctLs=[ {**r} for r in _rowLs ]
    return dctLs


