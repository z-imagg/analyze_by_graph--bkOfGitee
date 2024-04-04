#!/usr/bin/env python
# -*- coding: utf-8 -*-

from neo4j import Driver,GraphDatabase
from neo4j_db_entity import Neo4J_DB_Entity

def getDriver(db:Neo4J_DB_Entity)->Driver:
    driver:Driver=GraphDatabase.driver(db.URI, auth=(db.AUTH_user,db.AUTH_pass))
    assert isinstance(driver, Driver) == True
    return driver

#neo4j 两个数据库连接 主程序模板
def neo4j2dbMain(db1:Neo4J_DB_Entity,db2:Neo4J_DB_Entity,func):


    driver1:Driver=getDriver(db1 )
    driver2:Driver=getDriver(db2 )


    try:
        with driver1.session(database=db1.DB_NAME) as sess1:
            with driver2.session(database=db2.DB_NAME) as sess2:
                func(driver1, sess1, driver2, sess2)

    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        try:
            driver1.close()
        except:
            pass
        finally:
            driver2.close()