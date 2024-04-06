#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 找进出不平衡的fnCallId
#【术语】 
#【备注】 
#【术语】 

import typing
import sqlite3

from sqlite3_basic_DU_inInts import sq3DU_inInts
from sqlite3_basic_Q_inInts import sq3Q_inInts, sq3Q_inInts_2Dcts
from sqlite3_basic_func import sq3Q
from util_basic import lsIsEmpty
## 找进出不平衡的fnCallId



#  以前用spark也找出过[sql方式找进出不平衡的fncallid](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/raw/tag/%E5%AE%8C%E5%A4%87%E4%BE%8B%E5%AD%90/spark3.5.0_pyspark3.5.0_sql%E4%B8%BA%E4%B8%BB/spark_demo_pyspark.ipynb#sql%E6%96%B9%E5%BC%8F%E6%89%BE%E8%BF%9B%E5%87%BA%E4%B8%8D%E5%B9%B3%E8%A1%A1%E7%9A%84fncallid)，　可以作为这里的对比

### 找到 不平衡的fnCallId列表 和 不平衡的 TmPnt列表
def qeury_notBalanced_fnCallIdLs_tmPntLs(sq3dbConn:sqlite3.Connection):
    fnCallIdLs=sq3Q(sq3dbConn,"select fnCallId,count(*) cnt from t_FnCallLog group by fnCallId having cnt=1","fnCallId")
    if lsIsEmpty(fnCallIdLs)  :
        print("无不平衡的fnCallLog")
        return None,None
        
    print("找到不平衡的fnCallIdLs",fnCallIdLs)

    #找到不平衡的FnCallLog列表 _clLogLs_nBl

    # fnCallIdStrLs=joinInts(fnCallIdLs) ; tmPntLs=sq3Q(sq3dbConn,f"select  *  from t_FnCallLog where fnCallId in ({fnCallIdStrLs})","tmPnt")
    #上一行与下一行 等价
    tmPntLs=sq3Q_inInts(sq3dbConn,"select  *  from t_FnCallLog where fnCallId in ({lsVar})",fnCallIdLs,"tmPnt")

    print("找到不平衡的tmPntLs=",tmPntLs)

    return fnCallIdLs,tmPntLs



### _ 找到不平衡的FnSym列表 
def sq3_query_notBalanced_fnSymLs(sq3dbConn:sqlite3.Connection):
    _fnAdrLs=sq3Q_inInts(sq3dbConn, "select  fnAdr from t_FnCallLog where fnCallId in ( {lsVar} )", notBalancedFnCallIdLs, "fnAdr")
    _symLs_nBl=sq3Q_inInts_2Dcts(sq3dbConn, "select  * from t_FnSym where address in ( {lsVar} )", _fnAdrLs )

    print("找到不平衡的FnSym列表 _symLs_nBl=",_symLs_nBl)


    # 找到不平衡的FnSym列表 _symLs_nBl= [{'address': '0x5555555659e0', 'name': '_start', 'moduleName': 'simple_nn.elf', 'fileName': '', 'lineNumber': 0, 'column': 0}]


### 删除不平衡的fnCallId的记录行(移到他表)
def sq3_move_notBalanced_fnCallCallLog(sq3dbConn:sqlite3.Connection,notBalancedFnCallIdLs:typing.List[int]):
    #  不平衡的fnCallId列表 移动到 表t_FnCallLog_notBalanced
    _rowCnt_insert=sq3DU_inInts(sq3dbConn, 
    "insert into t_FnCallLog_notBalanced select * from t_FnCallLog where fnCallId in ( {lsVar} )",notBalancedFnCallIdLs)

    #  删除不平衡的fnCallId列表
    _rowCnt_delete=sq3DU_inInts(sq3dbConn,"delete from t_FnCallLog where fnCallId in ( {lsVar} )",notBalancedFnCallIdLs)
    assert _rowCnt_insert == _rowCnt_delete
    print(f"notBalancedFnCallIdLs={notBalancedFnCallIdLs}, 移动不平衡记录行数 {_rowCnt_insert}")


    # notBalancedFnCallIdLs=[1], 移动不平衡记录行数 1




    # #现在应该没有不平衡的fnCallId了
    # assert lsIsEmpty( qeury_notBalanced_fnCallIdLs_tmPntLs()[0] )


