#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】  
#【返回类型说明】  
#【备注】 


from neo4j_db_basic import Neo4J_DB_Entity
from util_path import assertFilePathExisted, followFilePathSoftLink_getDirName_assert, make_parentDirOfFilePath

#frida_js/_main.sh中有如下定义 :
#  目前日志文件软链接
# _LogFP_PureNow_link="/gain/frida-out/PureNow.log"
# 【目前日志文件软链接举例】 /gain/frida-out/PureNow.log ---> /gain/frida-out/appName--qemu-system-x86_64--v8.2.2/Pure-1712031317.log
FnCallLogFP:str=assertFilePathExisted("/gain/frida-out/PureNow.log","frida_js产物日志文件找不到")
#  举例 appName=='qemu-system-x86_64--v8.2.2'
appName=followFilePathSoftLink_getDirName_assert(FnCallLogFP,"appName--")

sqlite3_dbFilePath=f'/gain/analyze_by_graph-out/FnCallLog--{appName}.db'
#创建sqlite3数据库文件的父目录
make_parentDirOfFilePath(sqlite3_dbFilePath)

neo4jDB_default= Neo4J_DB_Entity(URI="neo4j://localhost:7687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")