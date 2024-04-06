#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S
#【术语】 itm==item

from collections import defaultdict
import typing
from neo4j import Session
from neo4j.graph import Node
from dbConn_inject_neo4j import dbConn_inject_neo4j_default
from util_basic import assertRE_fnAdr_eq_RL__return_fnAdr, assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf, lsIsEmpty
from util_file import readTxt
from neo4j_misc import update__init_markup_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_update
from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
import json
    
class Item:
    def __init__(self,fnAdr:str,cnt:int) -> None:
        self.fnAdr:str=fnAdr
        self.cnt:int=cnt
    
    @staticmethod
    def buildFromTupleLs(tupleLs:typing.List[typing.Tuple[str,int]]) ->typing.List['Item']:
        if lsIsEmpty(tupleLs): return None
        ls:typing.List['Item'] = [Item(fnAdr,cnt)  for fnAdr,cnt in tupleLs ]
        return ls
    
    def __repr__(self) -> str:
        return f"【Item】{self.fnAdr}:{self.cnt}"
    

class Markup:
    def __init__(self) -> None:
        self.itmLs:typing.List[Item] = []
    
    def 填1个(self,fnAdr:str ):
        self.itmLs.append(Item(fnAdr,1))
        return self
    
    @staticmethod
    def merge(*markupLs:typing.List['Markup'])-> 'Markup':
        m:Markup
        dct = defaultdict(int)
        for m in markupLs:
            for j in m.itmLs:
                dct[j.fnAdr] += j.cnt
        
        newMarkup=Markup()
        itms:typing.List[Item]=Item.buildFromTupleLs(dct.items())
        newMarkup.itmLs.extend(itms)
        
        return newMarkup

    def assert_uniqe(self):
        fnAdrLs=[ i.fnAdr for i in self.itmLs]
        fnAdrLsLen=len(fnAdrLs)
        fnAdrSetLen=len(set(fnAdrLs))
        assert fnAdrLsLen == fnAdrSetLen, "此算法(遍历器 或 成份 业务函数)有错，因为itmLs的地址们应该是唯一的，但这里不唯一"
    def _to_json(self) -> dict:
        self.assert_uniqe()
        return dict([(item.fnAdr, item.cnt) for item in self.itmLs])

    def jsonTxt(self)->str:
        _jsonTxt: str = json.dumps(self, default=lambda o: o._to_json())
        return _jsonTxt

class BzWriteMarkup(TraverseAbs):
    cypher__update_setFieldMarkup=readTxt("cypher_src/update_setFieldMarkup.cypher") 
    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算成份 并 写字段markup
    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[Markup], _) -> Markup:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,_)

        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)

        #断言起点、终点fnAdr相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnAdr=assertRE_fnAdr_eq_RL__return_fnAdr(RE,RL)

        markup:Markup=None
        if isLeaf:
            #不写成份字段
            markup= Markup( ).填1个(fnAdr)
        else:
            #写成份字段
            markup= Markup( ).merge(*S)
            markupJsonTxt:str=markup.jsonTxt()
            neo4j_update(self.N.sess,"update_setFieldMarkup",BzWriteMarkup.cypher__update_setFieldMarkup,params={"prm_fnCallId":fnCallId,"prm_markup":markupJsonTxt},filedName="更新记录数")
            print(f"BzWriteMarkup.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段markup; 第{self.Vi}次遍历")
        
        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return markup





    

def _bz_markup_write_main(sess:Session):
    from neo4j_tool_traverse import NTT
    RootFnCallId=667245 #13,229638,667245

    #初始化: 全体置空markup字段
    # update__init_markup_as_null(sess)

    # 起点RE
    RE:Node=NTT(sess).getE_byFnCallId(RootFnCallId)
    # 遍历过程中 计算深度
    BzWriteMarkup(sess).V(RE)

if __name__=="__main__":
    dbConn_inject_neo4j_default(_bz_markup_write_main)

