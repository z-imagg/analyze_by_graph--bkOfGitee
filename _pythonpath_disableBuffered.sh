#!/usr/bin/env bash

#【描述】 PYTHONPATH配置  、 设置python的stdout无缓存（即默认flush）
#【使用举例】  
# source /fridaAnlzAp/analyze_by_graph/_pythonpath_disableBuffered.sh
# python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py #...

#'-e': 任一语句异常将导致此脚本终止; '-u': 使用未声明变量将导致异常; 
set -e -u  


#设置python的stdout无缓存（即默认flush）
export PYTHONUNBUFFERED=1

_PyDirCommon="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/db_conn_inject"

#fridaLog转sqlite3转neo4j
_PYTHONPATH__fridaLog_to_sqlite3_to_neo4j="$_PyDirCommon:/fridaAnlzAp/analyze_by_graph/_sqlite3/:/fridaAnlzAp/analyze_by_graph/fridaLog-sqlite3-neo4j/:"



#neo4j遍历器算法
_PYTHONPATH__neo4j_traverse="$_PyDirCommon:/fridaAnlzAp/analyze_by_graph/neo4j_traverse/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/"



#初步可视化
_PYTHONPATH__basic_visual_main="$_PyDirCommon:/fridaAnlzAp/analyze_by_graph/visual/"
#上下 ， 哪一个是对的需要确认
# _PYTHONPATH__basic_visual_main="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/:/fridaAnlzAp/analyze_by_graph/db_conn_inject/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/visual/"
