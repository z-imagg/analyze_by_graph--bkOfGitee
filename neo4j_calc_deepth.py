
#  已知 深度k-1 更新深度k,   给定 函数地址， 给定 调用过程持续时间长度（为了阻止neo4j查询发生组合爆炸）
#    不再按照单个 函数调用 来更新深度
from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver
from neo4j import Record,Result,Session
from neo4j.graph import Node
import pandas
import typing
import numpy
from pathlib import Path
from datetime import datetime,timedelta

#不平衡的时刻点个数 为 1，来自 .ipynb 
NotBlncTmPntCnt:int=1

import threading
thrdVarDct = threading.local()


def nowDateTimeTxt():
    #通用时间差 为  当前时刻 减去 本线程的前一个时刻
    _now=datetime.now()
    _nowTxt=_now.strftime( '%Y-%m-%d %H:%M:%S %f' )

    previous_now = getattr(thrdVarDct, 'previous_now', None)
    deltaTxt=None
    if previous_now is None:
        #初始 时间差为空串
        deltaTxt=""
    else:
        #平常 时间差为 此时 减去 前一个时刻
        delta:timedelta=_now-previous_now
        deltaTxt=f"{delta.seconds}.{delta.microseconds}秒"
    
    #下一回 的 前一个时刻 就是 此时
    thrdVarDct.previous_now=_now

    return  f"【{deltaTxt}；{_nowTxt}】"

def readTxt(filePath:str) ->str :
    txt = Path(filePath).read_text()
    return txt

NEO4J_DB="neo4j"

init_deepth_as_null=readTxt("cypher_src/init_deepth_as_null.cypher") 

deepth_0_set=readTxt("cypher_src/deepth_0_set.cypher") 
unique_fnAdr_ls__no_deepth=readTxt("cypher_src/unique_fnAdr_ls__no_deepth.cypher") 
max_tmLen__by_fnAdr=readTxt("cypher_src/max_tmLen__by_fnAdr.cypher") 

update_deepth_by_fnAdr__tmLen=readTxt("cypher_src/update_deepth_by_fnAdr__tmLen.cypher") 

def update__init_deepth_as_null(sess:Session)->bool:
    for i in range(0,10):
        reslt:Result=sess.run(query=init_deepth_as_null, fnCallId_remainder10=i)
        reslt_df:pandas.DataFrame=reslt.to_df()
        更新记录数:int=reslt_df["更新记录数"].to_list()[0]
        print(f"update__init_deepth_as_null, {nowDateTimeTxt()},全体置空deepth字段, 更新记录数:{更新记录数} ", flush=True)
    return True


def update__deepth_0_set(sess:Session)->int:
    #标记 叶子函数 ：  新增深度字段deepth，并设置深度数值为0
    reslt:Result=sess.run(query=deepth_0_set)
    reslt_df:pandas.DataFrame=reslt.to_df()
    叶子调用次数:int=reslt_df["叶子调用次数"].to_list()[0]
    叶子函数个数:int=reslt_df["叶子函数个数"].to_list()[0]
    print(f"update__deepth_0_set， {nowDateTimeTxt()},设置深度0, 叶子调用次数:{叶子调用次数},叶子函数个数:{叶子函数个数}", flush=True)
    return 叶子调用次数

def query__unique_fnAdr_ls(sess:Session)->typing.List[str]:
    reslt:Result=sess.run(query=unique_fnAdr_ls__no_deepth)
    reslt_df:pandas.DataFrame=reslt.to_df()
    fnAdr_ls:typing.List[str]=reslt_df["fnAdr"].to_list()
    print(f"query__unique_fnAdr_ls， {nowDateTimeTxt()},函数地址个数:{len(fnAdr_ls)}", flush=True)
    return fnAdr_ls

def query__max_tmLen__by_fnAdr(sess:Session, fnAdr:str)->typing.Tuple[int,int]:
    print(f"query__max_tmLen, {nowDateTimeTxt()}, fnAdr:{fnAdr}", flush=True, end=";; ")
    reslt:Result=sess.run(query=max_tmLen__by_fnAdr , fnAdr=fnAdr)
    reslt_df:pandas.DataFrame=reslt.to_df()
    min_tmLen:int=reslt_df["min_tmLen"].to_list()[0]
    max_tmLen:int=reslt_df["max_tmLen"].to_list()[0]
    print(f"{nowDateTimeTxt()},  min_tmLen:{min_tmLen}, max_tmLen:{max_tmLen}", flush=True)
    return min_tmLen,max_tmLen

#neo4j 计算函数调用日志节点 深度
def update_deepth(sess:Session,fnAdr:str,min_tmLen:int, max_tmLen:int,deepthK:int):
    print(f"update_deepth，fnAdr={fnAdr}",end=";;")
    try:

        #更新深度
        # 原本 ： 时刻点是连续的整数， 即 两点之间的时刻点个数 == 两点时刻点数值之差
        # 但是 由于 不平衡点 在 前置.ipynb处理 中 被删除了，  导致   两点之间的时刻点个数 + 此路径中 被删除的 不平衡点个数 == 两点时刻点数值之差
        # 因此 无脑的将 查找区间 左右扩大 不平衡点数 长度 即可
        _min_tmLen=max(min_tmLen-NotBlncTmPntCnt,1)
        _max_tmLen=max_tmLen+NotBlncTmPntCnt
        cypherTxt=update_deepth_by_fnAdr__tmLen\
.replace("__min_tmLen__", f"{_min_tmLen}")\
.replace("__max_tmLen__", f"{_max_tmLen}")
        updateRs:Result=sess.run( 
query=cypherTxt,   #保险起见  宽一点 用 max_tmLen+1
fnAdr=fnAdr,  deepthK=deepthK 
)
        updateRs_df:pandas.DataFrame=updateRs.to_df()
        #被更新的记录行数
        updateRowCnt:int=updateRs_df.to_dict(orient="records")[0]["updated_rows"] #if len(updRsData)>0  else 0
        if updateRowCnt > 0:
            print(f"{nowDateTimeTxt()},匹配深度{deepthK},max_tmLen={max_tmLen}; 更新{updateRowCnt}行日志;   ", flush=True)
        else:
            print(f"{nowDateTimeTxt()},非匹深度{deepthK},max_tmLen={max_tmLen}; 无更新日志;    ", flush=True)
            # print("")


    except (Exception,) as  err:
        LV=locals()
        print(f"发生错误,fnAdr={fnAdr},max_tmLen={max_tmLen}, deepthK={deepthK} ")
        import traceback
        traceback.print_exception(err)


def _main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")


    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            #全体置空deepth字段
            update__init_deepth_as_null(sess)
            #标记 叶子函数 ：  新增深度字段deepth，并设置深度数值为0
            update__deepth_0_set(sess)
            
            for deepthK in range(1,10):
                #查询 函数地址们fnAdrLs
                fnAdrLs:typing.List[str]=query__unique_fnAdr_ls(sess)
                for j,fnAdrJ in enumerate(fnAdrLs):
                    #查询 该函数地址 的 调用过程持续时间长度max_tmLen
                    min_tmLen,max_tmLen=query__max_tmLen__by_fnAdr(sess,fnAdrJ)
                    #已知 深度k-1 更新深度k,   给定 函数地址， 给定 调用过程持续时间长度（为了阻止neo4j查询发生组合爆炸）
                    update_deepth(sess,fnAdrJ,min_tmLen,max_tmLen,deepthK=deepthK)
            
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()