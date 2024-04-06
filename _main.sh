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
source /app/Miniconda3-py310_22.11.1-1/bin/activate
$bash_en_dbg && set -x #如果启用了调试模式, 则打开调试模式
# pip install -r requirements.txt


#删除旧日志
rm -frv *.log

now="$(date +%s)"

export PYTHONPATH="/fridaAnlzAp/analyze_by_graph/;/fridaAnlzAp/analyze_by_graph/_neo4j/;/fridaAnlzAp/analyze_by_graph/_sqlite3/;/fridaAnlzAp/analyze_by_graph/fridaLog-sqlite3-neo4j/;/fridaAnlzAp/analyze_by_graph/neo4j_traverse/;/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/;/fridaAnlzAp/analyze_by_graph/db_conn_inject/;/fridaAnlzAp/analyze_by_graph/util/;/fridaAnlzAp/analyze_by_graph/visual/"

#fridaLog-sqlite3-neo4j
python _main_fridaLog-sqlite3-neo4j.py | tee fridaLog-sqlite3-neo4j-${now}.log

#遍历器
python bz_deepth_write_main.py | tee bz_deepth_write_main-${now}.log
python bz_width_write_main.py | tee bz_width_write_main-${now}.log
python bz_markup_write_main.py | tee bz_markup_write_main-${now}.log


md5sum *.log > log.md5sum-${now}.txt

