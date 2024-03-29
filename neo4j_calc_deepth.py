from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver
from neo4j import Record,Result,Session
import pandas
import typing
import numpy


NEO4J_DB="neo4j"

#开发用, 将某个 fnCallId 的 deepth 打回 为 空, 供继续 开发调试 
"""
MATCH (log:V_FnCallLog )
WHERE   log.fnCallId = 522501
// set log.deepth = NULL
// return和set是可以共存的
return log
// RETURN TRUE

"""

fnCallIdLs_noDeepth_query="""
MATCH (logV:V_FnCallLog )
WHERE   logV.deepth is NULL
return distinct logV.fnCallId  as _fnCallId
// limit 1000 //开发用,生成不要打开
"""
fnCallIdLs_query1Page_noDeepth="""
MATCH (logV:V_FnCallLog )
WHERE   logV.deepth is NULL
AND logV.fnCallId > $fnCallId_end_incld-$pageSize AND logV.fnCallId <= $fnCallId_end_incld
return distinct logV.fnCallId
// ORDER BY logV.fnCallId DESC
// limit 4 //开发调试用
"""

#来自文件 neo4j_Cypher_example.cypher
Cypher_update_deepth="""
MATCH path = (fromLog:V_FnCallLog {fnCallId:$fnCallId} )-[:E_NxtTmPnt*1..]->(toLog:V_FnCallLog {fnCallId:$fnCallId})
WHERE 
// 所有 中间点 的深度为0 即 所有 中间点 为 叶子节点
all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth <= $this_deepth-1 )
// 起点fromLog 无 深度字段deepth
AND (NOT exists(fromLog.deepth) )
// 终点toLog 无 深度字段deepth
AND (NOT exists(toLog.deepth)  )
//neo4j的索引, 为何 范围条件 比 精确条件 快?
// 范围条件
// AND fromLog.fnCallId <= $fnCallId AND  toLog.fnCallId <= $fnCallId     
AND  $fnCallId=fromLog.fnCallId  AND   $fnCallId=toLog.fnCallId
SET fromLog.deepth = $this_deepth, toLog.deepth = $this_deepth
// RETURN fromLog,toLog
return count(fromLog)+count(toLog) AS updated_rows
"""

def query_2dFnCallIdLs_noDeepth(sess:Session, granularity=100)->typing.List[typing.List[int]]:
    reslt:Result=sess.run(query=fnCallIdLs_noDeepth_query)
    reslt_df:pandas.DataFrame=reslt.to_df()
    # fnCallIdLs = reslt_df.to_dict()["_fnCallId"]
    ndarray_ls=numpy.array_split(reslt_df["_fnCallId"].to_list(),granularity)
    _2d_ls=[list(k) for k in ndarray_ls]
    return _2d_ls

#neo4j 计算函数调用日志节点 深度
def update_deepth(sess:Session,fnCallIdLs:typing.List[int],this_deepth:int):
    for fnCallId in fnCallIdLs: 
        #更新深度
        updateRs:Result=sess.run( query=Cypher_update_deepth,  fnCallId=fnCallId, this_deepth=this_deepth )
        updateRs_df:pandas.DataFrame=updateRs.to_df()
        #被更新的记录行数
        updateRowCnt:int=updateRs_df.to_dict(orient="records")[0]["updated_rows"] #if len(updRsData)>0  else 0
        if updateRowCnt > 0:
            print(f"更新记录行数为{updateRowCnt}, 更新fnCallId={fnCallId}的深度为{this_deepth}")
        else:
            print(f"无记录行被更新,fnCallId={fnCallId}不符合深度为{this_deepth}")

    
    


def _main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")


    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            _2d_fnCallIdLs:typing.List[typing.List[int]]=query_2dFnCallIdLs_noDeepth(sess)
            for k,fnCallIdLs in enumerate(_2d_fnCallIdLs):
                update_deepth(sess,fnCallIdLs,this_deepth=1)
        # calc_deepth(driver,this_deepth=2)
        # ...
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()