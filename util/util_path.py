#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 路径工具函数
#【术语】 
#【备注】 此文不能依赖上层业务脚本，否则可能循环依赖
#【术语】 


import typing

#断言路径存在
from pathlib import Path
def assertFilePathExisted(fPTxt:str,errMsg:str)->str:
    logFp=Path(fPTxt)
    assert logFp.exists(), f"【断言失败 路径不存在】【errMsg='{errMsg}'】 【fPTxt={fPTxt}】"
    return   fPTxt

#解析给定路径的实际指向，获得该实际指向的目录名, 并断言该目录名含有assertWord
def followFilePathSoftLink_getDirName_assert(fPTxt:str,assertWord:str)->str:
    fP=Path(fPTxt)
    targetFP=fP.resolve().absolute()
    _dirName:str=targetFP.parent.name
    
    #断言 目录名包含 assertWord
    assert assertWord is not None and _dirName.__contains__(assertWord)
    
    dirName=_dirName.replace(_dirName,assertWord)
    
    return   dirName
