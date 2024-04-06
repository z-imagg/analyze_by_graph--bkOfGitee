from neo4j import EagerResult,   ResultSummary 
import typing
import neo4j

from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from neo4j_delete_all import deleteAll
from neo4j_tool import neo4j_query_1field1row, neo4j_query_1row
from util_file import readTxt

class Neo4j_CAUD_chain:
    @staticmethod
    def _minMax_fnCallId( sess:neo4j.Session):
        CypherTxt=\
    """match (v:V_FnCallLog {direct:1})
    return min(v.fnCallId) as min_fnCallId, max(v.fnCallId) as max_fnCallId
    """
        min_fnCallId,max_fnCallId=neo4j_query_1row(sess,"",CypherTxt,params={},filedNameLs=["min_fnCallId","max_fnCallId"])
        return min_fnCallId,max_fnCallId

    @staticmethod
    def _next_begin_fnCallId( sess:neo4j.Session,previous_end_fnCallId:int)->int:
        CypherTxt=readTxt("./cypher_src/query__next_chain__begin_fnCallId.cypher")
        next_begin_fnCallId=neo4j_query_1field1row(sess,"query__next_chain__begin_fnCallId",CypherTxt,
    params={"previous_end_fnCallId":previous_end_fnCallId} ,
    filedName="next_begin_fnCallId")
        return next_begin_fnCallId

    #写链条 首尾fnCallId
    @staticmethod
    def _write_chain( sess:neo4j.Session, tabNameSuffix:str, curThreadId,root_fnCallId, end_fnCallId:int,   root_tmPnt:int,end_tmPnt:int):
        result:EagerResult=sess.run(
    "CREATE (x:V_Chain__tabNameSuffix__ {curThreadId: $curThreadId, root_fnCallId: $root_fnCallId, end_fnCallId: $end_fnCallId,   root_tmPnt:$root_tmPnt, end_tmPnt:$end_tmPnt })"
    .replace("tabNameSuffix__",tabNameSuffix)
    ,
    curThreadId=curThreadId, root_fnCallId=root_fnCallId,  end_fnCallId=end_fnCallId,    root_tmPnt=root_tmPnt,end_tmPnt=end_tmPnt)
        s=result.single()
        v=result.value()
        summary:ResultSummary=result.consume()
        print(f"_write_chain;curThreadId={curThreadId},root_fnCallId={root_fnCallId},end_fnCallId={end_fnCallId}, root_tmPnt={root_tmPnt},end_tmPnt={end_tmPnt},创建V_Chain节点{summary.counters.nodes_created}个,")


    #写链条 首尾fnCallId
    @staticmethod
    def _del_chain(sess:neo4j.Session):
        #### 删除顶点 V_Chain
        for tabNameSuffix in [BzDeepth.__class__.__name__,BzWriteDeepth.__class__.__name__,BzWriteWidth.__class__.__name__,BzWriteMarkup.__class__.__name__]:
            Cypher_delete_V="""
    MATCH (n:V_Chain__tabNameSuffix__)
    WITH n
    LIMIT 2
    DETACH DELETE n
        """.replace("tabNameSuffix__",tabNameSuffix)
            # 循环删除, 因为一次行删除 可能报内存超出
            deleteAll(sess,Cypher_delete_V)