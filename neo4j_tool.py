# from neo4j import GraphDatabase, RoutingControl
# from neo4j import Driver
# from neo4j import Record
# from neo4j.graph import Node
from neo4j import Result,Session
import pandas
import typing

from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt

def neo4j_update(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any],filedName:str)->int:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    更新记录数:int=reslt_df[filedName].to_list()[0]
    print(f"{title}, {nowDateTimeTxt()}, 更新记录数:{更新记录数} ", flush=True)
    return 更新记录数


def neo4j_query(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any] )->pandas.DataFrame:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    print(f"neo4j_query 【{title}】, {nowDateTimeTxt()}, 查询结果尺寸:{reslt_df.size} ", flush=True)
    return reslt_df

def neo4j_query_1field1row(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any],filedName:str )->pandas.DataFrame:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    rowLs=reslt_df[filedName].to_list()  #[0]
    if len(rowLs)>0 : 
        assert len(rowLs) == 1, f"neo4j_query_1field1row 必须只能有1条记录,实际行数={len(rowLs)}"
    val=rowLs[0]
    print(f"neo4j_query_1field1row 【{title}】, {nowDateTimeTxt()}, 查询结果:{val} ", flush=True)
    return val