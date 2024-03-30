from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver
from neo4j import Record,Result,Session
from neo4j.graph import Node
import pandas
import typing
import numpy

from datetime import datetime
def nowDateTimeTxt():
    return datetime.now()   .strftime( '%Y-%m-%d %H:%M:%S %f' )

NEO4J_DB="neo4j"


fnCallIdLs_noDeepth_query="""
MATCH (logV:V_FnCallLog )
WHERE   logV.deepth is NULL
return distinct logV.fnCallId  as _fnCallId
"""
fnSym_name__queryBy_fnCallId="""
MATCH (logV:V_FnCallLog )
WHERE   logV.fnCallId =$fnCallId
return  logV 
"""

#来自文件 neo4j_Cypher_example.cypher
Cypher_update_deepth="""
MATCH path = (fromLog:V_FnCallLog {fnCallId:$fnCallId} )-[:E_NxtTmPnt* 1 .. __tmPntLength__ ]->(toLog:V_FnCallLog {fnCallId:$fnCallId})
WHERE 
// 1. 存在 中间时刻点 深度比该深度小1 
any( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = $this_deepth-1 )
// 且 
// 2.所有中间时刻点 深度 都 已知 
//    即 所有中间时刻点 深度 都 小于等于 该深度-1 , 因为 当前所有已知深度 就是 小于等于 该深度-1
// 可以表明 起点和终点 为 该深度, 这是 深度准确定义吧
AND all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth  is not null )
// 起点fromLog 无 深度字段deepth
AND fromLog.deepth is null
// 终点toLog 无 深度字段deepth
AND toLog.deepth is null
//neo4j的索引, 为何 范围条件 比 精确条件 快?
// 范围条件
AND  $fnCallId=fromLog.fnCallId  AND   $fnCallId=toLog.fnCallId
SET fromLog.deepth = $this_deepth, toLog.deepth = $this_deepth
// RETURN fromLog,toLog
return count(fromLog)+count(toLog) AS updated_rows
"""

def query_2dFnCallIdLs_noDeepth(sess:Session, granularity=100)->typing.List[typing.List[int]]:
    reslt:Result=sess.run(query=fnCallIdLs_noDeepth_query)
    reslt_df:pandas.DataFrame=reslt.to_df()
    _1d_ls:typing.List[int]=reslt_df["_fnCallId"].to_list()
    print(f"{nowDateTimeTxt()},无深度字段的函数调用数目为:{len(_1d_ls)}", flush=True)
    ndarray_ls=numpy.array_split(_1d_ls,granularity)
    _2d_ls=[list(k) for k in ndarray_ls]
    return _2d_ls

#neo4j 计算函数调用日志节点 深度
def update_deepth(sess:Session,fnCallIdLs:typing.List[int],this_deepth:int):
    for fnCallId in fnCallIdLs: 
        print(f"fnCallId={fnCallId}",end=";;")
        try:
            logLs=sess.run(query=fnSym_name__queryBy_fnCallId, fnCallId=fnCallId).to_df().to_dict(orient="records")
            logEnter:Node=logLs[0]["logV"]
            logLeave:Node=logLs[1]["logV"]
            assert logEnter["fnSym_name"] == logLeave["fnSym_name"]
            fnSym_name:str=logEnter["fnSym_name"]
            
            tmPntEnter:int=logEnter["tmPnt"]
            tmPntLeave:int=logLeave["tmPnt"]
            #中间时刻节点 个数 取 中间时刻点个数最大个数,  越到上层越吃亏
            tmPntLength:int = tmPntLeave-(tmPntEnter-1)

            #更新深度
            updateRs:Result=sess.run( 
    query=Cypher_update_deepth.replace("__tmPntLength__", f"{tmPntLength}"),  
    fnCallId=fnCallId,  this_deepth=this_deepth 
    )
            updateRs_df:pandas.DataFrame=updateRs.to_df()
            #被更新的记录行数
            updateRowCnt:int=updateRs_df.to_dict(orient="records")[0]["updated_rows"] #if len(updRsData)>0  else 0
            if updateRowCnt > 0:
                print(f"{nowDateTimeTxt()},匹配目标深度{this_deepth}; 更新{updateRowCnt}行日志; fnCallId={fnCallId},fnSym_name={fnSym_name}", flush=True)
            # else:
            #     print(f"{nowDateTimeTxt()},非目标深度{this_deepth}; 无更新日志; fnCallId={fnCallId},fnSym_name={fnSym_name}, ", flush=True)

    
        except (Exception,) as  err:
            LV=locals()
            print(f"发生错误,fnCallId={fnCallId},tmPntEnter={LV.get('tmPntEnter','')}, tmPntLeave={LV.get('tmPntLeave','')} ")
            import traceback
            traceback.print_exception(err)




def _main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")


    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            for deepth_j in range(1,10):
                _2d_fnCallIdLs:typing.List[typing.List[int]]=query_2dFnCallIdLs_noDeepth(sess)
                for k,fnCallIdLs in enumerate(_2d_fnCallIdLs):
                    update_deepth(sess,fnCallIdLs,this_deepth=deepth_j)
            
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()