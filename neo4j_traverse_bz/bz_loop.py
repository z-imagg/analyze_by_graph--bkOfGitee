#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【描述】 多个链，每个链条都得遍历
#【术语】 
#【返回类型说明】 
#【备注】 

import typing
from neo4j import EagerResult, ResultSummary
from neo4j.graph import Node
from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from neo4j_CAUD_chain import Neo4j_CAUD_chain
from neo4j_tool import neo4j_query_1field1row, neo4j_query_1row
from neo4j_tool_traverse import NTT
from util_file import readTxt

class LoopTraverse( ):
    def __init__(self, trav: typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup]) -> None:
        self.trav:typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup] = trav

    #进入循环之前做的事情
    def before_loop( this):
        #初始化: 全体置空deepth|width|markup字段
        this.trav.clear_field( )

    def loop_traverse( this):
        #进入循环之前做的事情
        this.before_loop()
        
        min_fnCallId,max_fnCallId=Neo4j_CAUD_chain._minMax_fnCallId(this.trav.N.sess )

        
        root_fnCallId:int=min_fnCallId
        while root_fnCallId!=max_fnCallId:

            assert root_fnCallId < max_fnCallId, "frida_js有逻辑错误， frida_js生成的fnCallId应该沿着链条递增"


            # 起点RE
            RE:Node=NTT(this.trav.N.sess).getE_byFnCallId(root_fnCallId)
            curThreadId:int=RE["curThreadId"] ; root_tmPnt:int=RE["tmPnt"]
            
            # 遍历过程中 计算深度deepth|宽度width|成份markup
            this.trav.V(RE)
            
            #遍历完, 遍历器trav 的 curFnCallId == 链条 的 末尾FnCallId
            end_fnCallId:int=this.trav.cur_fnCallId
            end_tmPnt:int=this.trav.cur_tmPnt

            #写链条
            # 理论上 每个chain写一次即可，但是这里图简单 每个Bz写了一次， 实际上 V_chain__Bz* 中的内容完全相同
            Neo4j_CAUD_chain._write_chain(this.trav.N.sess,this.trav.__class__.__name__, curThreadId,root_fnCallId,end_fnCallId, root_tmPnt, end_tmPnt)
            
            #切换到下一个链条
            # 已知上一个 孤立群 的 终点fnCallId 为 this.trav.curFnCallId , 求 下一个孤立群 的 起点fnCallId
            root_fnCallId=Neo4j_CAUD_chain._next_begin_fnCallId(this.trav.N.sess, this.trav.cur_fnCallId)


if __name__=="__main__":
    raise Exception("请运行_main_neo4j_traverse_bz.py")


    

