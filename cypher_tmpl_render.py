#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 从 cypher脚本模板 生成 cypher脚本
import typing

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

def _endswith_ls(ln:str, *flagS:str)->bool:
    fitFlagS:typing.List[str]=list(filter(lambda flagK: ln.endswith(f"{flagK}\n"), flagS))
    assert fitFlagS is not None, "据说list(filter(func,ls))若空返回空列表，而不会返回None"
    len_fitFlagS:int=len(fitFlagS)
    if len_fitFlagS >0 :
        assert len_fitFlagS == 1, f"你怎么能匹配到多个标志词呢？手误？ln={ln}, flagS={flagS}"
    fit:bool = len_fitFlagS == 1
    return fit


def _remove_flags(_newLn:str, *flagS:str)->str:
    newLn=_newLn
    for k,flagK in enumerate(flagS):
        newLn = newLn.replace(flagK,f" //渲染{k}")
    return newLn

def replaceLn(ln:str,repeatCnt:int, *flagS:str)->str:
    if _endswith_ls(ln, *flagS): #"//点k路径（模板）\n"  "//点k条件（模板）\n"
        newLnS=[_remove_flags ( newXJ(ln,J), *flagS ) for J in range(0,repeatCnt)]
        newLnMerge="".join(newLnS)
        return newLnMerge
    else:
        return ln
        
def cypherTmplRender(tmplFP:str,repeatCnt:int,*flagS:str):
    with open(tmplFP) as fr: #"cypher_src/update_deepth__Bnull_repeatK_Lnull__tmpl.cypher"
        lines=fr.readlines()
        newLines=[replaceLn(ln,repeatCnt,*flagS) for ln in lines]
        _new_cypher_txt:str="".join(newLines)
        # print(f"_new_cypher_txt=【{_new_cypher_txt}】")
        return _new_cypher_txt

    raise Exception(f"不应该走到这里,repeatCnt={repeatCnt}")
