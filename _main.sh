#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

#'-e': 任一语句异常将导致此脚本终止; '-u': 使用未声明变量将导致异常; '-o pipefail': 管道不吃错误代码
#         'set -o pipefail ; errCmd | tee my.log || echo ErrMsg' : 管道不吃错误代码, errCmd的错误将透过tee传递到 ||后的echo 因此显示'ErrMsg'
#         'set +o pipefail ; errCmd | tee my.log || echo ErrMsg' : 管道吃错误代码,  errCmd的错误传到tee, 而tee正常执行,因此||后的echo不对执行, 因此不显示'ErrMsg'
set -e -u -o pipefail

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

_PyDirCommon="/fridaAnlzAp/analyze_by_graph/:/fridaAnlzAp/analyze_by_graph/util/:/fridaAnlzAp/analyze_by_graph/_neo4j/:/fridaAnlzAp/analyze_by_graph/db_conn_inject"

export PYTHONPATH="$_PyDirCommon:/fridaAnlzAp/analyze_by_graph/_sqlite3/:/fridaAnlzAp/analyze_by_graph/fridaLog-sqlite3-neo4j/:"

#fridaLog转sqlite3转neo4j
_errMsg1="_main_fridaLog-sqlite3-neo4j.py报错，请解决后，重新执行此脚本analyze_by_graph/_main.sh,退出代码"
#                                               'set -o pipefail': 管道后的tee不吃错误代码 
python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-neo4j-${now}.log || { _exitCode1=$? ; echo "${_errMsg1} ${_exitCode1}" ; exit $_exitCode1 ;}

read -p "fridaLog转sqlite3转neo4j 已执行完毕，按回车则将执行遍历器:"

export PYTHONPATH="$_PyDirCommon:/fridaAnlzAp/analyze_by_graph/neo4j_traverse/:/fridaAnlzAp/analyze_by_graph/neo4j_traverse_bz/:/fridaAnlzAp/analyze_by_graph/visual/"

#遍历器
python neo4j_traverse_bz/_main_neo4j_traverse_bz.py 2>&1 | tee _main_neo4j_traverse_bz-${now}.log

#构造喂给cytoscape的neo4j表
read -p "遍历器执行完毕, 请你人工修改  query__链条_宽_宽1深.cypher(被visual_main.py调) 以在单线程的全链条中挑选一个链条:"

python visual/visual_main.py 2>&1 | tee _visual_main-${now}.log

md5sum *.log > log.md5sum-${now}.txt

