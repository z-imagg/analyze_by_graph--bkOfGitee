#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 日志文件全路径
#【术语】 
#【备注】 
#【术语】 

import typing

## 获取 日志文件全路径



from pathlib import Path
def getLogFullPath()->str:
    logF_ls=[ * Path("/fridaAnlzAp/frida_js/").glob("./frida-out-Pure-*.log") ]
    assert len(logF_ls)==1


    # 日志文件全路径举例: TorchFnCallLogFP="/fridaAnlzAp/frida_js/frida-out-Pure-1712031317.log"



    TorchFnCallLogFP=logF_ls[0].as_posix()
    return TorchFnCallLogFP
