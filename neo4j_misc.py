from neo4j import Session

from print_nowDateTime_with_prevSeconds_tool import nowDateTimeTxt
from file_tool import readTxt

cypher__init_deepth_as_null=readTxt("cypher_src/init_deepth_as_null.cypher") 

from neo4j_tool import neo4j_update 

def update__init_deepth_as_null(sess:Session)->bool:
    for i in range(0,10):
        更新记录数=neo4j_update(sess,"init_deepth_as_null",cypher__init_deepth_as_null,params={"fnCallId_remainder10":i},filedName="更新记录数")
        print(f"update__init_deepth_as_null, {nowDateTimeTxt()},全体置空deepth字段, 更新记录数:{更新记录数} ", flush=True)
    return True


