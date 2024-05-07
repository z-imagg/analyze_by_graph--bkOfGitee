#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  


cd /fridaAnlzAp/analyze_by_graph/

#安装依赖
pip install -r requirements.txt


now="$(date +%s)"

#设置python的stdout无缓存（即默认flush）
export PYTHONUNBUFFERED=1


export PYTHONPATH="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/:/fridaAnlzAp/analyze_by_graph/db_conn_inject/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/visual/"

#构造喂给cytoscape的neo4j表
python visual/visual_main.py | tee _visual_main-${now}.log


