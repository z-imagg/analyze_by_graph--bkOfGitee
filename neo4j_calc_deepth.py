
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

from datetime import datetime
def nowDateTimeTxt():
    return datetime.now()   .strftime( '%Y-%m-%d %H:%M:%S %f' )

def readTxt(filePath:str) ->str :
    txt = Path(filePath).read_text()
    return txt

NEO4J_DB="neo4j"

deepth_0_set=readTxt("cypher_src/deepth_0_set.cypher") 
unique_fnAdr_ls=readTxt("cypher_src/unique_fnAdr_ls.cypher") 
max_tmLen__by_fnAdr=readTxt("cypher_src/max_tmLen__by_fnAdr.cypher") 

update_deepth_by_fnAdr__tmLen=readTxt("cypher_src/update_deepth_by_fnAdr__tmLen.cypher") 

def query__unique_fnAdr_ls(sess:Session)->typing.List[str]:
    reslt:Result=sess.run(query=unique_fnAdr_ls)
    reslt_df:pandas.DataFrame=reslt.to_df()
    _1d_ls:typing.List[str]=reslt_df["fnAdr"].to_list()
    print(f"{nowDateTimeTxt()},无深度字段的函数调用数目为:{len(_1d_ls)}", flush=True)
    return _1d_ls

def query__max_tmLen__by_fnAdr(sess:Session, fnAdr:str)->int:
    reslt:Result=sess.run(query=max_tmLen__by_fnAdr , fnAdr=fnAdr)
    reslt_df:pandas.DataFrame=reslt.to_df()
    _1d_ls:typing.List[str]=reslt_df["max_tmLen"].to_list()
    return _1d_ls[0]

#neo4j 计算函数调用日志节点 深度
def update_deepth(sess:Session,fnAdr:str,max_tmLen:int,this_deepth:int):
    print(f"fnAdr={fnAdr}",end=";;")
    try:

        #更新深度
        updateRs:Result=sess.run( 
query=update_deepth_by_fnAdr__tmLen.replace("__tmLen__", f"{max_tmLen}"),  
fnAdr=fnAdr,  this_deepth=this_deepth 
)
        updateRs_df:pandas.DataFrame=updateRs.to_df()
        #被更新的记录行数
        updateRowCnt:int=updateRs_df.to_dict(orient="records")[0]["updated_rows"] #if len(updRsData)>0  else 0
        if updateRowCnt > 0:
            print(f"{nowDateTimeTxt()},匹配目标深度{this_deepth},max_tmLen={max_tmLen}; 更新{updateRowCnt}行日志;   ", flush=True)
        else:
            # print(f"{nowDateTimeTxt()},非目标深度{this_deepth},max_tmLen={max_tmLen}; 无更新日志;    ", flush=True)
            print("")


    except (Exception,) as  err:
        LV=locals()
        print(f"发生错误,fnAdr={fnAdr},max_tmLen={max_tmLen}, this_deepth={this_deepth} ")
        import traceback
        traceback.print_exception(err)



def _main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")


    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        with driver.session(database=NEO4J_DB) as sess:
            #标记 叶子函数 ：  新增深度字段deepth，并设置深度数值为0
            reslt__deepth_0_set:Result=sess.run(query=deepth_0_set)
            
            for deepth_j in range(1,10):
                fnAdrLs:typing.List[str]=query__unique_fnAdr_ls(sess)
                for k,fnAdrK in enumerate(fnAdrLs):
                    max_tmLen:int=query__max_tmLen__by_fnAdr(sess,fnAdrK)
                    update_deepth(sess,fnAdrK,max_tmLen,this_deepth=deepth_j)
            
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()