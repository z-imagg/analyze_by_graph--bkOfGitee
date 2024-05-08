#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 基础sqlite3函数
#【术语】 
#【备注】 
#【术语】 


import sqlite3
from sqlite3 import Row as sqlite3Row
import typing

from util_basic import lsIsEmpty


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
def sq3DU(sq3dbConn:sqlite3.Connection,sqlTxt):
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

# 打印记录列表
def sq3RowsPrint(_rowLs:typing.List[sqlite3Row],title:str)->None:
    #若空结果集合，则提示并直接返回
    if lsIsEmpty(_rowLs): 
        print(f"空结果集[{title}]")
        return
    
    
    print(f"打印结果集[{title}]")
        
    #字段名列表
    # 取第0条记录的字段名列表
    row0:sqlite3Row=_rowLs[0]
    fieldNameLs:typing.List[str]=row0.keys()
    #打印字段名列表
    fieldNamesTxt:str=",".join(fieldNameLs)
    print(f"_rowK;{fieldNamesTxt}")
    
    #打印记录列表
    for k,rowK in enumerate( _rowLs ):
        #打印第k条记录行
        rowK_strArr=[str(valI) for valI in rowK]
        rowKTxt:str=",".join(rowK_strArr)
        print(f"{k};{rowKTxt}")
    
    return

