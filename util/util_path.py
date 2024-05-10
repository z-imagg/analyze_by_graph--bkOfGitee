#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 路径工具函数
#【术语】 
#【备注】 
#【术语】 


import typing

#断言路径存在
from pathlib import Path
def assertFilePathExisted(fPTxt:str,errMsg:str)->str:
    logFp=Path(fPTxt)
    assert logFp.exists(), f"【断言失败 路径不存在】【errMsg='{errMsg}'】 【fPTxt={fPTxt}】"
    return   fPTxt
