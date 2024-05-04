#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

function get_bash_en_dbg() {
  bash_en_dbg=false; [[ $- == *x* ]] && bash_en_dbg=true #记录bash是否启用了调试模式
}

cd /fridaAnlzAp/analyze_by_graph/

#安装frida py工具
# 临时关闭bash调试模式， 是 由于 miniconda 的 activate 脚本内容太大，从而减少视觉干扰
get_bash_en_dbg  #记录bash是否启用了调试模式
$bash_en_dbg && set +x #如果启用了调试模式, 则关闭调试模式
# wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
source /app/Miniconda3-py310_22.11.1-1/bin/activate
$bash_en_dbg && set -x #如果启用了调试模式, 则打开调试模式

#安装依赖
pip install -r requirements.txt


#删除旧日志
rm -frv *.log

now="$(date +%s)"

#设置python的stdout无缓存（即默认flush）
export PYTHONUNBUFFERED=1

export PYTHONPATH="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/_sqlite3/:/fridaAnlzAp/analyze_by_graph/fridaLog-sqlite3-neo4j/:/fridaAnlzAp/analyze_by_graph/db_conn_inject"

#fridaLog转sqlite3转neo4j
python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py | tee fridaLog-sqlite3-neo4j-${now}.log

read -p "fridaLog转sqlite3转neo4j 已执行完毕，按回车则将执行遍历器:"

export PYTHONPATH="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/:/fridaAnlzAp/analyze_by_graph/db_conn_inject/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/visual/"

#遍历器
python neo4j_traverse_bz/_main_neo4j_traverse_bz.py | tee _main_neo4j_traverse_bz-${now}.log

#构造喂给cytoscape的neo4j表
python visual/visual_main.py | tee _visual_main-${now}.log

md5sum *.log > log.md5sum-${now}.txt

