#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Session
from neo4j.graph import Node
from bz_util import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from neo4j_main import neo4jMain
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs


class BzDeepth(TraverseAbs):
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度
    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[int], _)->int:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,_)

        #deepth数值列表即为S
        deepth_ls:typing.List[int]= S
        
        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)

        #叶子的deepth为0,非叶子的deepth为 1+直接孩子们的deepth的最大值
        d=0 if isLeaf  else 1+max(deepth_ls)

        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return d


import sys
def _bz_deepth_main(sess:Session):
    from neo4j_tool_traverse import NTT
    #1:不平衡点;  
    #孤立点群：{2:叶子}； 
    #孤立点群：{3:孩子为4，4:叶子}； 
    #孤立点群：{5:孩子为6， 6:孩子为7， 7:孩子为8， 8:孩子为9， 9:孩子为10、12， 10:孩子为11， 11:叶子， 12:叶子}；
    #孤立点群：{13:孩子为..., 229371:叶子} 此群点数庞大， fnCallId==229371是最后一个节点

    #初始化: 全体置空deepth字段
    # update__init_deepth_as_null(sess)

    startFnCallId=667243+1
    RootFnCallId=startFnCallId 
    while True:
        print(f"开始RootFnCallId={RootFnCallId}",end="; ",file=sys.stderr,flush=True)
        # 起点RE
        RE:Node=NTT(sess).getE_byFnCallId(RootFnCallId)
        # 遍历过程中 计算深度
        bz=BzDeepth(sess)
        bz.V(RE)
        endFnCallId= bz.fnCallId
        if endFnCallId - startFnCallId > 1000:
            print(f"发现长链条",file=sys.stderr)
            break
        else:
            print(f"短链条endFnCallId={endFnCallId}",file=sys.stderr)
            RootFnCallId=endFnCallId+1
            continue
        
"""
开始RootFnCallId=229372; 短链条endFnCallId=229400
开始RootFnCallId=229401; 短链条endFnCallId=229469
开始RootFnCallId=229470; 短链条endFnCallId=229538
开始RootFnCallId=229539; 短链条endFnCallId=229607
开始RootFnCallId=229608; 短链条endFnCallId=229624
开始RootFnCallId=229625; 短链条endFnCallId=229634
开始RootFnCallId=229635; 短链条endFnCallId=229636
开始RootFnCallId=229637; 短链条endFnCallId=229637
开始RootFnCallId=229638;  #可见下一个长链条是 起点是 fnCallId=229638, 根据运行结果 得知 终点是 fnCallId=667243

修改变量 startFnCallId 为 667243+1， 运行此程序 'python bz_deepth_main.py 1>/dev/null' ，得到结果:
开始RootFnCallId=667244; 短链条endFnCallId=667244
开始RootFnCallId=667245;  #可见下一个长链条是 起点是 fnCallId=667245
"""

if __name__=="__main__":
    neo4jMain(_bz_deepth_main)


    

