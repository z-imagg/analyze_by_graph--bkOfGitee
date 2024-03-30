
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

import threading
thrdVarDct = threading.local()

from datetime import datetime,timedelta
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

cypher__update_deepth__kp1_by_k=readTxt("cypher_src/update_deepth__kp1_by_k.cypher") 
cypher__cnt_deepth_null=readTxt("cypher_src/cnt_deepth_null.cypher") 


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

def update_deepth__kp1_by_k(sess:Session,deepthK:int)->int:
    #根据 四点深度递推模式 ， 已知 深度k 递推的 求 深度k+1
    reslt:Result=sess.run(query=cypher__update_deepth__kp1_by_k, K=deepthK)
    reslt_df:pandas.DataFrame=reslt.to_df()
    路径数目:int=reslt_df["路径数目"].to_list()[0]
    print(f"update_deepth__kp1_by_k {nowDateTimeTxt()}, 四点深度递推模式，已知深度k={deepthK}求深度k+1, 路径数目:{路径数目} ", flush=True)
    return 路径数目


def cnt_deepth_null(sess:Session)->int:
    reslt:Result=sess.run(query=cypher__cnt_deepth_null)
    reslt_df:pandas.DataFrame=reslt.to_df()
    深度为空的节点个数:int=reslt_df["深度为空的节点个数"].to_list()[0]
    print(f"cnt_deepth_null {nowDateTimeTxt()},深度为空的节点个数:{深度为空的节点个数}", flush=True)
    return 深度为空的节点个数




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
            
            for deepthK in range(0,100):
                路径数目:int = update_deepth__kp1_by_k(sess,deepthK=deepthK)
                if 路径数目 == 0 :
                    print(f"深度{deepthK}下，四点深度递推模式 无匹配，因此深度更新结束")
                    break
            
            深度为空的节点个数:int=cnt_deepth_null(sess)
            if 深度为空的节点个数 > 0 :
                print(f"请您思考，为何还有节点的深度为空？深度为空的节点个数={深度为空的节点个数}")
            
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()