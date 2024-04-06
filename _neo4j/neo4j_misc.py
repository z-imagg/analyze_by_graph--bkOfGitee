from neo4j import Session

from util_datetime import nowDateTimeTxt
from util_file import readTxt

cypher__init_deepth_as_null=readTxt("cypher_src/init_deepth_as_null.cypher") 
cypher__init_width_as_null=readTxt("cypher_src/init_width_as_null.cypher") 
cypher__init_markup_as_null=readTxt("cypher_src/init_markup_as_null.cypher") 

from neo4j_tool import neo4j_update 


def update__loop_template(sess:Session,title,cypher_txt)->bool:
    for i in range(0,10):
        更新记录数=neo4j_update(sess,title,cypher_txt,params={"fnCallId_remainder10":i},filedName="更新记录数")
        print(f"{title}, {nowDateTimeTxt()},全体置空字段, 更新记录数:{更新记录数} ", flush=True)
    return True

def update__init_deepth_as_null(sess:Session)->bool:
    return update__loop_template(sess,"init_deepth_as_null",cypher__init_deepth_as_null)


def update__init_width_as_null(sess:Session)->bool:
    return update__loop_template(sess,"init_width_as_null",cypher__init_width_as_null)



def update__init_markup_as_null(sess:Session)->bool:
    return update__loop_template(sess,"init_markup_as_null",cypher__init_markup_as_null)

