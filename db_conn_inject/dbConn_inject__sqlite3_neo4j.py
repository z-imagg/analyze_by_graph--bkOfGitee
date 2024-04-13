#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
import sqlite3
import neo4j
from neo4j import Driver,GraphDatabase,Session
from fridaLog__sqlite3_reinitDbTabDef import reinit_sq3_db_tabDef
from neo4j_db_basic import Neo4J_DB_Entity, getDriver
import traceback

MyT = typing.TypeVar('MyT')

def dbConn_inject__sqlite3_neo4j(sqlite3_dbFilePath:str, neo4j_db_entity:Neo4J_DB_Entity,
    func:typing.Callable[
        [sqlite3.Connection,neo4j.Session #业务函数func具有的参数列表
        #  ,neo4j.Driver    #要不要给neo4j_dbDriver是有待考虑的
         ],  
        MyT #业务函数func的返回值类型
    ]
)->MyT:

    # sq_db_fp='./FnCallLog.db'
    ### 重初始化sqlite3数据库、表结构
    sq3dbConn:sqlite3.Connection=reinit_sq3_db_tabDef(sqlite3_dbFilePath)

    neo4j_dbDriver:neo4j.Driver=getDriver(neo4j_db_entity )
    
    try:
        with neo4j_dbDriver.session(database=neo4j_db_entity.DB_NAME) as neo4j_sess:
            return func(sq3dbConn, neo4j_sess
                # ,neo4j_dbDriver  #不给neo4j_dbDriver
                )

    except (Exception,) as  err1:
        traceback.print_exception(err1)
    finally:
        try:
            #提交sqlite3数据库
            sq3dbConn.commit()
        except (Exception,) as  err2:
            traceback.print_exception(err2)
        finally:
            try:
                #关闭sqlite3数据库
                sq3dbConn.close()
            except (Exception,) as  err3:
                traceback.print_exception(err3)
            finally:
                #关闭neo4j的连接
                neo4j_dbDriver.close() 