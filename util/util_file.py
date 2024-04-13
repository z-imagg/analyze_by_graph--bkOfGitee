#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 文件工具


from pathlib import Path

def readTxt(filePath:str) ->str :
    txt = Path(filePath).read_text()
    return txt

#删除路径（繁琐模式）
def unlink_verbose(_file_path:str)->None:
    fp=Path(_file_path)
    
    type_txt="文件"  if fp.is_file() else "非文件"
    type_txt="目录"  if fp.is_dir() else "非文件、非目录"
    
    abs_txt=fp.absolute().as_posix()
    
    exists_txt="存在" if fp.exists() else "不存在"
    
    print(f"【{exists_txt}】 文件种类【{type_txt}】 路径【{abs_txt}】",end="")
    
    fp.unlink(missing_ok=True)
    exists_after_del__txt="存在" if fp.exists() else "不存在"
    print(f"，删除后, 该路径【{exists_after_del__txt}】  ")
    return
