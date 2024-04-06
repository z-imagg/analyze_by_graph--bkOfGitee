#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数, 链条 的 末尾FnCallId==endFnCallId
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
import neo4j
from neo4j import EagerResult, ResultSummary
from neo4j.graph import Node
from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from neo4j_CAUD_chain import Neo4j_CAUD_chain
from neo4j_tool import neo4j_query_1field1row, neo4j_query_1row
from neo4j_tool_traverse import NTT
from util_basic import assert_ls_as_set_only_1_element
from util_file import readTxt


class LoopTraverse( ):
    def __init__(self, sess:neo4j.Session, trav_ls: typing.List[typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup]]) -> None:
        self.sess:neo4j.Session=sess
        assert len(trav_ls) > 0
        self.trav_ls:typing.List[typing.Union[BzDeepth,BzWriteDeepth,BzWriteWidth,BzWriteMarkup]] = trav_ls

    #进入循环之前做的事情
    def before_loop( this):
        input("neo4j,即将进行全表删除操作，按回车即删除；Ctrl+C终止本程序则不会执行删除")
        #初始化: 全体置空deepth|width|markup字段
        for trav in this.trav_ls:
            trav.clear_field( )

    def loop_traverse( this):
        #进入循环之前做的事情
        this.before_loop()
        
        min_fnCallId,max_fnCallId=Neo4j_CAUD_chain._minMax_fnCallId(this.sess )

        
        root_fnCallId:int=min_fnCallId
        while root_fnCallId!=max_fnCallId:

            assert root_fnCallId < max_fnCallId, "frida_js有逻辑错误， frida_js生成的fnCallId应该沿着链条递增"


            # 起点RE
            RE:Node=NTT(this.sess).getE_byFnCallId(root_fnCallId)
            curThreadId:int=RE["curThreadId"] ; root_tmPnt:int=RE["tmPnt"]
            
            # 遍历过程中 计算深度deepth|宽度width|成份markup
            for trav in this.trav_ls:
                trav.V(RE)
            
            #这里其实也很丑陋
            #遍历完, 遍历器trav 的 curFnCallId == 链条 的 末尾FnCallId
            end_fnCallId:int=assert_ls_as_set_only_1_element([trav.cur_fnCallId for trav in this.trav_ls ])
            end_tmPnt:int=assert_ls_as_set_only_1_element([trav.cur_tmPnt for trav in this.trav_ls ])

            #写链条
            Neo4j_CAUD_chain._write_chain(this.sess, curThreadId,root_fnCallId,end_fnCallId, root_tmPnt, end_tmPnt)
            
            #切换到下一个链条
            # 已知上一个 孤立群 的 终点fnCallId 为 this.trav.curFnCallId , 求 下一个孤立群 的 起点fnCallId
            root_fnCallId=Neo4j_CAUD_chain._next_begin_fnCallId(this.sess, end_fnCallId)


if __name__=="__main__":
    raise Exception("请运行_main_neo4j_traverse_bz.py")


    

