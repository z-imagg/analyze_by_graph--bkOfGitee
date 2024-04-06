from bz_deepth_main import BzDeepth
from bz_deepth_write_main import BzWriteDeepth
from bz_loop import LoopTraverse
from bz_markup_write_main import BzWriteMarkup
from bz_width_write_main import BzWriteWidth
from dbConn_inject_neo4j import dbConn_inject_neo4j_default


dbConn_inject_neo4j_default(
lambda sess: 
    LoopTraverse(trav=BzDeepth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    LoopTraverse(trav=BzWriteDeepth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    LoopTraverse(trav=BzWriteWidth(sess)).loop_traverse()
)

dbConn_inject_neo4j_default(
lambda sess: 
    LoopTraverse(trav=BzWriteMarkup(sess)).loop_traverse()
)