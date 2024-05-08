#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 测试main
#【术语】 
#【备注】 
#【术语】 


import sqlite3

from sqlite3_basic_Q_z import sq3QD_askKeepWhichProcessIdThreadId, sq3Q_printFnGt1WCall


if __name__=="__main__":
    #测试代码
    sq_db_fp="/home/z/FnCallLog.db"
    sq3dbConn:sqlite3.Connection = sqlite3.connect(sq_db_fp)
    #  设置sqlite3.connect.execute.fetchall返回字典列表而非tuple列表
    origin_sq3dbConn_row_factory=sq3dbConn.row_factory #先备份
    sq3dbConn.row_factory = sqlite3.Row #再修改
    sq3Q_printFnGt1WCall(sq3dbConn)
    sq3QD_askKeepWhichProcessIdThreadId(sq3dbConn)
    sq3dbConn.commit()
    sq3dbConn.close()