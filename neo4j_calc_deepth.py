from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver
from neo4j import Record,Result,Session
from neo4j.graph import Node
import pandas
import typing
import numpy
from pathlib import Path

from datetime import datetime
def nowDateTimeTxt():
    return datetime.now()   .strftime( '%Y-%m-%d %H:%M:%S %f' )

def readTxt(filePath:str) ->str :
    txt = Path(filePath).read_text()
    return txt

NEO4J_DB="neo4j"


fnCallIdLs_noDeepth_query=readTxt("cypher_src/fnCallIdLs_noDeepth_query.cypher") 
fnSym_name__queryBy_fnCallId=readTxt("cypher_src/fnSym_name__queryBy_fnCallId.cypher") 

Cypher_update_deepth=readTxt("cypher_src/Cypher_update_deepth.cypher") 

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
                print(f"{nowDateTimeTxt()},匹配目标深度{this_deepth},tmPntLength={tmPntLength}; 更新{updateRowCnt}行日志; fnCallId={fnCallId},fnSym_name={fnSym_name}", flush=True)
            else:
                # print(f"{nowDateTimeTxt()},非目标深度{this_deepth},tmPntLength={tmPntLength}; 无更新日志; fnCallId={fnCallId},fnSym_name={fnSym_name}, ", flush=True)
                print("")

    
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