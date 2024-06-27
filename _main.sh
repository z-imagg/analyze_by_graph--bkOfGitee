#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

#'-e': 任一语句异常将导致此脚本终止; '-u': 使用未声明变量将导致异常; '-o pipefail': 管道不吃错误代码
#         'set -o pipefail ; errCmd | tee my.log || echo ErrMsg' : 管道不吃错误代码, errCmd的错误将透过tee传递到 ||后的echo 因此显示'ErrMsg'
#         'set +o pipefail ; errCmd | tee my.log || echo ErrMsg' : 管道吃错误代码,  errCmd的错误传到tee, 而tee正常执行,因此||后的echo不对执行, 因此不显示'ErrMsg'
set -e -u -o pipefail

#bash允许alias展开
shopt -s expand_aliases   

#加载alias(临时禁止bash调试) (bashTmpDisDbgBegin_alias,bashTmpDisDbgEnd_alias)
source /app/bash-simplify/alias__bashTmpDisDbg.sh
# wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
# 临时禁止bash调试 以抑制 miniconda  的 activate 脚本 的大量输出
bashTmpDisDbgBegin_alias ; source /app/Miniconda3-py310_22.11.1-1/bin/activate ; bashTmpDisDbgEnd_alias

cd /fridaAnlzAp/analyze_by_graph/

#PYTHONPATH配置  、 设置python的stdout无缓存（即默认flush）
source _pythonpath_disableBuffered.sh

#安装依赖
pip install -r requirements.txt

#删除旧日志
rm -frv *.log

now="$(date +%s)"


#fridaLog转sqlite3转neo4j
_fridaLog_to_sqlite3_to_neo4j

read -p "fridaLog转sqlite3转neo4j 已执行完毕， 请输入 [ t :遍历器 ] (继续执行遍历器) 、 [ 空|q : 退出 ] (现在退出,即 只需要fridaLog转sqlite3) :"  act

#现在退出,即 只需要fridaLog转sqlite3
[[ $act == "q" || $act == "" ]] && exit 0

#neo4j遍历器算法
_neo4j_traverse

#构造喂给cytoscape的neo4j表
read -p "遍历器执行完毕, 请你人工修改  query__链条_宽_宽1深.cypher(被visual_main.py调) 以在单线程的全链条中挑选一个链条:"

#初步可视化
_visual_main

md5sum *.log > log.md5sum-${now}.txt


#########

#fridaLog转sqlite3转neo4j
function _fridaLog_to_sqlite3_to_neo4j(){
local _errMsg1="_main_fridaLog-sqlite3-neo4j.py报错，请解决后，重新执行此脚本analyze_by_graph/_main.sh,退出代码"


# fridaLog文件路径 == '配置文件 config.py / FnCallLogFP'
#                                               'set -o pipefail': 管道后的tee不吃错误代码 
PYTHONPATH="$_PYTHONPATH__fridaLog_to_sqlite3_to_neo4j" python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-neo4j-${now}.log || { _exitCode1=$? ; echo "${_errMsg1} ${_exitCode1}" ; exit $_exitCode1 ;}
}


#neo4j遍历器算法
function _neo4j_traverse(){
#遍历器
PYTHONPATH="$_PYTHONPATH__neo4j_traverse"  python neo4j_traverse_bz/_main_neo4j_traverse_bz.py 2>&1 | tee _main_neo4j_traverse_bz-${now}.log
}


#初步可视化
function _visual_main(){
PYTHONPATH="$_PYTHONPATH__basic_visual_main"  python visual/visual_main.py 2>&1 | tee _visual_main-${now}.log
}