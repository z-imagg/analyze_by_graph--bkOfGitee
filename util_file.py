#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 文件工具


from pathlib import Path

def readTxt(filePath:str) ->str :
    txt = Path(filePath).read_text()
    return txt
