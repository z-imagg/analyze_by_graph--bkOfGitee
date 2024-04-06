#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
import neo4j
from neo4j import Driver,GraphDatabase
from neo4j_db_basic import Neo4J_DB_Entity, getDriver
import traceback
from config import neo4jDB_default

MyT2 = typing.TypeVar('MyT2')

#neo4j 数据库连接 注入模板
def dbConn_inject_neo4j(neo4jBbEntity:Neo4J_DB_Entity,
    func:typing.Callable[
        [neo4j.Session],
        MyT2
    ]
)->MyT2:
    neo4jDbDriver:Driver=getDriver(neo4jBbEntity )

    try:
        with neo4jDbDriver.session(database=neo4jBbEntity.DB_NAME) as neo4j_sess:
            return func(neo4j_sess)

    except (Exception,) as  err:
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        neo4jDbDriver.close()


def dbConn_inject_neo4j_default( 
    func:typing.Callable[
        [neo4j.Session],
        MyT2
    ]
)->MyT2:
    return dbConn_inject_neo4j(neo4jDB_default,func)