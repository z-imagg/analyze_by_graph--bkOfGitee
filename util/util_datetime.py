#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 打印当前时刻、到上次调用本方法过去的秒数

import threading
thrdVarDct = threading.local()

from datetime import datetime,timedelta
def nowDateTimeTxt():
    #通用时间差 为  当前时刻 减去 本线程的前一个时刻
    _now=datetime.now()
    _nowTxt=_now.strftime( '%Y-%m-%d %H:%M:%S %f' )

    previous_now = getattr(thrdVarDct, 'previous_now', None)
    deltaTxt=None
    if previous_now is None:
        #初始 时间差为空串
        deltaTxt=""
    else:
        #平常 时间差为 此时 减去 前一个时刻
        delta:timedelta=_now-previous_now
        deltaTxt=f"{delta.seconds}.{delta.microseconds}秒"
    
    #下一回 的 前一个时刻 就是 此时
    thrdVarDct.previous_now=_now

    return  f"【{deltaTxt}；{_nowTxt}】"



def printLn(msgLn:str):
    print(f"{nowDateTimeTxt()}{msgLn}")