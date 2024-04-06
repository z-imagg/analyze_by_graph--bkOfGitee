#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

from collections import defaultdict
import typing
from neo4j import Session
from neo4j.graph import Node
from util_basic import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from file_tool import readTxt
from neo4j_main import neo4jMain
from neo4j_misc import update__init_deepth_as_null, update__init_width_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
import json

class BzWriteWidth(TraverseAbs):
    cypher__update_width=readTxt("cypher_src/update_width.cypher") 

    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

    def bz(self, RE:Node, RL:Node, isLeaf:bool, _, C:typing.List[Node])->Node:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,C)
        sonLs:typing.List[Node]=C
        
        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)

        #叶子的width为0,非叶子的width为直接孩子个数
        #叶子的sonFnCallIdLs为空,非叶子的sonFnCallIdLs为直接孩子fnCallId列表
        if isLeaf:
            width=0
            sonFnCallIdLs= None
        else:
            width=len(sonLs)
            sonFnCallIdLs= [son["fnCallId"] for son in sonLs]

        _msg_sonFnCallIdLs= "sonFnCallIdLs为空" if sonFnCallIdLs is None else f"sonFnCallIdLs长度为{len(sonFnCallIdLs)}"
        
        jsonTxt_sonFnCallIdLs= None if sonFnCallIdLs is None else json.dumps(sonFnCallIdLs)
        params={"prm_fnCallId":fnCallId,"prm_width":width,"prm_sonFnCallIdLs":jsonTxt_sonFnCallIdLs}
        #写width字段、sonFnCallIdLs字段
        neo4j_update(self.N.sess,"update_width",BzWriteWidth.cypher__update_width,params=params,filedName="更新记录数")
        print(f"BzWriteWidth.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段width={width}写字段{_msg_sonFnCallIdLs}; 第{self.Vi}次遍历")



        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return None
    

def _bz_width_write_main(sess:Session):
    from neo4j_tool_traverse import NTT
    RootFnCallId=667245 #13,229638,667245

    #初始化: 全体置空width字段
    # update__init_width_as_null(sess)

    # 起点RE
    RE:Node=NTT(sess).getE_byFnCallId(RootFnCallId)
    # 遍历过程中 计算深度
    BzWriteWidth(sess).V(RE)


if __name__=="__main__":
    neo4jMain(_bz_width_write_main)



    

