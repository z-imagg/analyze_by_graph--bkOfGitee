#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Session
from neo4j.graph import Node
import pandas
from bz_util import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from file_tool import readTxt
from neo4j_main import neo4jMain
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_query, neo4j_query_RowLs, neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
from math import log2

cypher__query__链条_宽_宽1深=readTxt("cypher_src/query__链条_宽_宽1深.cypher") 





from itertools import chain
from pathlib import Path
import json
def _visual_main(sess:Session):
    rowLs:typing.List[typing.Dict[str,typing.Any]]=neo4j_query_RowLs(sess,"_visual_main", cypher__query__链条_宽_宽1深, params={})
    # nodeLs:typing.List[Node]=rowLs["v"]
    nodeLs_visjs=[ {  "id":r["fnCallId"],"size":int(log2(1+r["width"])), "label":r["fnSym_name"], "shape":"dot" , 
              #后面这些字段是方便开发调试用的,多字段 对vis.js无造成影响
               "fnCallId":r["fnCallId"],  "width":r["width"], "fnSym_name":r["fnSym_name"],   } for r in rowLs]
    
    _edgeLs=[
    [ (r["fnCallId"],x) for x in json.loads(r["sonFnCallIdLs"]) ]  
for r in rowLs 
]
    #展平嵌套列表
    edgeLs=list(chain.from_iterable(_edgeLs))

    edgeLs_visjs=[{"from":parentFnCallId, "to":sonFnCallId} for parentFnCallId,sonFnCallId in edgeLs]

    nodeLs_jsonTxt_visjs=json.dumps(nodeLs_visjs)
    edgeLs_jsonTxt_visjs=json.dumps(edgeLs_visjs)

    nodeLs_bigJsVar_visjs=f"var generated_nodeLs_visjs={nodeLs_jsonTxt_visjs}"
    edgeLs_bigJsVar_visjs=f"var generated_edgeLs_visjs={edgeLs_jsonTxt_visjs}"
    Path("./visual/generated_nodeLs_visjs.js").write_text(nodeLs_bigJsVar_visjs)
    Path("./visual/generated_edgeLs_visjs.js").write_text(edgeLs_bigJsVar_visjs)
    end=True


if __name__=="__main__":
    neo4jMain(_visual_main)



    

