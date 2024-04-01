#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 从 cypher脚本模板 生成 cypher脚本

def newXJ(_ln:str,J:int):
    
    ln=_ln

    tJ=f"t{J}"
    ln=ln.replace("tJ",tJ)

    BJ=f"B{J}"
    ln=ln.replace("BJ",BJ)

    fJ=f"f{J}"
    ln=ln.replace("fJ",fJ)
    
    LJ=f"L{J}"
    ln=ln.replace("LJ",LJ)

    return ln

def replaceLn(ln:str,repeatCnt:int,tmplLnEndFlag1:str,tmplLnEndFlag2:str)->str:
    if ln .endswith(tmplLnEndFlag1) or ln.endswith(tmplLnEndFlag2): #"//点k路径（模板）\n"  "//点k条件（模板）\n"
        _=[newXJ(ln,J) for J in range(0,repeatCnt)]
        newLn="".join(_)
        return newLn
    else:
        return ln
        
def cypherTmplRender(tmplFP:str,repeatCnt:int,tmplLnEndFlag1:str,tmplLnEndFlag2:str):
    with open(tmplFP) as fr: #"cypher_src/update_deepth__Bnull_repeatK_Lnull__tmpl.cypher"
        lines=fr.readlines()
        newLines=[replaceLn(ln,repeatCnt,tmplLnEndFlag1,tmplLnEndFlag2) for ln in lines]
        _new_cypher_txt:str="".join(newLines)
        # print(f"_new_cypher_txt=【{_new_cypher_txt}】")
        return _new_cypher_txt

    raise Exception(f"不应该走到这里,repeatCnt={repeatCnt}")
