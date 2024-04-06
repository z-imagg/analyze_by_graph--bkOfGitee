#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 入口
#【术语】 
#【备注】 
#【术语】 

import typing

## torch函数调用日志文件(frida日志文件) 装入 sqlite3 
from fridaLog__sqlite3_reinitDbTabDef import reinit_sq3_db_tabDef 
from fridaLog__sqlite3_writeTabFnSym import sq3_wTab_FnSym
from fridaLog__sqlite3_writeTabFnCallLog import sq3_wTab_FnCallLog
sq_db_fp='./FnCallLog.db'
### 重初始化sqlite3数据库、表结构
sq3dbConn=reinit_sq3_db_tabDef(sq_db_fp)
### 写 表 FnSym
sq3_wTab_FnSym(sq3dbConn)
###  写 表FnCallLog
sq3_wTab_FnCallLog(sq3dbConn)
### 提交、关闭sqlite3数据库
sq3dbConn.commit()
# sq3dbConn.close()

## 找进出不平衡的fnCallId
from sq3_qeury_notBalanced_fnCallIdLs_tmPntLs import qeury_notBalanced_fnCallIdLs_tmPntLs,sq3_move_notBalanced_fnCallCallLog
### 找到 不平衡的fnCallId列表 和 不平衡的 TmPnt列表
notBalancedFnCallIdLs, notBalancedTmPntLs=qeury_notBalanced_fnCallIdLs_tmPntLs()
### 删除不平衡的fnCallId的记录行(移到他表)
sq3_move_notBalanced_fnCallCallLog()