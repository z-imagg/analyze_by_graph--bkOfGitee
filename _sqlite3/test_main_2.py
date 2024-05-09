#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 测试main
#【术语】 
#【备注】 打印大于1万次调用的函数们（方便返工修改frida_js以跳过大量调用函数）， 询问保留哪一个<进程id、线程id>
#【术语】 


import sqlite3

from sqlite3_basic_Q_fnCallLog import queryFnCallLogByTmPnt


if __name__=="__main__":
    #测试代码
    sq_db_fp="/home/z/0509-FnCallLog.db"
    sq3dbConn:sqlite3.Connection = sqlite3.connect(sq_db_fp)
    to_tmPnt=3
    toLog=queryFnCallLogByTmPnt(sq3dbConn,to_tmPnt)
    # sq3dbConn.commit()
    sq3dbConn.close()