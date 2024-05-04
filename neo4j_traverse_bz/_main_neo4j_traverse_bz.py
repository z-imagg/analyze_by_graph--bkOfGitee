from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_loop import LoopTraverse
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from dbConn_inject_neo4j import dbConn_inject_neo4j_default
from neo4j_CAUD_chain import Neo4j_CAUD_chain
from neo4j_index_constraint import neo4j_recreateIdx
from util_file import readTxt


cypher__index_create=readTxt("cypher_src/index.cypher") 
dbConn_inject_neo4j_default(
lambda sess: 
    #遍历器开始前 创建索引 (执行   cypher_src/index.cypher )
    neo4j_recreateIdx(sess,cypher__index_create)
)

dbConn_inject_neo4j_default(
lambda sess: 
    #删除全部 V_chain
    Neo4j_CAUD_chain._del_chain(sess)
)

dbConn_inject_neo4j_default(
lambda sess: 
    #遍历孤立群 做BzDeepth业务， 多个遍历
    LoopTraverse(trav=BzDeepth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    #遍历孤立群 做BzWriteDeepth业务， 多个遍历
    LoopTraverse(trav=BzWriteDeepth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    #遍历孤立群 做BzWriteWidth业务， 多个遍历
    LoopTraverse(trav=BzWriteWidth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    #遍历孤立群 做BzWriteMarkup业务， 多个遍历
    LoopTraverse(trav=BzWriteMarkup(sess)).loop_traverse()
)