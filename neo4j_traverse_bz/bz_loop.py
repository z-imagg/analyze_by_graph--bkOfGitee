#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数, 链条 的 末尾FnCallId==endFnCallId
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import EagerResult, ResultSummary
from neo4j.graph import Node
from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from neo4j_tool import neo4j_query_1field1row, neo4j_query_1row
from neo4j_tool_traverse import NTT
from util_file import readTxt

class LoopTraverse( ):
    def __init__(self, trav: typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup]) -> None:
        self.trav:typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup] = trav

    def _minMax_fnCallId( this):
        CypherTxt=\
"""match (v:V_FnCallLog {direct:1})
return min(v.fnCallId) as min_fnCallId, max(v.fnCallId) as max_fnCallId
"""
        min_fnCallId,max_fnCallId=neo4j_query_1row(this.trav.N.sess,"",CypherTxt,params={},filedNameLs=["min_fnCallId","max_fnCallId"])
        return min_fnCallId,max_fnCallId

    def _next_begin_fnCallId( this,previous_end_fnCallId:int)->int:
        CypherTxt=readTxt("./cypher_src/query__next_chain__begin_fnCallId.cypher")
        next_begin_fnCallId=neo4j_query_1field1row(this.trav.N.sess,"",CypherTxt,params={"previous_end_fnCallId", previous_end_fnCallId} )
        return next_begin_fnCallId

    #写链条 首尾fnCallId
    def _write_chain( this,curThreadId,rootFnCallId,endFnCallId):
        result:EagerResult=this.trav.N.sess.run(
"CREATE (x:V_Chain {curThreadId: $curThreadId, rootFnCallId: $rootFnCallId, endFnCallId: $endFnCallId})",
curThreadId=curThreadId, rootFnCallId=rootFnCallId,  endFnCallId=endFnCallId)
        s=result.single()
        v=result.value()
        summary:ResultSummary=result.consume()
        print(f"_write_chain;curThreadId={curThreadId},rootFnCallId={rootFnCallId},curThreadId={endFnCallId},创建V_Chain节点{summary.counters.nodes_created}个,")

    def loop_traverse( this):
        min_fnCallId,max_fnCallId=this._minMax_fnCallId( )

        rootFnCallId:int=min_fnCallId
        while rootFnCallId!=max_fnCallId:

            assert rootFnCallId < max_fnCallId, "frida_js有逻辑错误， frida_js生成的fnCallId应该沿着链条递增"

            #初始化: 全体置空deepth|width|markup字段
            # this.trav.clear_field(this.trav.N.sess)

            # 起点RE
            RE:Node=NTT(this.trav.N.sess).getE_byFnCallId(rootFnCallId)
            curThreadId:int=RE["curThreadId"]
            # 遍历过程中 计算深度deepth|宽度width|成份markup
            this.trav.V(RE)
            #遍历完, 遍历器trav 的 curFnCallId == 链条 的 末尾FnCallId
            endFnCallId:int=this.trav.curFnCallId
            #写链条
            this._write_chain(curThreadId,rootFnCallId,endFnCallId)
            #切换到下一个链条
            # 已知上一个 孤立群 的 终点fnCallId 为 this.trav.curFnCallId , 求 下一个孤立群 的 起点fnCallId
            rootFnCallId=this._next_begin_fnCallId(this.trav.curFnCallId)


if __name__=="__main__":
    raise Exception("请运行_main_neo4j_traverse_bz.py")


    

