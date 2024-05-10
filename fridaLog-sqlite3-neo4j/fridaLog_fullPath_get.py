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
    #frida_js/_main.sh中有如下定义 :
    #  目前日志文件软链接
    _LogFP_PureNow_link="/gain/frida-out/PureNow.log"

    # 【目前日志文件软链接举例】 /gain/frida-out/PureNow.log ---> /gain/frida-out/torch/Pure-1712031317.log

    logFp=Path(_LogFP_PureNow_link)
    assert logFp.exists(), f"断言失败 目前日志文件软链接 不存在. _LogFP_PureNow_link={_LogFP_PureNow_link}"
    
    logFpTxt=logFp.as_posix()
    return logFpTxt
