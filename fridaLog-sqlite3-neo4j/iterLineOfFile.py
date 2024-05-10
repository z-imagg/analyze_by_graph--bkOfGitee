#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 torch函数调用日志文件(frida日志文件) 按行遍历器
#【术语】 
#【备注】 
#【术语】 

import sqlite3
import typing

## torch函数调用日志文件(frida日志文件) 按行遍历器

#  逐行加载 frida_js生产的日志文件



import typing
import json

from config import FnCallLogFP
#FirstLineFunc 只在开发时用
# LogFP==TorchFnCallLogFP
def iterLineF(LogFP:str,sq3dbConn:sqlite3.Connection,
    LineFunc:typing.Callable[[int,str,sqlite3.Connection],None]=None,
    FirstLineFunc_onlyDevelop:typing.Callable[[int,str,sqlite3.Connection],None]=None #开发调试用的 只回调第一行 为了节省时间
)->int:
    LogF= open(LogFP,"r")

    hasFrtLnFunc=FirstLineFunc_onlyDevelop is not None
    hasLineFunc= LineFunc is not None

    #如果指定了FirstLineFunc, 则表明现在是开发状态,只看第一行后结束循环
    if hasFrtLnFunc and not hasLineFunc:
        k,lnK=0,LogF.readline()
        ln0_json=json.loads(lnK)
        FirstLineFunc_onlyDevelop(k,ln0_json,sq3dbConn)
    elif hasLineFunc:        
        for k,lnK in enumerate( LogF ):
            if k % 500000 == 0 :  print(f"即将处理第{k}行日志")
    
            lnK_json=json.loads(lnK)
    
            #对每行 都执行回调行数
            LineFunc(k,lnK_json,sq3dbConn)
    else:
        raise Exception(f"函数 iterLogF 条件混乱, hasFrtLnFunc={hasFrtLnFunc},hasLineFunc={hasLineFunc}")


    #关闭日志文件
    LogF.close()
    
    lineCnt:int=k+1
    print(f"已处理,文件{LogFP}共{lineCnt}行")

    #返回日志文件中行个数
    return lineCnt
    



if __name__ == "__main__":
    #显示最后一行的结构
    lnEnd_json=None
    def assignEveryLn(k,lnK_json):
        global lnEnd_json
        lnEnd_json=lnK_json
            
    
    TorchFnCallLogFP=FnCallLogFP
    iterLineF(TorchFnCallLogFP,assignEveryLn)

    print("最后一行",type(lnEnd_json), "\n",lnEnd_json)
    del lnEnd_json



# 即将处理第0行日志
# 即将处理第500000行日志
# 即将处理第1000000行日志
# 即将处理第1500000行日志
# 已处理,文件/fridaAnlzAp/frida_js/frida-out-Pure-1712123780.log共1619593行
# 最后一行 <class 'dict'> 
#     {'tmPnt': 1619593, 'logId': 1619593, 'processId': 21580, 'curThreadId': 21580, 'direct': 2, 'fnAdr': '0x7ffff61c7c50', 'fnCallId': 809561, 'fnSym': {'address': '0x7ffff61c7c50', 'name': '__do_global_dtors_aux', 'moduleName': 'libc10.so', 'fileName': '', 'lineNumber': 0, 'column': 0}}
