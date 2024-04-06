# from neo4j import GraphDatabase, RoutingControl
# from neo4j import Driver
# from neo4j import Record
from neo4j.graph import Node,Path
from neo4j import Result,Session
import pandas
import typing

from tool_datetime import nowDateTimeTxt

def neo4j_update(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any],filedName:str)->int:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    更新记录数:int=reslt_df[filedName].to_list()[0]
    # print(f"{title}, {nowDateTimeTxt()}, 更新记录数:{更新记录数} ", flush=True)
    return 更新记录数


def neo4j_query(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any] )->pandas.DataFrame:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    # print(f"neo4j_query 【{title}】, {nowDateTimeTxt()}, 查询结果尺寸:{reslt_df.size} ", flush=True)
    return reslt_df

#要求cypher语句中return的是单纯字段 而不能是复合字段
def neo4j_query_RowLs(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any]  )->typing.List[typing.Dict[str,typing.Any]]:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    #orient : str {'dict', 'list', 'series', 'split', 'records', 'index'}
    rowLs:typing.List[typing.Dict[str,typing.Any]]=reslt_df.to_dict(orient="records" )
    # print(f"neo4j_query 【{title}】, {nowDateTimeTxt()}, 查询结果尺寸:{rowLs.__len__()} ", flush=True)
    return rowLs


def neo4j_query_1row(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any],filedNameLs:typing.List[str] )->typing.Union[Node,Path]:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    records=reslt_df.to_dict(orient="records")
    rowCnt=len(records) #rowCnt==行数
    if rowCnt == 0:
        return None,cypherTxt
    #若有，则只能有1行
    if rowCnt>0:
        assert rowCnt == 1, f"rowCnt{rowCnt}!=1"

    row0=records[0]#row0==首行
    valLs= [row0[fn] for fn in filedNameLs]
    # print(f"neo4j_query_1row 【{title}】, {nowDateTimeTxt()}, 查询结果尺寸:{len(valLs)} ", flush=True)
    return valLs

def neo4j_query_1field1row(sess:Session,title:str,cypherTxt:str,params:typing.Dict[str,typing.Any],filedName:str )->typing.Union[Node,Path]:
    reslt:Result=sess.run(query=cypherTxt, parameters=params)
    reslt_df:pandas.DataFrame=reslt.to_df()
    rowLs=reslt_df[filedName].to_list()  #[0]
    assert rowLs is not Node, "据说pandas.DataFrame.to_list一定不会返回None? 即使无也返回空列表?"
    rowCnt=len(rowLs)
    if rowCnt==0:
        return None
    if rowCnt>0 : 
        assert rowCnt == 1, f"neo4j_query_1field1row 必须只能有1条记录,实际行数={rowCnt}"
    val:Node=rowLs[0]
    # print(f"neo4j_query_1field1row 【{title}】, {nowDateTimeTxt()}, 查询结果:{val} ", flush=True)
    return val